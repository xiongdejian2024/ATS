#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_diag_tcam_full_new.py
@time         : 2023/12/1 14:19
@author       : wenyu.liang_ext@jiduauto.com
@description  : 
'''


import os
import sys
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))


from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


#pytest basetech/diagnostics/test_diag_tcam_full.py::TestEOL::test_caseid_1981700
#pytest basetech/diagnostics/test_diag_tcam_full.py::TestUdSService::test_caseid_1981141 --disable_env=true  --bl_ver=v_2_0_0
#pytest basetech/diagnostics/test_diag_tcam_full.py::TestDID::test_caseid_1981651
# @pytest.mark.repeat(200)

@allure.feature('TCAM BaseTech/诊断')
class TestEOL(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self,ecu)
        with allure.step("初始化环境"):
            self.mix.init_boot_per()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,check_data='62f18601',check_length=8)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        with allure.step("初始化环境"):
            self.mix.init_boot_per()
        super().after_class(self, ecu)

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F18C_01会话下')
    def test_caseid_1981750(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF18C,SESSION.DEFAULT,'62f18c',check_length=14)

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F18C_02会话下')
    def test_caseid_1981749(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF18C,SESSION.PROGRAMMING,'62f18c',check_length=14)

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F18C_03会话下')
    def test_caseid_1981748(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF18C,SESSION.EXTENDED,'62f18c',check_length=14)
   
    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1A0_01会话下')
    def test_caseid_1981747(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1A0,SESSION.DEFAULT,'62f1a0',check_length=22)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1A0_02会话下')
    def test_caseid_1981746(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1A0,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1A0_03会话下')
    def test_caseid_1981745(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1A0,SESSION.EXTENDED,'62f1a0',check_length=22)

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1AA_01会话下')
    def test_caseid_1981744(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1AA,SESSION.DEFAULT,'62f1aa',check_length=22)

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1AA_02会话下')
    def test_caseid_1981743(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1AA,SESSION.PROGRAMMING,'62f1aa',check_length=22)

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1AA_03会话下')
    def test_caseid_1981742(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1AA,SESSION.EXTENDED,'62f1aa',check_length=22)

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1AB_01会话下')
    def test_caseid_1981741(self):
       self.sd_tester.read_did_and_check(TA.TCAM,0xF1AB,SESSION.DEFAULT,'62f1ab',check_length=22)

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1AB_02会话下')
    def test_caseid_1981740(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1AB,SESSION.PROGRAMMING,'62f1ab',check_length=22)

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1AB_03会话下')
    def test_caseid_1981739(self):
       self.sd_tester.read_did_and_check(TA.TCAM,0xF1AB,SESSION.EXTENDED,'62f1ab',check_length=22)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1AE_01会话下')
    def test_caseid_1981738(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1AE,SESSION.DEFAULT,'62f1ae',check_length=24)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1AE_02会话下')
    def test_caseid_1981737(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1AE,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1AE_03会话下')
    def test_caseid_1981736(self):
       self.sd_tester.read_did_and_check(TA.TCAM,0xF1AE,SESSION.EXTENDED,'62f1ae',check_length=24)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)_2ED01C_01会话下')
    def test_caseid_1981735(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD01C,SESSION.DEFAULT,UnLock.L0,'A2C837613E12B712ADF3F540751F77A24E82B9E01C61D152FA1DFAA3D699E8A4670FB350628FB490732E948473A9273FB76D62DFEC15CDF8AB8310199A23FCBF2EA3C91593E855968626E197F30D048D90F0BB95CB2C501E09DBCFA3BA4A8CE6F8461EF1EE4527732D976E5D494D43DE009F02A91329A44E26EDF3CD61E1B02633B9E9AC196D79072203F9F009FEC94E4A1BB9B0040346BC6B645C29E614ED2C9B82C681C8374817231298F716DD8CA26E5D18B9E8BD05AC14339B81C0C6E2EEB27ED1F570C0425147B2429665E11F08675E3FDAE30D0A336A2897231B8A8BEDD965E3464943085A3DA026C807FB52BEE8B0972AFDFC477EB2F88187305D381F00010001C0E7686676D89205A740DEE5A0E8E269FFCA903A3C36EC1309A76825A6C54DC0','7f2e31',check_method=Check_Method.response,recover=False)



    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)_2ED01C_03会话下')
    def test_caseid_1981733(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD01C,SESSION.EXTENDED,UnLock.L0,'A2C837613E12B712ADF3F540751F77A24E82B9E01C61D152FA1DFAA3D699E8A4670FB350628FB490732E948473A9273FB76D62DFEC15CDF8AB8310199A23FCBF2EA3C91593E855968626E197F30D048D90F0BB95CB2C501E09DBCFA3BA4A8CE6F8461EF1EE4527732D976E5D494D43DE009F02A91329A44E26EDF3CD61E1B02633B9E9AC196D79072203F9F009FEC94E4A1BB9B0040346BC6B645C29E614ED2C9B82C681C8374817231298F716DD8CA26E5D18B9E8BD05AC14339B81C0C6E2EEB27ED1F570C0425147B2429665E11F08675E3FDAE30D0A336A2897231B8A8BEDD965E3464943085A3DA026C807FB52BEE8B0972AFDFC477EB2F88187305D381F00010001C0E7686676D89205A740DEE5A0E8E269FFCA903A3C36EC1309A76825A6C54DC0''7f2e31',check_method=Check_Method.response,recover=False)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2EF102_01会话下')
    def test_caseid_1981732(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xF102,SESSION.DEFAULT,UnLock.L0,'FFFFFFFFEE','7f2e31',check_method=Check_Method.response,recover=False)



    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2EF102_03会话下')
    def test_caseid_1981730(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xF102,SESSION.EXTENDED,UnLock.L0,'FFFFFFFFEE','7f2e31',check_method=Check_Method.response,recover=False)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22408F_01会话下')
    def test_caseid_1981729(self):
       self.sd_tester.read_did_and_check(TA.TCAM,0x408F,SESSION.DEFAULT,'7f2231')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22408F_02会话下')
    def test_caseid_1981728(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0x408F,SESSION.PROGRAMMING,'7f2231')
 
    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22408F_03会话下')
    def test_caseid_1981727(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,check_data='6712')
        self.sd_tester.read_did_and_check(TA.TCAM,0x408F,SESSION.EMPTY,'62408f55555555555555555555555555555555')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2E408F_01会话下')
    def test_caseid_1981726(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0x408F,SESSION.DEFAULT,UnLock.L0,'50555555555555555555555555555555','7f2e31',check_method=Check_Method.response,recover=False)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2E408F_02会话下')
    def test_caseid_1981725(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0x408F,SESSION.PROGRAMMING,UnLock.L0,'50555555555555555555555555555555','7f2e31',check_method=Check_Method.response,recover=False)

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2E408F_03会话下')
    def test_caseid_1981724(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,check_data='6712')
        self.sd_tester.write_did_and_check(TA.TCAM,0x408F,SESSION.EMPTY,UnLock.L0,'50555555527387809980803092308934','62408f50555555527387809980803092308934',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0x408F,SESSION.EMPTY,UnLock.L0,'50555555023009235949555555550000','62408f50555555023009235949555555550000',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0x408F,SESSION.EMPTY,UnLock.L0,'50658454923893902555555555555555','62408f50658454923893902555555555555555',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0x408F,SESSION.EMPTY,UnLock.L0,'50555555555555897631254879090000','62408f50555555555555897631254879090000',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0x408F,SESSION.EMPTY,UnLock.L0,'55555555555555555555555555555555','62408f55555555555555555555555555555555',check_method=Check_Method.read,recover=False)


    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_2241AE_01会话下')
    def test_caseid_1981723(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0x41AE,SESSION.DEFAULT,'6241ae',check_length=46)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_2241AE_02会话下')
    def test_caseid_1981722(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0x41AE,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_2241AE_03会话下')
    def test_caseid_1981721(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0x41AE,SESSION.EXTENDED,'6241ae',check_length=46)

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_229003_01会话下')
    def test_caseid_1981720(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0x9003,SESSION.DEFAULT,'629003',check_length=36)

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_229003_02会话下')
    def test_caseid_1981719(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0x9003,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_229003_03会话下')
    def test_caseid_1981718(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0x9003,SESSION.EXTENDED,'629003',check_length=36)

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22CF05_01会话下')
    def test_caseid_1981717(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xCF05,SESSION.DEFAULT,'62cf05',check_length=36)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22CF05_02会话下')
    def test_caseid_1981716(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xCF05,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22CF05_03会话下')
    def test_caseid_1981715(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xCF05,SESSION.EXTENDED,'62cf05',check_length=36)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED12F_01会话下')
    def test_caseid_1981714(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD12F,SESSION.DEFAULT,UnLock.L0,'FFFFFFFFEE','7f2e31',check_method=Check_Method.response,recover=False)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED12F_02会话下')
    def test_caseid_1981713(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD12F,SESSION.PROGRAMMING,UnLock.L0,'FFFFFFFFEE','7f2e31',check_method=Check_Method.response,recover=False)


    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D917_01会话下')
    def test_caseid_1981711(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD917,SESSION.DEFAULT,'62d917',check_length=36)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D917_02会话下')
    def test_caseid_1981710(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD917,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D917_03会话下')
    def test_caseid_1981709(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD917,SESSION.EXTENDED,'62d917',check_length=36)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22B163_01会话下')
    def test_caseid_1981708(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xB163,SESSION.DEFAULT,'7f2231')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22B163_02会话下')
    def test_caseid_1981707(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xB163,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22B163_L5_03会话下')
    def test_caseid_1981706(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.read_did_and_check(TA.TCAM,0xb163,SESSION.EMPTY,'62b163')
    

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22B163_L7_03会话下')
    def test_caseid_1981703(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.read_did_and_check(TA.TCAM,0xB163,SESSION.EMPTY,'62b163',check_length=38)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2EB163_01会话下')
    def test_caseid_1981702(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xB163,SESSION.DEFAULT,UnLock.L0,'11223344556677881122334455667788','7f2e31',check_method=Check_Method.response,recover=False)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2EB163_L7_02会话下')
    def test_caseid_1981701(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xB163,SESSION.PROGRAMMING,UnLock.L0,'11223344556677881122334455667788','7f2e31',check_method=Check_Method.response,recover=False)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2EB163_L7_03会话下')
    def test_caseid_1981700(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.write_did_and_check(TA.TCAM,0xB163,SESSION.EMPTY,UnLock.L0,'236427a27bfac547bf3028e457fd7375','62b163236427a27bfac547bf3028e457fd7375',check_method=Check_Method.read)
        self.sd_tester.write_did_and_check(TA.TCAM,0xB163,SESSION.EMPTY,UnLock.L0,'e8200f671b1401b525e23660ed2611b8','62b163e8200f671b1401b525e23660ed2611b8',check_method=Check_Method.read)
        self.sd_tester.write_did_and_check(TA.TCAM,0xB163,SESSION.EMPTY,UnLock.L0,'721a3d6a1b8aefc061ecc6c5b25c52dd','62b163721a3d6a1b8aefc061ecc6c5b25c52dd',check_method=Check_Method.read)
        self.sd_tester.write_did_and_check(TA.TCAM,0xB163,SESSION.EMPTY,UnLock.L0,'e8200f671b1401b53564865876584658','62b163e8200f671b1401b53564865876584658',check_method=Check_Method.read)
        self.sd_tester.write_did_and_check(TA.TCAM,0xB163,SESSION.EMPTY,UnLock.L0,'721a3d6a1b8a6598765934c5b25c52dd','62b163721a3d6a1b8a6598765934c5b25c52dd',check_method=Check_Method.read)

class TestUdSService(TestABCBase): 
    def before_class(self, ecu):
        super().before_class(self,ecu)
        with allure.step("初始化环境"):
            self.mix.init_boot_per()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,check_data='62f18601',check_length=8)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        with allure.step("初始化环境"):
            self.mix.init_boot_per()
        super().after_class(self, ecu)
        
    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('ECU启动时间测试')
    def test_caseid_1981276(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'1103','5103')
        before = time.time()
        time.sleep(15)
        while True:
            if '5003' == self.sd_tester.send_data_and_check(TA.TCAM,'1003')[0:4]:
                break
            else:
                time.sleep(1)
        extended_response_time = time.time() - before
        logger.info(f'extended_response_time :{extended_response_time}')

        # before = time.time()
        while True:
            if '6705' == self.sd_tester.send_data_and_check(TA.TCAM,'2705','')[0:4]:
                break
            else:
                time.sleep(1)

        security_l5_time = time.time() - before
        logger.info(f'security_l5_time :{security_l5_time}')
        
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EMPTY,UnLock.L11,UnlockStep.key)

        while True:
            if '62408f' == self.sd_tester.read_did_and_check(TA.TCAM,0x408F,SESSION.EMPTY,'')[0:6]:
                break
            else:
                time.sleep(1)

        remote_vehicle_immobilization_secret_key_time = time.time() - before
        logger.info(f'remote_vehicle_immobilization_secret_key_time :{remote_vehicle_immobilization_secret_key_time}')
        while True:
            if '6707' == self.sd_tester.send_data_and_check(TA.TCAM,'2707','')[0:4]:
                break
            else:
                time.sleep(1)

        security_l7_time = time.time() - before
        logger.info(f'security_l7_time :{security_l7_time}')
        after = time.time()
        logger.info(f'TCAM from send 1103 for reset to work  interval time={after - before}')
        assert after - before <180,'TCAM重启到工作超过180s'

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1001)_01会话下')
    def test_caseid_1981275(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1001)_03会话下')
    def test_caseid_1981274(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1001)_02会话下')
    def test_caseid_1981273(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')

    
    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1081)_01会话下')
    def test_caseid_1981272(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.update_serverdoipid(0x1011)
        self.sd_tester.send_data([0x10,0x81])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        time.sleep(0.03)
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1081)_02会话下')
    def test_caseid_1981271(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.update_serverdoipid(0x1011)
        self.sd_tester.send_data([0x10,0x81])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        time.sleep(0.03)
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1081)_03会话下')
    def test_caseid_1981270(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.update_serverdoipid(0x1011)
        self.sd_tester.send_data([0x10,0x81])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        time.sleep(0.03)
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1002)_01会话下')
    def test_caseid_1981269(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'1002')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1002)_02会话下')
    def test_caseid_1981268(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'1002')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1002)_03会话下')
    def test_caseid_1981267(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'1002')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1082)_01会话下')
    def test_caseid_1981266(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.update_serverdoipid(0x1011)
        self.sd_tester.send_data([0x10,0x82])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        time.sleep(0.03)
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1082)_02会话下')
    def test_caseid_1981265(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.update_serverdoipid(0x1011)
        self.sd_tester.send_data([0x10,0x82])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        time.sleep(0.03)
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1082)_03会话下')
    def test_caseid_1981264(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.update_serverdoipid(0x1011)
        self.sd_tester.send_data([0x10,0x82])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        time.sleep(0.03)
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1003)_01会话下')
    def test_caseid_1981263(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'1003')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1003)_02会话下')
    def test_caseid_1981262(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'1003')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1003)_03会话下')
    def test_caseid_1981261(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'1003')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1083)_01会话下')
    def test_caseid_1981260(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.update_serverdoipid(0x1011)
        self.sd_tester.send_data([0x10,0x83])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        time.sleep(0.03)
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1083)_02会话下')
    def test_caseid_1981259(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.update_serverdoipid(0x1011)
        self.sd_tester.send_data([0x10,0x83])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        time.sleep(0.03)
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x1083)_03会话下')
    def test_caseid_1981258(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.update_serverdoipid(0x1011)
        self.sd_tester.send_data([0x10,0x83])
        self.sd_tester.return_udsdata_and_check_and_print_response_result()
        time.sleep(0.03)
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x10)_01会话下NRC12')
    def test_caseid_1981257(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'1000','7f1012')
        self.sd_tester.send_data_and_check(TA.TCAM,'1011','7f1012')
        self.sd_tester.send_data_and_check(TA.TCAM,'1022','7f1012')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x10)_02会话下NRC12')
    def test_caseid_1981256(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'1000','7f1012')
        self.sd_tester.send_data_and_check(TA.TCAM,'1011','7f1012')
        self.sd_tester.send_data_and_check(TA.TCAM,'1022','7f1012')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x10)_03会话下NRC12')
    def test_caseid_1981255(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'1000','7f1012')
        self.sd_tester.send_data_and_check(TA.TCAM,'1011','7f1012')
        self.sd_tester.send_data_and_check(TA.TCAM,'1022','7f1012')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x10)_01会话下NRC13')
    def test_caseid_1981254(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'10','7f1013')
        self.sd_tester.send_data_and_check(TA.TCAM,'100102','7f1013')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x10)_02会话下NRC13')
    def test_caseid_1981253(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'10','7f1013')
        self.sd_tester.send_data_and_check(TA.TCAM,'100102','7f1013')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x10)_03会话下NRC13')
    def test_caseid_1981252(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'10','7f1013')
        self.sd_tester.send_data_and_check(TA.TCAM,'100102','7f1013')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x10)_01会话下NRC22')
    def test_caseid_1981251(self):  
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.DEFAULT,'62dd0a')
        self.sd_tester.send_data_and_check(TA.TCAM,'1002','7f1022')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')
        self.sd_tester.change_usage_mode(UsageMode.ABANDONED)


    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SessionControl(0x10)_03会话下NRC22')
    def test_caseid_1981249(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.change_usage_mode(UsageMode.DRIVING)
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EXTENDED,'62dd0a')
        self.sd_tester.send_data_and_check(TA.TCAM,'1002','7f1022')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')
        self.sd_tester.change_usage_mode(UsageMode.ABANDONED)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_EcuReset(0x1103)_01会话下')
    def test_caseid_1981248(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'1103','7f117e')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_EcuReset(0x1103)_02会话下')
    def test_caseid_1981247(self):
        self.mix.init_boot_per()
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'1103','7f117e')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_EcuReset(0x1103)_03会话下')
    def test_caseid_1981246(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'1103','5103')
        time.sleep(180)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_EcuReset(0x1103)_01会话下NRC12')
    def test_caseid_1981245(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'1100','7f1112')
        self.sd_tester.send_data_and_check(TA.TCAM,'1111','7f1112')
        self.sd_tester.send_data_and_check(TA.TCAM,'1122','7f1112')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')
        
    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_EcuReset(0x1103)_02会话下NRC12')
    def test_caseid_1981244(self):
        self.mix.init_boot_per()
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'1100','7f1112')
        self.sd_tester.send_data_and_check(TA.TCAM,'1111','7f1112')
        self.sd_tester.send_data_and_check(TA.TCAM,'1122','7f1112')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_EcuReset(0x1103)_03会话下NRC12')
    def test_caseid_1981243(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'1100','7f1112')
        self.sd_tester.send_data_and_check(TA.TCAM,'1111','7f1112')
        self.sd_tester.send_data_and_check(TA.TCAM,'1122','7f1112')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_EcuReset(0x1103)_01会话下NRC13')
    def test_caseid_1981242(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'11','7f1113')
        self.sd_tester.send_data_and_check(TA.TCAM,'110311','7f1113')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_EcuReset(0x1103)_02会话下NRC13')
    def test_caseid_1981241(self):
        self.mix.init_boot_per()
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'11','7f1113')
        self.sd_tester.send_data_and_check(TA.TCAM,'110311','7f1113')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_EcuReset(0x1103)_03会话下NRC13')
    def test_caseid_1981240(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'11','7f1113')
        self.sd_tester.send_data_and_check(TA.TCAM,'110311','7f1113')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_EcuReset(0x1103)_01会话下NRC22')
    def test_caseid_1981239(self):
        self.mix.init_boot_per()
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,SESSION.EXTENDED,UnLock.L7,'0100','7101a040')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16501')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'1103','7f1122')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,SESSION.EXTENDED,UnLock.L7,'02FF','7101a040')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16502')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_EcuReset(0x1103)_02会话下NRC22')
    def test_caseid_1981238(self):
        self.mix.init_boot_per()
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,SESSION.EXTENDED,UnLock.L7,'0100','7101a040')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16501')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'1103','7f1122')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,SESSION.EXTENDED,UnLock.L7,'02FF','7101a040')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16502')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_EcuReset(0x1103)_03会话下NRC22')
    def test_caseid_1981237(self):
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,SESSION.EXTENDED,UnLock.L7,'0100','7101a040')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16501')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'1103','7f1122')
        self.sd_tester.routine_ctrl_and_check(TA.BGM_SOC,0xa040,0x01,SESSION.EXTENDED,UnLock.L7,'02FF','7101a040')
        self.sd_tester.read_did_and_check(TA.BGM_SOC,0xb165,SESSION.EMPTY,'62b16502')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level1_01会话下')
    def test_caseid_1981236(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'2701','7f277f')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level5_01会话下')
    def test_caseid_1981235(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'2705','7f277f')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level7_01会话下')
    def test_caseid_1981234(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'2707','7f277f')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level11_01会话下')
    def test_caseid_1981233(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'2711','7f277f')

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level1_02会话下')
    def test_caseid_1981232(self):
        self.mix.init_boot_per()
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        
    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level5_02会话下')
    def test_caseid_1981231(self):
        self.mix.init_boot_per()
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'2705','7f277e')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level7_02会话下')
    def test_caseid_1981230(self):
        self.mix.init_boot_per()
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'2707','7f277e')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level11_02会话下')
    def test_caseid_1981229(self):
        self.mix.init_boot_per()
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'2711','7f277e')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_EcuReset(0x27)_level1_03会话下')
    def test_caseid_1981228(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'2701','7f277e')

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level5_03会话下')
    def test_caseid_1981227(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L5,check_data='6706')

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level7_03会话下')
    def test_caseid_1981226(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EMPTY,UnLock.L0,check_data='6708')

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level11_03会话下')
    def test_caseid_1981225(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,check_data='6712')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_03会话下NRC12')
    def test_caseid_1981224(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'2733','7f2712')
        self.sd_tester.send_data_and_check(TA.TCAM,'2755','7f2712')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_02会话下NRC12')
    def test_caseid_1981223(self):
        self.mix.init_boot_per()
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'2713','7f2712')
        self.sd_tester.send_data_and_check(TA.TCAM,'2715','7f2712')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_02会话下NRC13')
    def test_caseid_1981222(self):
        self.mix.init_boot_per()
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'27','7f2713')
        self.sd_tester.send_data_and_check(TA.TCAM,'270101','7f2713')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_03会话下NRC13')
    def test_caseid_1981221(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'27','7f2713')
        self.sd_tester.send_data_and_check(TA.TCAM,'270501','7f2713')
        self.sd_tester.send_data_and_check(TA.TCAM,'270701','7f2713')
        self.sd_tester.send_data_and_check(TA.TCAM,'271101','7f2713')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x2705)_03会话下NRC35_36_37')
    def test_caseid_1981220(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L5,UnlockStep.seed,check_data='6705')
        self.sd_tester.send_data_and_check(TA.TCAM,'2706000000','7f2735')
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L5,UnlockStep.seed,check_data='6705')
        self.sd_tester.send_data_and_check(TA.TCAM,'2706000000','7f2736')
        time.sleep(9)
        self.sd_tester.send_data_and_check(TA.TCAM,'2705','7f2737')
        
        
    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x2707)_03会话下NRC35_36_37')
    def test_caseid_1981219(self):
        # self.mix.init_boot_per()
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,UnlockStep.seed,check_data='6707')
        self.sd_tester.send_data_and_check(TA.TCAM,'270800000000000000000000000000000000','7f2735')
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,UnlockStep.seed,check_data='6707')
        self.sd_tester.send_data_and_check(TA.TCAM,'2708000000','7f2736')
        time.sleep(9)
        self.sd_tester.send_data_and_check(TA.TCAM,'2707','7f2737')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x2711)_03会话下NRC35_36_37')
    def test_caseid_1981218(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,UnlockStep.seed,check_data='6711')
        self.sd_tester.send_data_and_check(TA.TCAM,'2712000000','7f2735')
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,UnlockStep.seed,check_data='6711')
        self.sd_tester.send_data_and_check(TA.TCAM,'2712000000','7f2736')
        time.sleep(9)
        self.sd_tester.send_data_and_check(TA.TCAM,'2711','7f2737')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x2701)_02会话下NRC35_36_37')
    def test_caseid_1981217(self):
        self.mix.init_boot_per()
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.PROGRAMMING,UnLock.L1,UnlockStep.seed,check_data='6701')
        self.sd_tester.send_data_and_check(TA.TCAM,'2702000000','7f2735')
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.PROGRAMMING,UnLock.L1,UnlockStep.seed,check_data='6701')
        self.sd_tester.send_data_and_check(TA.TCAM,'2702000000','7f2736')
        time.sleep(9)
        self.sd_tester.send_data_and_check(TA.TCAM,'2701','7f2737')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x2702)_02会话下NRC24')
    def test_caseid_1981216(self):
        self.mix.init_boot_per()
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'2702','7f2724')
    
    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x2706)_03会话下NRC24')
    def test_caseid_1981215(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'2706','7f2724')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x2708)_03会话下NRC24')
    def test_caseid_1981214(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'2708','7f2724')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x2712)_03会话下NRC24')
    def test_caseid_1981213(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'2712','7f2724')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x2701)_01会话下NRC7F')
    def test_caseid_1981212(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'2701','7f277f')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x2705)_01会话下NRC7F')
    def test_caseid_1981211(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'2705','7f277f')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x2707)_01会话下NRC7F')
    def test_caseid_1981210(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'2707','7f277f')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x2711)_01会话下NRC7F')
    def test_caseid_1981209(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'2711','7f277f')
    
    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_Tester present(0x3E00)_02会话下')
    def test_caseid_1981208(self):
        flag = True
        try:
            self.sd_tester.sd_tester.stop_tester_present() #暂停3E80
            self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
            self.sd_tester.send_data_and_check(TA.TCAM,'3e00','7e00')
            # t1 = time.time() #记录当前时间
            time.sleep(16) 
            self.sd_tester.read_did_and_check(TA.TCAM,0xf186,SESSION.EMPTY,'62f18602')
            self.sd_tester.send_data_and_check(TA.TCAM,'3e00','7e00')
            logger.info('等17s')
            time.sleep(17)
            self.sd_tester.read_did_and_check(TA.TCAM,0xf186,SESSION.EMPTY,'62f18601')
        except Exception as e:
            logger.warning(f'error:{e}')
            flag = False
        finally:
            self.sd_tester.sd_tester.tester_present() #打开3E80
        assert flag
    
    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_Tester present(0x3E00)_03会话下')
    def test_caseid_1981207(self):
        flag = True
        try:
            self.sd_tester.sd_tester.stop_tester_present() #暂停3E80
            self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
            self.sd_tester.send_data_and_check(TA.TCAM,'3e00','7e00')
            # t1 = time.time() #记录当前时间
            time.sleep(16) 
            self.sd_tester.read_did_and_check(TA.TCAM,0xf186,SESSION.EMPTY,'62f18603')
            self.sd_tester.send_data_and_check(TA.TCAM,'3e00','7e00')
            logger.info('等17s')
            time.sleep(17)
            self.sd_tester.read_did_and_check(TA.TCAM,0xf186,SESSION.EMPTY,'62f18601')
        except Exception as e:
            logger.warning(f'error:{e}')
            flag = False
        finally:
            self.sd_tester.sd_tester.tester_present() #打开3E80
        assert flag

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_Tester present(0x3E80)_02会话下')
    def test_caseid_1981206(self):
        flag = True
        try:
            self.sd_tester.sd_tester.stop_tester_present() #暂停3E80
            self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
            self.sd_tester.update_serverdoipid(0X1011)
            self.sd_tester.send_data([0X3e,0x80])
            # t1 = time.time() #记录当前时间
            time.sleep(16) 
            self.sd_tester.read_did_and_check(TA.TCAM,0xf186,SESSION.EMPTY,'62f18602')
            self.sd_tester.update_serverdoipid(0X1011)
            self.sd_tester.send_data([0X3e,0x80])
            logger.info('等17s')
            time.sleep(17)
            self.sd_tester.read_did_and_check(TA.TCAM,0xf186,SESSION.EMPTY,'62f18601')
        except Exception as e:
            logger.warning(f'error:{e}')
            flag = False
        finally:
            self.sd_tester.sd_tester.tester_present() #打开3E80
        assert flag

    
    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_Tester present(0x3E80)_03会话下')
    def test_caseid_1981205(self):
        flag = True
        try:
            self.sd_tester.sd_tester.stop_tester_present() #暂停3E80
            self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
            self.sd_tester.update_serverdoipid(0X1011)
            self.sd_tester.send_data([0X3e,0x80])
            # t1 = time.time() #记录当前时间
            time.sleep(16) 
            self.sd_tester.read_did_and_check(TA.TCAM,0xf186,SESSION.EMPTY,'62f18603')
            self.sd_tester.update_serverdoipid(0X1011)
            self.sd_tester.send_data([0X3e,0x80])
            logger.info('等17s')
            time.sleep(17)
            self.sd_tester.read_did_and_check(TA.TCAM,0xf186,SESSION.EMPTY,'62f18601')
        except Exception as e:
            logger.warning(f'error:{e}')
            flag = False
        finally:
            self.sd_tester.sd_tester.tester_present() #打开3E80
        assert flag

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_Tester present(0x3E00)_01会话下')
    def test_caseid_1981204(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'3e00','7e00')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_Tester present(0x3E80)_01会话下')
    def test_caseid_1981203(self):
        self.sd_tester.update_serverdoipid(0X1011)
        self.sd_tester.send_data([0X3e,0x80])
        

    
    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2800)_01会话下')
    # def test_caseid_1981202(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280001','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280002','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280003','7f287f')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')
        # 28服务不需要测试

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2800)_02会话下')
    # def test_caseid_1981201(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280001','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280002','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280003','7f287f')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')
    # 28服务不需要测试

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2800)_03会话下')
    # def test_caseid_1981200(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280001','6800')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280002','6800')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280003','6800')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2880)_01会话下')
    # def test_caseid_1981199(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288001','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288002','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288003','7f287f')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2880)_02会话下')
    # def test_caseid_1981198(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288001','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288002','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288003','7f287f')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2880)_03会话下')
    # def test_caseid_1981197(self):
    #     pass
        # data=self.sd_tester.communication_control_and_check(TA.TCAM,0x80,0x01)
        # data=self.sd_tester.communication_control_and_check(TA.TCAM,0x80,0x02)
        # data=self.sd_tester.communication_control_and_check(TA.TCAM,0x80,0x03)
        # assert data[0:2] != '7F','回复否定响应'F

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2801)_01会话下')
    # def test_caseid_1981196(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280101','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280102','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280103','7f287f')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2801)_02会话下')
    # def test_caseid_1981195(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280101','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280102','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280103','7f287f')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2801)_03会话下')
    # def test_caseid_1981194(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280101','6801')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280102','6801')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280103','6801')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2881)_01会话下')
    # def test_caseid_1981193(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288101','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288102','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288103','7f287f')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2881)_02会话下')
    # def test_caseid_1981192(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288101','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288102','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288103','7f287f')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2881)_03会话下')
    # def test_caseid_1981191(self):
    #     pass
        # data=self.sd_tester.communication_control_and_check(TA.TCAM,0x81,0x01)
        # data=self.sd_tester.communication_control_and_check(TA.TCAM,0x81,0x02)
        # data=self.sd_tester.communication_control_and_check(TA.TCAM,0x81,0x03)
        # assert data[0:2] != '7F','回复否定响应'

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2802)_01会话下')
    # def test_caseid_1981190(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280201','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280202','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280203','7f287f')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2802)_02会话下')
    # def test_caseid_1981189(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280201','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280202','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280203','7f287f')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2802)_03会话下')
    # def test_caseid_1981188(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280201','6802')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280202','6802')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280203','6802')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2882)_01会话下')
    # def test_caseid_1981187(self):
        # pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288201','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288202','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288203','7f287f')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2882)_02会话下')
    # def test_caseid_1981186(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288201','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288202','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288203','7f287f')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2882)_03会话下')
    # def test_caseid_1981185(self):
    #     pass
        # data=self.sd_tester.communication_control_and_check(TA.TCAM,0x82,0x01)
        # data=self.sd_tester.communication_control_and_check(TA.TCAM,0x82,0x02)
        # data=self.sd_tester.communication_control_and_check(TA.TCAM,0x82,0x03)
        # assert data[0:2] != '7F','回复否定响应'

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2803)_01会话下')
    # def test_caseid_1981184(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280301','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280302','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280303','7f287f')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2803)_02会话下')
    # def test_caseid_1981183(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280301','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280302','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280303','7f287f')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2803)_03会话下')
    # def test_caseid_1981182(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280301','6803')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280302','6803')
        # self.sd_tester.send_data_and_check(TA.TCAM,'280303','6803')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')
        # 28服务不需要测试

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2883)_01会话下')
    # def test_caseid_1981181(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288301','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288302','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288303','7f287f')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')
    # 28服务不需要测试

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2883)_02会话下')
    # def test_caseid_1981180(self):
    #     pass
        # self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288301','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288302','7f287f')
        # self.sd_tester.send_data_and_check(TA.TCAM,'288303','7f287f')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')
    # 28服务不需要测试

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2883)_03会话下')
    # def test_caseid_1981179(self):
    #     pass
        # data=self.sd_tester.communication_control_and_check(TA.TCAM,0x82,0x01)
        # data=self.sd_tester.communication_control_and_check(TA.TCAM,0x82,0x02)
        # data=self.sd_tester.communication_control_and_check(TA.TCAM,0x82,0x03)
        # assert data[0:2] != '7F','回复否定响应'
        # 28服务不需要测试

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2800x00)_03会话下')
    # def test_caseid_1981178(self):
    #     pass
        # self.sd_tester.communication_control_and_check(TA.TCAM,0x00,0x01,SESSION.EXTENDED,UnLock.L0,'6800')
        # captured_msgdata1= self.bus_comm.recv_pdu("connectivitycanfd",0x591,timeout=5)
        # captured_msgdata2= self.bus_comm.recv_pdu("connectivitycanfd",0x165,timeout=5)
        # assert captured_msgdata1 != None  and  captured_msgdata2 != None ,f'TCAM Tx网络管理报文已禁能 or Tx应用报文已禁能 报文:{captured_msgdata1} {captured_msgdata2}' 

        # self.sd_tester.communication_control_and_check(TA.TCAM,0x00,0x02,SESSION.EXTENDED,UnLock.L0,'6800')
        # captured_msgdata1= self.bus_comm.recv_pdu("connectivitycanfd",0x591,timeout=5)
        # captured_msgdata2= self.bus_comm.recv_pdu("connectivitycanfd",0x165,timeout=5)
        # assert captured_msgdata1 != None  and  captured_msgdata2 != None ,f'TCAM Tx网络管理报文已禁能 or Tx应用报文已禁能 报文:{captured_msgdata1} {captured_msgdata2}' 

        # self.sd_tester.communication_control_and_check(TA.TCAM,0x00,0x03,SESSION.EXTENDED,UnLock.L0,'6800')
        # captured_msgdata1= self.bus_comm.recv_pdu("connectivitycanfd",0x591,timeout=5)
        # captured_msgdata2= self.bus_comm.recv_pdu("connectivitycanfd",0x165,timeout=5)
        # assert captured_msgdata1 != None  and  captured_msgdata2 != None ,f'TCAM Tx网络管理报文已禁能 or Tx应用报文已禁能 报文:{captured_msgdata1} {captured_msgdata2}' 
        # 28服务不需要测试


    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2801x00)_03会话下')
    # def test_caseid_1981177(self):
        # self.sd_tester.communication_control_and_check(TA.TCAM,0x01,0x01,SESSION.EXTENDED,UnLock.L0,'6801')
        # captured_msgdata1 = self.bus_comm.recv_pdu("connectivitycanfd",0x591,timeout=5)
        # captured_msgdata2 = self.bus_comm.recv_pdu("connectivitycanfd",0x165,timeout=5)
        # assert captured_msgdata1 != None  and  captured_msgdata2 = None ,f'TCAM Tx网络管理报文已禁能 or Tx应用报文已禁能 报文:{captured_msgdata1} {captured_msgdata2}' 

        # self.sd_tester.communication_control_and_check(TA.TCAM,0x01,0x02,SESSION.EXTENDED,UnLock.L0,'6801')
        # captured_msgdata1= self.bus_comm.recv_pdu("connectivitycanfd",0x591,timeout=5)
        # captured_msgdata2= self.bus_comm.recv_pdu("connectivitycanfd",0x165,timeout=5)
        # assert captured_msgdata1 = None  and  captured_msgdata2 != None ,f'TCAM Tx网络管理报文已禁能 or Tx应用报文已禁能 报文:{captured_msgdata1} {captured_msgdata2}' 

        # self.sd_tester.communication_control_and_check(TA.TCAM,0x01,0x02,SESSION.EXTENDED,UnLock.L0,'6801')
        # captured_msgdata1= self.bus_comm.recv_pdu("connectivitycanfd",0x591,timeout=5)
        # captured_msgdata2= self.bus_comm.recv_pdu("connectivitycanfd",0x165,timeout=5)
        # assert captured_msgdata1 = None  and  captured_msgdata2 = None ,f'TCAM Tx网络管理报文已禁能 or Tx应用报文已禁能 报文:{captured_msgdata1} {captured_msgdata2}' 
        # pass
    # 28服务不需要测试

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2802x00)_03会话下')
    # def test_caseid_1981176(self):
        # try:
        #     with allure.step('关闭KL15'):
        #         logger.info('关闭KL15')
        #     self.sd_tester.communication_control_and_check(TA.TCAM,0x02,0x02,SESSION.EXTENDED,UnLock.L0,'6802')
        #     self.sd_tester.stop_sd_tester()
        #     time.sleep(180)
        #     check_data=self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT)
        #     assert check_data[0:4]=='5001',f'TCAM 未休眠 返回值:{check_data}' 
        # except Exception as e:
        #     asssert False,f'ERROR:{e}'
        # finally:
        #      with allure.step('打开KL15'):
        #         logger.info('打开KL15')
        # pass
    # 28服务不需要测试

            
    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2803x00)_03会话下')
    # def test_caseid_1981175(self):
    #     pass
    # 28服务不需要测试

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2880x00)_03会话下')
    # def test_caseid_1981174(self):
    #     pass
    # 28服务不需要测试

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2881x00)_03会话下')
    # def test_caseid_1981173(self):
    #     pass
    # 28服务不需要测试

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2882x00)_03会话下')
    # def test_caseid_1981172(self):
    #     pass
    # 28服务不需要测试

    # @allure.story('诊断服务')
    # @allure.title('UDS_Communication Control(0x2883x00)_03会话下')
    # def test_caseid_1981171(self):
    #     pass
    # 28服务不需要测试

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ControlDTCSetting(0x8501)_DtcMonitoringFunctionIsOn_01会话下')
    def test_caseid_1981170(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'8501','7f857f')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ControlDTCSetting(0x8502)_DtcMonitoringFunctionIsOff_01会话下')
    def test_caseid_1981169(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'8502','7f857f')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ControlDTCSetting(0x8501)_DtcMonitoringFunctionIsOn_02')
    def test_caseid_1981168(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'8501','7f857f')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ControlDTCSetting(0x8502)_DtcMonitoringFunctionIsOff_02')
    def test_caseid_1981167(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'8502','7f857f')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ControlDTCSetting(0x8501)_DtcMonitoringFunctionIsOn_03')
    def test_caseid_1981166(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'8501','c501')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ControlDTCSetting(0x8502)_DtcMonitoringFunctionIsOff_03')
    def test_caseid_1981165(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'8502','c502')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level5_03会话下其他安全请求切换')
    def test_caseid_1981162(self):
        seed=self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L5,UnlockStep.seed)[4:]
        key=self.sd_tester.caculate_key(TA.TCAM,UnLock.L5,seed)
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,UnlockStep.seed)
        self.sd_tester.send_data_and_check(TA.TCAM,[0x27,0x06]+key,'7f2724')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level7_03会话下其他安全请求切换')
    def test_caseid_1981161(self):
        seed=self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,UnlockStep.seed)[4:]
        key=self.sd_tester.caculate_key(TA.TCAM,UnLock.L7,seed)
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,UnlockStep.seed)
        self.sd_tester.send_data_and_check(TA.TCAM,[0x27,0x08]+key,'7f2724')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level11_03会话下其他安全请求切换')
    def test_caseid_1981160(self):
        seed=self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,UnlockStep.seed)[4:]
        key=self.sd_tester.caculate_key(TA.TCAM,UnLock.L11,seed)
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,UnlockStep.seed)
        self.sd_tester.send_data_and_check(TA.TCAM,[0x27,0x12]+key,'7f2724')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level1_02会话下其他安全请求切换')
    def test_caseid_1981159(self):
        self.sd_tester.update_serverdoipid(0x1011,"TCAM")
        self.sd_tester.send_request_and_recv_response([0x10,0x02],recv=[0x50,0x02])
        ret,data=self.sd_tester.send_request_and_recv_response([0x27, 0x01], recv=[0x67, 0x01])
        seed=bytes(data[2:]).hex()
        key = self.sd_tester.caculate_key(TA.TCAM, UnLock.L1, seed)
        self.sd_tester.send_request_and_recv_response([0x27, 0x35], recv=[0x7f, 0x27,0x12])
        self.sd_tester.send_request_and_recv_response([0x27, 0x02],msg1=key, recv='6702')


    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level1_02会话下相同会话切换切换')
    def test_caseid_1981158(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        self.sd_tester.send_data_and_check(TA.TCAM,'2701','6701000000')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level1_02会话下不同会话切换')
    def test_caseid_1981157(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')
        self.sd_tester.send_data_and_check(TA.TCAM,'2701','6701000000')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.PROGRAMMING,UnLock.L1,check_data='6702')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level5_03会话下相同会话切换')
    def test_caseid_1981156(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L5,check_data='6706')
        self.sd_tester.send_data_and_check(TA.TCAM,'2705','6705000000')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L5,check_data='6706')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level5_03会话下不同会话切换')
    def test_caseid_1981155(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L5,check_data='6706')
        self.sd_tester.send_data_and_check(TA.TCAM,'2705','6705000000')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L5,check_data='6706')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level7_03会话下相同会话切换')
    def test_caseid_1981154(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.send_data_and_check(TA.TCAM,'2707','670700000000000000000000000000000000')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.update_serverdoipid(0x1011)
        ret_code, ret_msg = self.sd_tester.send_request_and_recv_response([0x27,0x07])
        assert ret_msg[3:19] != [0] * 16 
       

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level7_03会话下不同会话切换')
    def test_caseid_1981153(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.send_data_and_check(TA.TCAM,'2707','6707000000')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.update_serverdoipid(0x1011)
        ret_code, ret_msg = self.sd_tester.send_request_and_recv_response([0x27,0x07])
        assert ret_msg[3:19] != [0] * 16 

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level11_03会话下相同会话切换')
    def test_caseid_1981152(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,check_data='6712')
        self.sd_tester.send_data_and_check(TA.TCAM,'2711','6711000000')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,check_data='6712')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level11_03会话下不同会话切换')
    def test_caseid_1981151(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,check_data='6712')
        self.sd_tester.send_data_and_check(TA.TCAM,'2711','6711000000')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,check_data='6712')


    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ClearDiagnosticInformation(0x14)_01会话下NRC13')
    def test_caseid_1981147(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'14FFFF','7f1413')
        self.sd_tester.send_data_and_check(TA.TCAM,'14FFFFFFFFFF','7f1413')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601') 

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ClearDiagnosticInformation(0x14)_01会话下NRC31')
    def test_caseid_1981146(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'14FFFF00','7f1431')
        self.sd_tester.send_data_and_check(TA.TCAM,'14FFFF11','7f1431')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ClearDiagnosticInformation(0x14)_03会话下NRC13')
    def test_caseid_1981145(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'14FFFF','7f1413')
        self.sd_tester.send_data_and_check(TA.TCAM,'14FFFFFFFFFF','7f1413')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ClearDiagnosticInformation(0x14)_03会话下NRC31')
    def test_caseid_1981144(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'14FFFF00','7f1431')
        self.sd_tester.send_data_and_check(TA.TCAM,'14FFFF11','7f1431')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')


    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadAllSupportedDTC(0x1902)_02会话下')
    def test_caseid_1981140(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'190209','7f197f')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadAllSupportedDTC(0x1904)_02会话下')
    def test_caseid_1981139(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'1904D0611320','7f197f')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadAllSupportedDTC(0x190A)_02会话下')
    def test_caseid_1981138(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'190A','7f197f')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')


    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadAllSupportedDTC(0x19)_01会话下NRC12')
    def test_caseid_1981134(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'19AA','7f1912')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadAllSupportedDTC(0x19)_01会话下NRC13')
    def test_caseid_1981133(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'1902','7f1913')
        self.sd_tester.send_data_and_check(TA.TCAM,'19020900','7f1913')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadAllSupportedDTC(0x19)_03会话下NRC12')
    def test_caseid_1981132(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'19AA','7f1912')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadAllSupportedDTC(0x19)_03会话下NRC13')
    def test_caseid_1981131(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'1902','7f1913')
        self.sd_tester.send_data_and_check(TA.TCAM,'19020900','7f1913')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')
    
    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_RequestDownload(0x3400)_在01会话下')
    def test_caseid_1981130(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'340044000000000AA8A810','7f347f')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')



    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_RequestDownload(0x3400)_在03会话下')
    def test_caseid_1981128(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'340044000000000AA8A810','7f347f')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')



    
    


    # @allure.story('诊断服务')
    # @allure.title('不同诊断会话切换时0x28诊断功能变化')
    # def test_caseid_1981120(self):
    #     pass
    # 28服务不需要测



    # @allure.story('诊断服务')
    # @allure.title('同诊断会话切换时0x28诊断功能变化')
    # def test_caseid_1981118(self):
    #     pass
    # 28服务不需要测

    # @allure.story('诊断服务')
    # @allure.title('11复位时0x28诊断功能变化')
    # def test_caseid_1981116(self):
    #     pass
    # 28服务不需要测


    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('不同诊断会话切换对写入的非易失性内存数据的影响')
    def test_caseid_1981114(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,check_data='6712')
        data=self.sd_tester.read_did_and_check(TA.TCAM,0x408F,SESSION.EMPTY,'62408f')[6:]
        self.sd_tester.write_did_and_check(TA.TCAM,0x408F,SESSION.EMPTY,UnLock.L0,'50555555555555555555555555555555','62408f50555555555555555555555555555555',check_method=Check_Method.read,recover=False)
        self.sd_tester.send_data_and_check(TA.TCAM,'1001','5001')
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,check_data='6712')
        self.sd_tester.read_did_and_check(TA.TCAM,0x408F,SESSION.EMPTY,'62408f50555555555555555555555555555555')
        self.sd_tester.write_did_and_check(TA.TCAM,0x408F,SESSION.EMPTY,UnLock.L0,data,f'62408f{data}',check_method=Check_Method.read,recover=False)



    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22408F_03会话下')
    def test_caseid_1986611(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0x408F,SESSION.EXTENDED,'7f2233')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2E408F_03会话下')
    def test_caseid_1986610(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0x408F,SESSION.EXTENDED,UnLock.L0,'55555555555555555555555555550055','7f2e33',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2E408F_03会话下-长度不对')
    def test_caseid_1986609(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,check_data='6712')
        self.sd_tester.write_did_and_check(TA.TCAM,0x408F,SESSION.EMPTY,UnLock.L0,'555555555555555555555555555555','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0x408F,SESSION.EMPTY,UnLock.L0,' 5555555555555555555555555555555555','7f2e13',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED902_01会话下-长度不对')
    def test_caseid_1986608(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD902,SESSION.DEFAULT,UnLock.L0,'03','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD902,SESSION.EMPTY,UnLock.L0,'030303','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD902,SESSION.EMPTY,UnLock.L0,'1500','6ed902',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD902,SESSION.EMPTY,UnLock.L0,'0015','6ed902',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD902,SESSION.EMPTY,UnLock.L0,'1515','6ed902',check_method=Check_Method.response,recover=False)
        # 错误的值应该回复NRC31，但是回复正响应，偏差接受了，SOA-21811

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED902_03会话下-长度不对')
    def test_caseid_1986607(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD902,SESSION.EXTENDED,UnLock.L0,'03','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD902,SESSION.EMPTY,UnLock.L0,'030303','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD902,SESSION.EMPTY,UnLock.L0,'1500','6ed902',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD902,SESSION.EMPTY,UnLock.L0,'0015','6ed902',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD902,SESSION.EMPTY,UnLock.L0,'1515','6ed902',check_method=Check_Method.response,recover=False)
        # 错误的值应该回复NRC31，但是回复正响应，偏差接受了，SOA-21811

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED903_01会话下-长度不对')
    def test_caseid_1986606(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD903,SESSION.DEFAULT,UnLock.L0,'000008','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD903,SESSION.EMPTY,UnLock.L0,'0000000008','7f2e13',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED903_03会话下-长度不对')
    def test_caseid_1986605(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD903,SESSION.EXTENDED,UnLock.L0,'000008','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD903,SESSION.EMPTY,UnLock.L0,'0000000008','7f2e13',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED904_01会话下-长度不对')
    def test_caseid_1986604(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD904,SESSION.DEFAULT,UnLock.L0,'000008','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD904,SESSION.EMPTY,UnLock.L0,'0000000008','7f2e13',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED904_03会话下-长度不对')
    def test_caseid_1986603(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD904,SESSION.EXTENDED,UnLock.L0,'000008','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD904,SESSION.EMPTY,UnLock.L0,'0000000008','7f2e13',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED905_01会话下-长度不对')
    def test_caseid_1986602(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD905,SESSION.DEFAULT,UnLock.L0,'000008','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD905,SESSION.EMPTY,UnLock.L0,'0000000008','7f2e13',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED905_03会话下-长度不对')
    def test_caseid_1986601(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD905,SESSION.EXTENDED,UnLock.L0,'000008','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD905,SESSION.EMPTY,UnLock.L0,'0000000008','7f2e13',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED906_01会话下-长度不对')
    def test_caseid_1986600(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD906,SESSION.DEFAULT,UnLock.L0,'000008','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD906,SESSION.EMPTY,UnLock.L0,'0000000008','7f2e13',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED906_03会话下-长度不对')
    def test_caseid_1986599(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD906,SESSION.EXTENDED,UnLock.L0,'000008','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD906,SESSION.EMPTY,UnLock.L0,'0000000008','7f2e13',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED907_01会话下-长度不对')
    def test_caseid_1986598(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD907,SESSION.DEFAULT,UnLock.L0,'000008','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD907,SESSION.EMPTY,UnLock.L0,'0000000008','7f2e13',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED907_03会话下-长度不对')
    def test_caseid_1986597(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD907,SESSION.EXTENDED,UnLock.L0,'000008','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD907,SESSION.EMPTY,UnLock.L0,'0000000008','7f2e13',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED916_L5_03会话下-长度不对')
    def test_caseid_1986596(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD916,SESSION.EXTENDED,UnLock.L5,'101010','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD916,SESSION.EMPTY,UnLock.L5,'1010101111','7f2e13',check_method=Check_Method.response,recover=False)
    
    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2EB163_L7_03会话下-长度不对')
    def test_caseid_1986593(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,constant=self.tcam_l7,check_data='6708')
        self.sd_tester.write_did_and_check(TA.TCAM,0xB163,SESSION.EMPTY,UnLock.L0,'112233445566778811223344556677','7f2e13',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xB163,SESSION.EMPTY,UnLock.L0,'1122334455667788112233445566778899','7f2e13',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED12F_03会话下')
    def test_caseid_1986592(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD12F,SESSION.EXTENDED,UnLock.L0,'FFFFFFFFEE','7f2e33',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D12F_03会话下')
    def test_caseid_1986591(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD12F,SESSION.EXTENDED,'7f2233')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22B163_03会话下')
    def test_caseid_1986590(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xB163,SESSION.EXTENDED,'7f2233')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2EB163_03会话下')
    def test_caseid_1986589(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xB163,SESSION.EXTENDED,UnLock.L0,'11223344556677881122334455667788','7f2e33',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED916_03会话下')
    def test_caseid_1986588(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD916,SESSION.EXTENDED,UnLock.L0,'10101011','7f2e33',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadAllSupportedDTC(0x19)_01会话下NRC31')
    def test_caseid_1986587(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005601','7f1931')
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005611','7f1931')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadAllSupportedDTC(0x19)_03会话下NRC31')
    def test_caseid_1986586(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005601','7f1931')
        self.sd_tester.send_data_and_check(TA.TCAM,'1904e3005611','7f1931')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_01会话下NRC13')
    def test_caseid_1986585(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'22','7f2213')
        self.sd_tester.send_data_and_check(TA.TCAM,'22f1','7f2213')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_02会话下NRC13')
    def test_caseid_1986584(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'22','7f2213')
        self.sd_tester.send_data_and_check(TA.TCAM,'22f1','7f2213')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_03会话下NRC13')
    def test_caseid_1986583(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'22','7f2213')
        self.sd_tester.send_data_and_check(TA.TCAM,'22f1','7f2213')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_01会话下NRC31')
    def test_caseid_1986582(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'22ffff','7f2231')
        self.sd_tester.send_data_and_check(TA.TCAM,'220000','7f2231')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_02会话下NRC31')
    def test_caseid_1986581(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'22ffff','7f2231')
        self.sd_tester.send_data_and_check(TA.TCAM,'220000','7f2231')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_03会话下NRC31')
    def test_caseid_1986580(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'22ffff','7f2231')
        self.sd_tester.send_data_and_check(TA.TCAM,'220000','7f2231')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_03会话下NRC33')
    def test_caseid_1986579(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'22b163','7f2233')
        self.sd_tester.send_data_and_check(TA.TCAM,'22408f','7f2233')
        self.sd_tester.send_data_and_check(TA.TCAM,'22d12f','7f2233')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_01会话下NRC13')
    def test_caseid_1986578(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'2ed90201','7f2e13')
        self.sd_tester.send_data_and_check(TA.TCAM,'2ed902010203','7f2e13')
        self.sd_tester.send_data_and_check(TA.TCAM,'2ed9ba303030303030303030','7f2e13')
        self.sd_tester.send_data_and_check(TA.TCAM,'2ed9ba3030303030303030303030','7f2e13')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_03会话下NRC13')
    def test_caseid_1986576(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'2ed90201','7f2e13')
        self.sd_tester.send_data_and_check(TA.TCAM,'2ed902010203','7f2e13')
        self.sd_tester.send_data_and_check(TA.TCAM,'2ed9ba303030303030303030','7f2e13')
        self.sd_tester.send_data_and_check(TA.TCAM,'2ed9ba3030303030303030303030','7f2e13')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_01会话下NRC31')
    def test_caseid_1986575(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'2E000000','7f2e31')
        self.sd_tester.send_data_and_check(TA.TCAM,'2EFFFFFFFF','7f2e31')
        self.sd_tester.send_data_and_check(TA.TCAM,'2EFFFFFFFFFF','7f2e31')
        self.sd_tester.send_data_and_check(TA.TCAM,'2E000000000000','7f2e31')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18601')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_02会话下NRC31')
    def test_caseid_1986574(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'2E000000','7f2e31')
        self.sd_tester.send_data_and_check(TA.TCAM,'2EFFFFFFFF','7f2e31')
        self.sd_tester.send_data_and_check(TA.TCAM,'2EFFFFFFFFFF','7f2e31')
        self.sd_tester.send_data_and_check(TA.TCAM,'2E000000000000','7f2e31')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18602')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_03会话下NRC31')
    def test_caseid_1986573(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'2E000000','7f2e31')
        self.sd_tester.send_data_and_check(TA.TCAM,'2EFFFFFFFF','7f2e31')
        self.sd_tester.send_data_and_check(TA.TCAM,'2EFFFFFFFFFF','7f2e31')
        self.sd_tester.send_data_and_check(TA.TCAM,'2E000000000000','7f2e31')
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EMPTY,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_03会话下NRC33')
    def test_caseid_1986572(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0x408F,SESSION.EXTENDED,UnLock.L0,'50555555555555555555555555555555','7f2e33',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0x408F,SESSION.EMPTY,UnLock.L0,'10101011','7f2e33',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x2705)_03会话下NRC35_36_37_超时')
    def test_caseid_1986571(self):
        self.mix.init_boot_per()
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L5,UnlockStep.seed,check_data='6705')
        self.sd_tester.send_data_and_check(TA.TCAM,'2706000000','7f2735')
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L5,UnlockStep.seed,check_data='6705')
        self.sd_tester.send_data_and_check(TA.TCAM,'2706000000','7f2736')
        time.sleep(11)
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L5,UnlockStep.seed,check_data='6705')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x2707)_03会话下NRC35_36_37超时')
    def test_caseid_1986570(self):
        self.mix.init_boot_per()
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,UnlockStep.seed,check_data='6707')
        self.sd_tester.send_data_and_check(TA.TCAM,'270800000000000000000000000000000000','7f2735')
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,UnlockStep.seed,check_data='6707')
        self.sd_tester.send_data_and_check(TA.TCAM,'2708000000','7f2736')
        time.sleep(11)
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,UnlockStep.seed,check_data='6707')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x2711)_03会话下NRC35_36_37超时')
    def test_caseid_1986569(self):
        self.mix.init_boot_per()
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,UnlockStep.seed,check_data='6711')
        self.sd_tester.send_data_and_check(TA.TCAM,'2712000000','7f2735')
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,UnlockStep.seed,check_data='6711')
        self.sd_tester.send_data_and_check(TA.TCAM,'2712000000','7f2736')
        time.sleep(11)
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,UnlockStep.seed,check_data='6711')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x2701)_02会话下NRC35_36_37超时')
    def test_caseid_1986568(self):
        self.mix.init_boot_per()
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.PROGRAMMING,UnLock.L1,UnlockStep.seed,check_data='6701')
        self.sd_tester.send_data_and_check(TA.TCAM,'2702000000','7f2735')
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.PROGRAMMING,UnLock.L1,UnlockStep.seed,check_data='6701')
        self.sd_tester.send_data_and_check(TA.TCAM,'2702000000','7f2736')
        time.sleep(11)
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.PROGRAMMING,UnLock.L1,UnlockStep.seed,check_data='6701')




    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ControlDTCSetting(0x8502)_DtcMonitoringFunctionIsOff_03功能测试')
    def test_caseid_1981164(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'190405151320','590405151309')
        self.sd_tester.send_data_and_check(TA.TCAM,'8502','c502')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        time.sleep(20)
        self.sd_tester.send_data_and_check(TA.TCAM,'190405151320','590405151300')
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'1103','5103')
        time.sleep(210)
        self.sd_tester.send_data_and_check(TA.TCAM,'1001','5001')
        

    # @pytest.mark.full
    # @allure.story('诊断服务')
    # @allure.title('UDS_ControlDTCSetting(0x8501)_DtcMonitoringFunctionIsOn_03功能测试')
    # def test_caseid_1981163(self):
    #     self.sd_tester.send_data_and_check(TA.TCAM,'190209','590209')
    #     self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
    #     self.sd_tester.send_data_and_check(TA.TCAM,'190405151320','590405151309')
    #     self.sd_tester.send_data_and_check(TA.TCAM,'8502','c502')
    #     self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
    #     time.sleep(10)
    #     self.sd_tester.send_data_and_check(TA.TCAM,'190405151320','590405151300')
    #     self.sd_tester.send_data_and_check(TA.TCAM,'22f186','62f18603')
    #     self.sd_tester.send_data_and_check(TA.TCAM,'8501','c501')
    #     time.sleep(10)
    #     self.sd_tester.send_data_and_check(TA.TCAM,'190405151320','590405151309')
    




    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ClearDiagnosticInformation(0x14)_01会话下')
    def test_caseid_1981150(self):
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        self.sd_tester.send_data_and_check(TA.TCAM,'190209','590209')
        

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ClearDiagnosticInformation(0x14)_02会话下')
    def test_caseid_1981149(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','7f147f')
        
    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ClearDiagnosticInformation(0x14)_03会话下')
    def test_caseid_1981148(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'14ffffff','54')
        self.sd_tester.send_data_and_check(TA.TCAM,'190209','590209')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadAllSupportedDTC(0x1902)_01会话下')
    def test_caseid_1981143(self):
        time.sleep(30)
        ret_code, ret_msg = self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0x09], recv=[0x59, 0x02, 0x09])
        assert len(ret_msg) >= 7, " 有DTC"

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadAllSupportedDTC(0x1904)_01会话下')
    def test_caseid_1981142(self):
        time.sleep(30)
        self.sd_tester.send_data_and_check(TA.TCAM,'190405151320','590405151309')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadAllSupportedDTC(0x190A)_01会话下')
    def test_caseid_1981141(self):
        check_dtc=['051511', '051512', '051513', '454600', '916F2F', '92EA04', '978B11', '978B12', '978B13', '978D11', '978D12', '978D95', '9D7911', '9D7912', '9D7913', 'D00200', 'D02A88', 'D03600', 'D06111', 'D06112', 'D06113', 'D06211', 'D06212', 'D06213', 'D06311', 'D06312', 'D06313', 'D06411', 'D06412', 'D06413', 'D07011', 'D07012', 'D07013', 'D0B000', 'D0B151', 'D0B211', 'D0B215', 'D0B286', 'E10912', 'E10914', 'E10962', 'E30055', 'E30056', 'E40057', 'EE0368', 'EE0468', 'EF874A','D06E11','D06E12','D06E13','D06E14']
        self.sd_tester.update_serverdoipid(0x1011)
        ret_code, ret_msg = self.sd_tester.send_request_and_recv_response([0x19,0x0a])
        data_lis = bytes(ret_msg[3:]).hex().upper()
        dtc_data_list = [data_lis[i:i + 8][:6] for i in range(0, len(data_lis), 8)]
        dtc_data_list=list(set(dtc_data_list))
        logger.info(f"DTC 个数{len(dtc_data_list)}个 {dtc_data_list}")
        assert len(dtc_data_list) == len(check_dtc), f"dtc 个数不是{len(check_dtc)}个"
        err_dtc = [item for item in dtc_data_list if item not in check_dtc]
        logger.info(f"未知 DTC 个数{len(err_dtc)}个 {err_dtc}")
        assert not len(err_dtc),f"存在未知DTC {err_dtc }"

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadAllSupportedDTC(0x1902)_03会话下')
    def test_caseid_1981137(self):
        self.sd_tester.send_data_and_check(TA.TCAM,'190209','590209')
    

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadAllSupportedDTC(0x1904)_03会话下')
    def test_caseid_1981136(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'190405151320','590405151309')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadAllSupportedDTC(0x190A)_03会话下')
    def test_caseid_1981135(self):
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        check_dtc=['051511', '051512', '051513', '454600', '916F2F', '92EA04', '978B11', '978B12', '978B13', '978D11', '978D12', '978D95', '9D7911', '9D7912', '9D7913', 'D00200', 'D02A88', 'D03600', 'D06111', 'D06112', 'D06113', 'D06211', 'D06212', 'D06213', 'D06311', 'D06312', 'D06313', 'D06411', 'D06412', 'D06413', 'D07011', 'D07012', 'D07013', 'D0B000', 'D0B151', 'D0B211', 'D0B215', 'D0B286', 'E10912', 'E10914', 'E10962', 'E30055', 'E30056', 'E40057', 'EE0368', 'EE0468', 'EF874A','D06E11','D06E12','D06E13','D06E14']
        self.sd_tester.update_serverdoipid(0x1011)
        ret_code, ret_msg = self.sd_tester.send_request_and_recv_response([0x19,0x0a])
        data_lis = bytes(ret_msg[3:]).hex().upper()
        dtc_data_list = [data_lis[i:i + 8][:6] for i in range(0, len(data_lis), 8)]
        dtc_data_list=list(set(dtc_data_list))
        logger.info(f"DTC 个数{len(dtc_data_list)}个 {dtc_data_list}")
        assert len(dtc_data_list) == len(check_dtc), f"dtc 个数不是{len(check_dtc)}个"
        err_dtc = [item for item in dtc_data_list if item not in check_dtc]
        logger.info(f"未知 DTC 个数{len(err_dtc)}个 {err_dtc}")
        assert not len(err_dtc),f"存在未知DTC {err_dtc }"


    # @pytest.mark.full
    # @allure.story('诊断服务')
    # @allure.title('不同诊断会话切换时0x85诊断功能变化')
    # def test_caseid_1981119(self):
    #     self.sd_tester.update_serverdoipid(0x1011)
    #     self.sd_tester.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])
    #     self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86], recv=[0x62, 0xf1, 0x86, 0x03])
    #     ret_code, ret_msg = self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0x09], recv=[0x59, 0x02, 0x09])
    #     assert len(ret_msg) >= 7, " 有DTC"
    #     self.sd_tester.send_request_and_recv_response([0x85, 0x02], recv=[0xC5, 0x02])
    #     sleep(3)
    #     self.sd_tester.send_request_and_recv_response([0x14, 0xFF, 0xFF,0xFF], recv=[0x54])
    #     sleep(10)
    #     ret_code, ret_msg = self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0x09], recv=[0x59, 0x02, 0x09])
    #     assert len(ret_msg) == 3, " 没有DTC"
    #     sleep(3)
    #     self.sd_tester.send_request_and_recv_response([0x10, 0x01], recv=[0x50, 0x01])
    #     # self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86], recv=[0x62, 0xf1, 0x86, 0x01])
    #     sleep(10)
    #     ret_code, ret_msg = self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0x09], recv=[0x59, 0x02, 0x09])
    #     assert len(ret_msg) >= 7, " 有DTC"


    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('相同诊断会话切换时0x85诊断功能变化')
    def test_caseid_1981117(self):
        self.sd_tester.update_serverdoipid(0x1011)
        self.sd_tester.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])
        self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86], recv=[0x62, 0xf1, 0x86, 0x03])
        ret_code, ret_msg = self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0x09], recv=[0x59, 0x02, 0x09])
        assert len(ret_msg) >= 7, "有DTC"
        self.sd_tester.send_request_and_recv_response([0x85, 0x02], recv=[0xC5, 0x02])
        self.sd_tester.send_request_and_recv_response([0x14, 0xFF, 0xFF,0xFF], recv=[0x54])
        sleep(10)
        ret_code, ret_msg = self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0x09], recv=[0x59, 0x02, 0x09])
        assert len(ret_msg) == 3, "没有DTC"
        self.sd_tester.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])
        self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86], recv=[0x62, 0xf1, 0x86, 0x03])
        sleep(10)
        ret_code, ret_msg = self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0x09], recv=[0x59, 0x02, 0x09])
        assert len(ret_msg) == 3, "没有DTC"
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.EXTENDED,'62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'1103','5103')
        time.sleep(210)
        self.sd_tester.send_data_and_check(TA.TCAM,'1001','5001')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('11复位时0x85诊断功能变化')
    def test_caseid_1981115(self):
        self.sd_tester.update_serverdoipid(0x1011)
        self.sd_tester.send_request_and_recv_response([0x10, 0x03], recv=[0x50, 0x03])
        self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86], recv=[0x62, 0xf1, 0x86, 0x03])
        ret_code, ret_msg = self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0x09], recv=[0x59, 0x02, 0x09])
        assert len(ret_msg) >= 7, "有DTC"
        self.sd_tester.send_request_and_recv_response([0x85, 0x02], recv=[0xC5, 0x02])
        self.sd_tester.send_request_and_recv_response([0x14, 0xFF, 0xFF,0xFF], recv=[0x54])
        sleep(10)
        ret_code, ret_msg = self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0x09], recv=[0x59, 0x02, 0x09])
        assert len(ret_msg) == 3, "没有DTC"
        self.sd_tester.send_request_and_recv_response([0x11, 0x03], recv=[0x51, 0x03])
        time.sleep(180)
        ret_code, ret_msg = self.sd_tester.send_request_and_recv_response([0x19, 0x02, 0x09], recv=[0x59, 0x02, 0x09])
        assert len(ret_msg) >= 7, "有DTC"

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level11_03会话下 其他不存在子函数的安全请求切换')
    def test_caseid_1990916(self):
        seed=self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,UnlockStep.seed)[4:]
        key=self.sd_tester.caculate_key(TA.TCAM,UnLock.L11,seed)
        self.sd_tester.send_data_and_check(TA.TCAM,'2723','7f2712')
        self.sd_tester.send_data_and_check(TA.TCAM,[0x27,0x12]+key,'6712')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level7_03会话下 其他不存在子函数的安全请求切换')
    def test_caseid_1990915(self):
        seed=self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L7,UnlockStep.seed)[4:]
        key=self.sd_tester.caculate_key(TA.TCAM,UnLock.L7,seed)
        self.sd_tester.send_data_and_check(TA.TCAM,'2737','7f2712')
        self.sd_tester.send_data_and_check(TA.TCAM,[0x27,0x08]+key,'6708')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_SecurityAccess(0x27)_level5_03会话下 其他不存在子函数的安全请求切换')
    def test_caseid_1990914(self):
        seed=self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L5,UnlockStep.seed)[4:]
        key=self.sd_tester.caculate_key(TA.TCAM,UnLock.L5,seed)
        self.sd_tester.send_data_and_check(TA.TCAM,'2723','7f2712')
        self.sd_tester.send_data_and_check(TA.TCAM,[0x27,0x06]+key,'6706')

    @pytest.mark.repeat(50)
    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_会话切换压测')
    def test_caseid_1990206(self):
        self.sd_tester.send_data_and_check(TA.TCAM,'1003','5003')
        self.sd_tester.send_data_and_check(TA.TCAM,'22f186','62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'1001','5001')
        self.sd_tester.send_data_and_check(TA.TCAM,'22f186','62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'1002','5002')
        self.sd_tester.send_data_and_check(TA.TCAM,'22f186','62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'1001','5001')
        self.sd_tester.send_data_and_check(TA.TCAM,'22f186','62f18601')
        self.sd_tester.send_data_and_check(TA.TCAM,'1003','5003')
        self.sd_tester.send_data_and_check(TA.TCAM,'22f186','62f18603')
        self.sd_tester.send_data_and_check(TA.TCAM,'1002','5002')
        self.sd_tester.send_data_and_check(TA.TCAM,'22f186','62f18602')
        self.sd_tester.send_data_and_check(TA.TCAM,'1001','5001')
        self.sd_tester.send_data_and_check(TA.TCAM,'22f186','62f18601')


class TestDID(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self,ecu)
        with allure.step("初始化环境"):
            self.mix.init_boot_per()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,check_data='62f18601',check_length=8)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        with allure.step("初始化环境"):
            self.mix.init_boot_per()
        super().after_class(self, ecu)
    
    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F186_01会话下')
    def test_caseid_1981699(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.DEFAULT,'62f18601')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F186_02会话下')
    def test_caseid_1981698(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.PROGRAMMING,'62f18602')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F186_03会话下')
    def test_caseid_1981697(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF186,SESSION.EXTENDED,'62f18603')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F190_01会话下')
    def test_caseid_1981696(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF190,SESSION.DEFAULT,'62f190',check_length=40)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F190_02会话下')
    def test_caseid_1981695(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF190,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F190_03会话下')
    def test_caseid_1981694(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF190,SESSION.EXTENDED,'62f190',check_length=40)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1F0_01会话下')
    def test_caseid_1981693(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1F0,SESSION.DEFAULT,'62f1f0',check_length=24)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1F0_02会话下')
    def test_caseid_1981692(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1F0,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1F0_03会话下')
    def test_caseid_1981691(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1F0,SESSION.EXTENDED,'62f1f0',check_length=24)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1F1_01会话下')
    def test_caseid_1981690(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1F1,SESSION.DEFAULT,'62f1f1',check_length=24)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1F1_02会话下')
    def test_caseid_1981689(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1F1,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22F1F1_03会话下')
    def test_caseid_1981688(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xF1F1,SESSION.EXTENDED,'62f1f1',check_length=24)
    
    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D01C_01会话下')
    def test_caseid_1981687(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD01C,SESSION.DEFAULT,'7f2231')

    
    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D01C_02会话下')
    def test_caseid_1981686(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD01C,SESSION.PROGRAMMING,'62d01cc0e7686676d89205a740dee5a0e8e269ffca903a3c36ec1309a76825a6c54dc0')
        # data=self.sd_tester.read_did_and_check(TA.TCAM,0xD01C,SESSION.PROGRAMMING,'62d01c')[6:]
        # assert len(data) == 64 ,f'CRC长度不对 实际长度:{len(data)}'

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D01C_03会话下')
    def test_caseid_1981685(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD01C,SESSION.EXTENDED,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22DD00_01会话下')
    def test_caseid_1981684(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD00,SESSION.DEFAULT,'62dd00',check_range=[0,4294966800])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22DD00_02会话下')
    def test_caseid_1981683(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD00,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22DD00_03会话下')
    def test_caseid_1981682(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD00,SESSION.EXTENDED,'62dd00',check_range=[0,4294966800])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22DD01_01会话下')
    def test_caseid_1981681(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD01,SESSION.DEFAULT,'62dd01',check_range=[0,16777215])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22DD01_02会话下')
    def test_caseid_1981680(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD01,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22DD01_03会话下')
    def test_caseid_1981679(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD01,SESSION.EXTENDED,'62dd01',check_range=[0,16777215])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22DD02_01会话下')
    def test_caseid_1981678(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD02,SESSION.DEFAULT,'62dd02',check_range=[0,255])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22DD02_02会话下')
    def test_caseid_1981677(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD02,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22DD02_03会话下')
    def test_caseid_1981676(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD02,SESSION.EXTENDED,'62dd02',check_range=[0,255])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22DD0A_01会话下')
    def test_caseid_1981675(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.DEFAULT,'62dd0a',check_in=['00','01','03','0b','0d','ff'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22DD0A_02会话下')
    def test_caseid_1981674(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22DD0A_03会话下')
    def test_caseid_1981673(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0A,SESSION.EXTENDED,'62dd0a',check_in=['00','01','03','0b','0d','ff'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22DD0C_01会话下')
    def test_caseid_1981672(self):
        check_data_list=[hex(i)[2:] for i in range(48,95)] + [hex(i)[2:] for i in range(32,37)] + ['10','11','FF']
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0C,SESSION.DEFAULT,'62dd0c',check_in=check_data_list)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22DD0C_02会话下')
    def test_caseid_1981671(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0C,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22DD0C_03会话下')
    def test_caseid_1981670(self):
        check_data_list=[hex(i)[2:] for i in range(48,95)] + [hex(i)[2:] for i in range(32,37)] + ['10','11','FF']
        self.sd_tester.read_did_and_check(TA.TCAM,0xDD0C,SESSION.EXTENDED,'62dd0c',check_in=check_data_list)

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D005_01会话下')
    def test_caseid_1981669(self):
        p=self.sd_tester.read_did_and_check(TA.TCAM,0xD005,SESSION.DEFAULT,'62d005')
        assert 0 <= int(p[6:14],16) <= 429496729.38

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D005_02会话下')
    def test_caseid_1981668(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD005,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D005_03会话下')
    def test_caseid_1981667(self):
        p=self.sd_tester.read_did_and_check(TA.TCAM,0xD005,SESSION.EXTENDED,'62d005')
        assert 0 <= int(p[6:14],16) <= 429496729.38

    
    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D03A_01会话下')
    def test_caseid_1981666(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD03A,SESSION.DEFAULT,'62d03ac0e7686676d89205a740dee5a0e8e269ffca903a3c36ec1309a76825a6c54dc0')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xD03A,SESSION.DEFAULT,'62d03a',check_length=70)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D03A_02会话下')
    def test_caseid_1981665(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD03A,SESSION.PROGRAMMING,'7f2231')

    
    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D03A_03会话下')
    def test_caseid_1981664(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD03A,SESSION.EXTENDED,'62d03ac0e7686676d89205a740dee5a0e8e269ffca903a3c36ec1309a76825a6c54dc0')
        # self.sd_tester.read_did_and_check(TA.TCAM,0xD03A,SESSION.EXTENDED,'62d03a',check_length=70)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D09A_01会话下')
    def test_caseid_1981663(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD09A,SESSION.DEFAULT,'62d09a',check_in=['0','1'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D09A_02会话下')
    def test_caseid_1981662(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD09A,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D09A_03会话下')
    def test_caseid_1981661(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD09A,SESSION.EXTENDED,'62d09a',check_in=['0','1'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D0B5_01会话下')
    def test_caseid_1981660(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD0B5,SESSION.DEFAULT,'62d0b5',check_length=12)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D0B5_02会话下')
    def test_caseid_1981659(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD0B5,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D0B5_03会话下')
    def test_caseid_1981658(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD0B5,SESSION.EXTENDED,'62d0b5',check_length=12)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D110_01会话下')
    def test_caseid_1981657(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD110,SESSION.DEFAULT,'62d110',check_range=[0,6553.5])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D110_02会话下')
    def test_caseid_1981656(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD110,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D110_03会话下')
    def test_caseid_1981655(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD110,SESSION.EXTENDED,'62d110',check_range=[0,6553.5])

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D12F_01会话下')
    def test_caseid_1981654(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD12F,SESSION.DEFAULT,'7f2233')

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D12F_02会话下')
    def test_caseid_1981653(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD12F,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.smoke
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D12F_03会话下')
    def test_caseid_1981652(self):
        self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EXTENDED,UnLock.L11,check_data='6712')
        self.sd_tester.read_did_and_check(TA.TCAM,0xD12F,SESSION.EMPTY,'62d12f',check_length=16)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D134_01会话下')
    def test_caseid_1981651(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD134,SESSION.DEFAULT,'62d134',check_in=['00','01','02','03','05'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D134_02会话下')
    def test_caseid_1981650(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD134,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D134_03会话下')
    def test_caseid_1981649(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD134,SESSION.EXTENDED,'62d134',check_in=['00','01','02','03','05'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D230_01会话下')
    def test_caseid_1981648(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD230,SESSION.DEFAULT,'62d230')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D230_02会话下')
    def test_caseid_1981647(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD230,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D230_03会话下')
    def test_caseid_1981646(self): 
        self.sd_tester.read_did_and_check(TA.TCAM,0xD230,SESSION.EXTENDED,'62d230')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D235_01会话下')
    def test_caseid_1981645(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD235,SESSION.DEFAULT,'62d235',check_length=106)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D235_02会话下')
    def test_caseid_1981644(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD235,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D235_03会话下')
    def test_caseid_1981643(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD235,SESSION.EXTENDED,'62d235',check_length=106)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D240_01会话下') 
    def test_caseid_1981642(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD240,SESSION.DEFAULT,'62d240',check_length=14,check_range=[0,4294967295])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D240_02会话下')
    def test_caseid_1981641(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD240,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D240_03会话下')
    def test_caseid_1981640(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD240,SESSION.EXTENDED,'62d240',check_length=14,check_range=[0,4294967295])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D250_01会话下')
    def test_caseid_1981639(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD250,SESSION.DEFAULT,'62d250',check_in=['00','01'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D250_02会话下')
    def test_caseid_1981638(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD250,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D250_03会话下')
    def test_caseid_1981637(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD250,SESSION.EXTENDED,'62d250',check_in=['00','01'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D251_01会话下')
    def test_caseid_1981636(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD251,SESSION.DEFAULT,'62d251',check_range=[0X00,0Xff])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D251_02会话下')
    def test_caseid_1981635(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD251,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D251_03会话下')
    def test_caseid_1981634(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD251,SESSION.EXTENDED,'62d251',check_range=[0X00,0Xff])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D260_01会话下')
    def test_caseid_1981633(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD260,SESSION.DEFAULT,'62d260',check_length=8)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D260_02会话下')
    def test_caseid_1981632(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD260,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D260_03会话下')
    def test_caseid_1981631(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD260,SESSION.EXTENDED,'62d260',check_length=8)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D900_01会话下')
    def test_caseid_1981630(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD900,SESSION.DEFAULT,'62d900',check_in=['00','01','03'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D900_02会话下')
    def test_caseid_1981629(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD900,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D900_03会话下')
    def test_caseid_1981628(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD900,SESSION.EXTENDED,'62d900',check_in=['00','01','03'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D901_01会话下')
    def test_caseid_1981627(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD901,SESSION.DEFAULT,'62d901',check_in=['00','01','02','03','04','05'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D901_02会话下')
    def test_caseid_1981626(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD901,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D901_03会话下')
    def test_caseid_1981625(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD901,SESSION.EXTENDED,'62d901',check_in=['00','01','02','03','04','05'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D902_01会话下')
    def test_caseid_1981624(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD902,SESSION.DEFAULT,'62d902',check_length=10)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D902_02会话下')
    def test_caseid_1981623(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD902,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D902_03会话下')
    def test_caseid_1981622(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD902,SESSION.EXTENDED,'62d902',check_length=10)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED902_01会话下')
    def test_caseid_1981621(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD902,SESSION.DEFAULT,UnLock.L0,'0303','62d9020303',check_method=Check_Method.read)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED902_02会话下')
    def test_caseid_1981620(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD902,SESSION.PROGRAMMING,UnLock.L0,'0303','7f2e31',check_method=Check_Method.response,recover=False)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED902_03会话下')
    def test_caseid_1981619(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD902,SESSION.EXTENDED,UnLock.L0,'0300','62d902',check_method=Check_Method.read)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D903_01会话下')
    def test_caseid_1981618(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD903,SESSION.DEFAULT,'62d903',check_length=14)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D903_02会话下')
    def test_caseid_1981617(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD903,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D903_03会话下')
    def test_caseid_1981616(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD903,SESSION.EXTENDED,'62d903',check_length=14)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED903_01会话下')
    def test_caseid_1981615(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD903,SESSION.DEFAULT,UnLock.L0,'00000008','62d90300000008',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD903,SESSION.EMPTY,UnLock.L0,'00000020','62d90300000020',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD903,SESSION.EMPTY,UnLock.L0,'00000009','62d90300000009',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD903,SESSION.EMPTY,UnLock.L0,'00000011','62d90300000011',check_method=Check_Method.read)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED903_02会话下')
    def test_caseid_1981614(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD903,SESSION.PROGRAMMING,UnLock.L0,'00000007','7f2e31',check_method=Check_Method.response,recover=False)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED903_03会话下')
    def test_caseid_1981613(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD903,SESSION.EXTENDED,UnLock.L0,'00000009','62d90300000009',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD903,SESSION.EMPTY,UnLock.L0,'00000020','62d90300000020',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD903,SESSION.EMPTY,UnLock.L0,'00000009','62d90300000009',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD903,SESSION.EMPTY,UnLock.L0,'00000011','62d90300000011',check_method=Check_Method.read)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D904_01会话下')
    def test_caseid_1981612(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD904,SESSION.DEFAULT,'62d904',check_length=14)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D904_02会话下')
    def test_caseid_1981611(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD904,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D904_03会话下')
    def test_caseid_1981610(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD904,SESSION.EXTENDED,'62d904',check_length=14)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED904_01会话下')
    def test_caseid_1981609(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD904,SESSION.DEFAULT,UnLock.L0,'0000000a','62d9040000000a',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD904,SESSION.EMPTY,UnLock.L0,'00000003','62d90400000003',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD904,SESSION.EMPTY,UnLock.L0,'00000002','62d90400000002',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD904,SESSION.EMPTY,UnLock.L0,'00000011','62d90400000011',check_method=Check_Method.read)


    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED904_02会话下')
    def test_caseid_1981608(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD904,SESSION.PROGRAMMING,UnLock.L0,'0000000c','7f2e31',check_method=Check_Method.response,recover=False)

    @pytest.mark.sanity
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED904_03会话下')
    def test_caseid_1981607(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD904,SESSION.EXTENDED,UnLock.L0,'0000000b','62d9040000000b',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD904,SESSION.EMPTY,UnLock.L0,'00000003','62d90400000003',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD904,SESSION.EMPTY,UnLock.L0,'00000002','62d90400000002',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD904,SESSION.EMPTY,UnLock.L0,'00000011','62d90400000011',check_method=Check_Method.read)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D905_01会话下')
    def test_caseid_1981606(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD905,SESSION.DEFAULT,'62d905',check_length=14)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D905_02会话下')
    def test_caseid_1981605(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD905,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D905_03会话下')
    def test_caseid_1981604(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD905,SESSION.EXTENDED,'62d905',check_length=14)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED905_01会话下')
    def test_caseid_1981603(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD905,SESSION.DEFAULT,UnLock.L0,'0000005a','62d9050000005a',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD905,SESSION.EMPTY,UnLock.L0,'00000021','62d90500000021',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD905,SESSION.EMPTY,UnLock.L0,'00000011','62d90500000011',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD905,SESSION.EMPTY,UnLock.L0,'00000008','62d90500000008',check_method=Check_Method.read)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED905_02会话下')
    def test_caseid_1981602(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD905,SESSION.PROGRAMMING,UnLock.L0,'0000003b','7f2e31',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED905_03会话下')
    def test_caseid_1981601(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD905,SESSION.EXTENDED,UnLock.L0,'0000003c','62d9050000003c',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD905,SESSION.EMPTY,UnLock.L0,'00000021','62d90500000021',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD905,SESSION.EMPTY,UnLock.L0,'00000011','62d90500000011',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD905,SESSION.EMPTY,UnLock.L0,'00000008','62d90500000008',check_method=Check_Method.read)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D906_01会话下')
    def test_caseid_1981600(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD906,SESSION.DEFAULT,'62d906',check_length=14)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D906_02会话下')
    def test_caseid_1981599(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD906,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D906_03会话下')
    def test_caseid_1981598(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD906,SESSION.EXTENDED,'62d906',check_length=14)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED906_01会话下')
    def test_caseid_1981597(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD906,SESSION.DEFAULT,UnLock.L0,'00000004','62d90600000004',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD906,SESSION.EMPTY,UnLock.L0,'00000006','62d90600000006',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD906,SESSION.EMPTY,UnLock.L0,'00000032','62d90600000032',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD906,SESSION.EMPTY,UnLock.L0,'00000054','62d90600000054',check_method=Check_Method.read)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED906_02会话下')
    def test_caseid_1981596(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD906,SESSION.PROGRAMMING,UnLock.L0,'00000005','7f2e31',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED906_03会话下')
    def test_caseid_1981595(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD906,SESSION.EXTENDED,UnLock.L0,'00000006','62d90600000006',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD906,SESSION.EMPTY,UnLock.L0,'00000006','62d90600000006',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD906,SESSION.EMPTY,UnLock.L0,'00000032','62d90600000032',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD906,SESSION.EMPTY,UnLock.L0,'00000054','62d90600000054',check_method=Check_Method.read)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D907_01会话下')
    def test_caseid_1981594(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD907,SESSION.DEFAULT,'62d907',check_length=70)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D907_02会话下')
    def test_caseid_1981593(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD907,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D907_03会话下')
    def test_caseid_1981592(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD907,SESSION.EXTENDED,'62d907',check_length=70)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED907_01会话下')
    def test_caseid_1981591(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD907,SESSION.DEFAULT,UnLock.L0,'3130363535303031303634363330303137000000000000000000000000000000','62d9073130363535303031303634363330303137000000000000000000000000000000',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD907,SESSION.EMPTY,UnLock.L0,'3121363535303031303634363330303137000000000000000000000000000000','62d9073121363535303031303634363330303137000000000000000000000000000000',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD907,SESSION.EMPTY,UnLock.L0,'2122363535303031303634363330303137000000000000000000000000000000','62d9072122363535303031303634363330303137000000000000000000000000000000',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD907,SESSION.EMPTY,UnLock.L0,'3123363535303031303634363330303137000000000000000000000000000000','62d9073123363535303031303634363330303137000000000000000000000000000000',check_method=Check_Method.read)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED907_02会话下')
    def test_caseid_1981590(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD907,SESSION.PROGRAMMING,UnLock.L0,'3130363535303031303634363330303137000000000000000000000000000000','7f2e31',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED907_03会话下')
    def test_caseid_1981589(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD907,SESSION.EXTENDED,UnLock.L0,'3130363535303031303634363330303137000000000000000000000000000000','62d9073130363535303031303634363330303137000000000000000000000000000000',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD907,SESSION.EMPTY,UnLock.L0,'3121363535303031303634363330303137000000000000000000000000000000','62d9073121363535303031303634363330303137000000000000000000000000000000',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD907,SESSION.EMPTY,UnLock.L0,'2122363535303031303634363330303137000000000000000000000000000000','62d9072122363535303031303634363330303137000000000000000000000000000000',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD907,SESSION.EMPTY,UnLock.L0,'3123362564568546545685465830303137000000000000000000000000000000','62d9073123362564568546545685465830303137000000000000000000000000000000',check_method=Check_Method.read)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D911_01会话下')
    def test_caseid_1981588(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD911,SESSION.DEFAULT,'62d911',check_length=18)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D911_02会话下')
    def test_caseid_1981587(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD911,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D911_03会话下')
    def test_caseid_1981586(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD911,SESSION.EXTENDED,'62d911',check_length=18)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D912_01会话下')
    def test_caseid_1981585(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD912,SESSION.DEFAULT,'62d912',check_length=14)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D912_02会话下')
    def test_caseid_1981584(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD912,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D912_03会话下')
    def test_caseid_1981583(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD912,SESSION.EXTENDED,'62d912',check_length=14)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D916_01会话下')
    def test_caseid_1981582(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD916,SESSION.DEFAULT,'62d916',check_length=14)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D916_02会话下')
    def test_caseid_1981581(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD916,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D916_03会话下')
    def test_caseid_1981580(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD916,SESSION.EXTENDED,'62d916',check_length=14)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED916_01会话下')
    def test_caseid_1981579(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD916,SESSION.DEFAULT,UnLock.L0,'10101011','7f2e31',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED916_02会话下')
    def test_caseid_1981578(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD916,SESSION.PROGRAMMING,UnLock.L0,'10101011','7f2e31',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED916_03会话下')
    def test_caseid_1981577(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD916,SESSION.EXTENDED,UnLock.L5,'10101011','62d91610101011',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD916,SESSION.EMPTY,UnLock.L0,'20240599','62d91620240599',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD916,SESSION.EMPTY,UnLock.L0,'88888888','62d91688888888',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.TCAM,0xD916,SESSION.EMPTY,UnLock.L0,'20991231','62d91620991231',check_method=Check_Method.read,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D949_01会话下')
    def test_caseid_1981576(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD949,SESSION.DEFAULT,'62d949',check_length=8)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D949_02会话下')
    def test_caseid_1981575(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD949,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D949_03会话下')
    def test_caseid_1981574(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD949,SESSION.EXTENDED,'62d949',check_length=8)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D99C_01会话下')
    def test_caseid_1981573(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD99C,SESSION.DEFAULT,'62d99c',check_in=['00','01'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D99C_02会话下')
    def test_caseid_1981572(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD99C,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D99C_03会话下')
    def test_caseid_1981571(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD99C,SESSION.EXTENDED,'62d99c',check_in=['00','01'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D99D_01会话下')
    def test_caseid_1981570(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD99D,SESSION.DEFAULT,'62d99d',check_in=['01','02','03','04','05','06','07','08','09','10'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D99D_02会话下')
    def test_caseid_1981569(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD99D,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D99D_03会话下')
    def test_caseid_1981568(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD99D,SESSION.EXTENDED,'62d99d',check_in=['01','02','03','04','05','06','07','08','09','10'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D99E_01会话下')
    def test_caseid_1981567(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD99E,SESSION.DEFAULT,'62d99e',check_range=[0x0000,0xffff])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D99E_02会话下')
    def test_caseid_1981566(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD99E,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D99E_03会话下')
    def test_caseid_1981565(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD99E,SESSION.EXTENDED,'62d99e',check_range=[0x0000,0xffff])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D99F_01会话下')
    def test_caseid_1981564(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD99F,SESSION.DEFAULT,'62d99f',check_range=[0,100])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D99F_02会话下')
    def test_caseid_1981563(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD99F,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D99F_03会话下')
    def test_caseid_1981562(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD99F,SESSION.EXTENDED,'62d99f',check_range=[0,100])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A0_01会话下')
    def test_caseid_1981561(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A0,SESSION.DEFAULT,'62d9a0',check_length=10)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A0_02会话下')
    def test_caseid_1981560(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A0,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A0_03会话下')
    def test_caseid_1981559(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A0,SESSION.EXTENDED,'62d9a0',check_length=10)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A1_01会话下')
    def test_caseid_1981558(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A1,SESSION.DEFAULT,'62d9a1',check_length=10)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A1_02会话下')
    def test_caseid_1981557(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A1,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A1_03会话下')
    def test_caseid_1981556(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A1,SESSION.EXTENDED,'62d9a1',check_length=10)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A2_01会话下')
    def test_caseid_1981555(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A2,SESSION.DEFAULT,'62d9a2',check_length=8)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A2_02会话下')
    def test_caseid_1981554(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A2,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A2_03会话下')
    def test_caseid_1981553(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A2,SESSION.EXTENDED,'62d9a2',check_length=8)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A4_01会话下')
    def test_caseid_1981552(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A4,SESSION.DEFAULT,'62d9a4',check_in=['00','01','02','03'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A4_02会话下')
    def test_caseid_1981551(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A4,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A4_03会话下')
    def test_caseid_1981550(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A4,SESSION.EXTENDED,'62d9a4',check_in=['00','01','02','03'])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A6_01会话下')
    def test_caseid_1981549(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A6,SESSION.DEFAULT,'62d9a6',check_length=8)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A6_02会话下')
    def test_caseid_1981548(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A6,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A6_03会话下')
    def test_caseid_1981547(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A6,SESSION.EXTENDED,'62d9a6',check_length=8)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A7_01会话下')
    def test_caseid_1981546(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A7,SESSION.DEFAULT,'62d9a7',check_length=34)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A7_02会话下')
    def test_caseid_1981545(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A7,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9A7_03会话下')
    def test_caseid_1981544(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9A7,SESSION.EXTENDED,'62d9a7',check_length=34)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9BA_01会话下')
    def test_caseid_1981543(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9BA,SESSION.DEFAULT,'62d9ba',check_length=26)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9BA_02会话下')
    def test_caseid_1981542(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9BA,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9BA_03会话下')
    def test_caseid_1981541(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9BA,SESSION.EXTENDED,'62d9ba',check_length=26)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED9BA_01会话下')
    def test_caseid_1981540(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD9BA,SESSION.DEFAULT,UnLock.L0,'30303030303030303030','62d9ba30303030303030303030',check_method=Check_Method.read)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED9BA_02会话下')
    def test_caseid_1981539(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD916,SESSION.PROGRAMMING,UnLock.L0,'30303030303030303030','7f2e31',check_method=Check_Method.response,recover=False)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)_2ED9BA_03会话下')
    def test_caseid_1981538(self):
        self.sd_tester.write_did_and_check(TA.TCAM,0xD9BA,SESSION.EXTENDED,UnLock.L0,'30303030303030303030','62d9ba30303030303030303030',check_method=Check_Method.read)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9BB_01会话下')
    def test_caseid_1981537(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9BB,SESSION.DEFAULT,'62d9bb',check_length=106)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9BB_02会话下')
    def test_caseid_1981536(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9BB,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9BB_03会话下')
    def test_caseid_1981535(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9BB,SESSION.EXTENDED,'62d9bb',check_length=106)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9BC_01会话下')
    def test_caseid_1981534(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9BC,SESSION.DEFAULT,'62d9bc',check_length=10)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9BC_02会话下')
    def test_caseid_1981533(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9BC,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9BC_03会话下')
    def test_caseid_1981532(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9BC,SESSION.EXTENDED,'62d9bc',check_length=10)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9BD_01会话下')
    def test_caseid_1981531(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9BD,SESSION.DEFAULT,'62d9bd',check_length=106)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9BD_02会话下')
    def test_caseid_1981530(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9BD,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9BD_03会话下')
    def test_caseid_1981529(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9BD,SESSION.EXTENDED,'62d9bd',check_length=106)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22E103_01会话下')
    def test_caseid_1981528(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.DEFAULT,'62e103',check_range=[0,255])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22E103_02会话下')
    def test_caseid_1981527(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22E103_03会话下')
    def test_caseid_1981526(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xE103,SESSION.EXTENDED,'62e103',check_range=[0,255])

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22FD46_01会话下')
    def test_caseid_1981525(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xFD46,SESSION.DEFAULT,'62fd46',check_length=606)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22FD46_02会话下')
    def test_caseid_1981524(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xFD46,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22FD46_03会话下')
    def test_caseid_1981523(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xFD46,SESSION.EXTENDED,'62fd46',check_length=606)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22FD50_01会话下')
    def test_caseid_1981522(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xFD50,SESSION.DEFAULT,'62fd50',check_length=26)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22FD50_02会话下')
    def test_caseid_1981521(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xFD50,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22FD50_03会话下')
    def test_caseid_1981520(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xFD50,SESSION.EXTENDED,'62fd50',check_length=26)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9C0_01会话下')
    def test_caseid_1981519(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9C0,SESSION.DEFAULT,'62d9c0',check_length=206)

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9C0_02会话下')
    def test_caseid_1981518(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9C0,SESSION.PROGRAMMING,'7f2231')

    @pytest.mark.full
    @allure.story('诊断服务')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_22D9C0_03会话下')
    def test_caseid_1981517(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD9C0,SESSION.EXTENDED,'62d9c0',check_length=206)

    # # @pytest.mark.repeat(200)
    # @pytest.mark.full
    # @allure.story('诊断服务')
    # @allure.title('UDS_ReadDataByIdentifier(0x22)_22EA41_01会话下')
    # def test_caseid_1981516(self):
    #     self.sd_tester.read_did_and_check(TA.TCAM,0xEA41,SESSION.DEFAULT,'62ea41')

    # @pytest.mark.full
    # @allure.story('诊断服务')
    # @allure.title('UDS_ReadDataByIdentifier(0x22)_22EA41_02会话下')
    # def test_caseid_1981515(self):
    #     self.sd_tester.read_did_and_check(TA.TCAM,0xEA41,SESSION.PROGRAMMING,'7f2231')

    # @pytest.mark.repeat(200)
    # @pytest.mark.full
    # @allure.story('诊断服务')
    # @allure.title('UDS_ReadDataByIdentifier(0x22)_22EA41_03会话下')
    # def test_caseid_1981514(self):
    #     self.sd_tester.read_did_and_check(TA.TCAM,0xEA41,SESSION.EXTENDED,'62ea41')
        



    # EOL:
    # test_caseid_1981712 只能写一次，需要手动测试，整个大版本测一次
    # test_caseid_1981731 只能写一次，需要手动测试，整个大版本测一次
    # test_caseid_1981734 只能写一次，需要手动测试，整个大版本测一次

    # UDS：
    # test_caseid_1981202-1981171 共32条,28服务不需要测
    # test_caseid_1981120 28服务不需要测
    # test_caseid_1981118 28服务不需要测
    # test_caseid_1981116 28服务不需要测
    
   
    


