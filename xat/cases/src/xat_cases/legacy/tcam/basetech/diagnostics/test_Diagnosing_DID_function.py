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
import re
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))


from xat_cases.legacy.basetech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH


@allure.feature('TCAM BaseTech/诊断')
class TestDID_function(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self,ecu)
        with allure.step("初始化环境"):
            self.mix.init_boot_per()
        global ip
        ip = self.tc_config.get('gateway_ip')

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,check_data='62f18601',check_length=8)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        with allure.step("初始化环境"):
            self.mix.init_boot_per()
        super().after_class(self, ecu)
    
    def get_command_result(self,command, re_txt, timeout=2):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                ret = self.ssh.tcam_ssh.type_commands(commands=command,expect='OK',timeout=1)
                if ret is not None:
                    if ',' in ret:
                        res = re.search('"(.*?)"',ret)
                        if res:
                            return res.group(1)
                    else:
                        res = re.findall(f'{re_txt}: (\d+)',ret)
                        if res:
                            return res[0]
                raise FileNotFoundError
            except:
                time.sleep(0.5)
        
    @pytest.mark.full
    @allure.story('功能诊断DID')
    @allure.title('验证DD00功能')
    def test_caseid_1987393(self):
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr12", "CarTiGlb",0)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd00,SESSION.EMPTY,'62dd00ffffffff')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr12", "CarTiGlb",1)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd00,SESSION.EMPTY,'62dd0000000001')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr12", "CarTiGlb",1000000)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd00,SESSION.EMPTY,'62dd00000f4240')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr12", "CarTiGlb",315619199)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd00,SESSION.EMPTY,'62dd0012cff77f')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr12", "CarTiGlb",315619200)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd00,SESSION.EMPTY,'62dd0012cff780')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr12", "CarTiGlb",315619201)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd00,SESSION.EMPTY,'62dd0012cff781')
        

    @pytest.mark.full
    @allure.story('功能诊断DID')
    @allure.title('验证DD01功能')
    def test_caseid_1987392(self):
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr13", "BkpOfDstTrvld",0)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd01,SESSION.EMPTY,'62dd01ffffff')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr13", "BkpOfDstTrvld",1000000)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd01,SESSION.EMPTY,'62dd010f4240')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr13", "BkpOfDstTrvld",2000000)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd01,SESSION.EMPTY,'62dd011e8480')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr13", "BkpOfDstTrvld",2097151)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd01,SESSION.EMPTY,'62dd011fffff')
             


    @pytest.mark.full
    @allure.story('功能诊断DID')
    @allure.title('验证DD02功能')
    def test_caseid_1987391(self):
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr13", "VehBattUSysU",0)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd02,SESSION.EMPTY,'62dd02ff')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr13", "VehBattUSysU",50)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd02,SESSION.EMPTY,'62dd0214')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr13", "VehBattUSysU",100)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd02,SESSION.EMPTY,'62dd0228')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr13", "VehBattUSysU",255)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd02,SESSION.EMPTY,'62dd0266')

    @pytest.mark.full
    @allure.story('功能诊断DID')
    @allure.title('验证DD0A功能')
    def test_caseid_1987390(self):
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1UsgModSts",0)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd0a,SESSION.EMPTY,'62dd0a00')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1UsgModSts",1)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd0a,SESSION.EMPTY,'62dd0a01')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1UsgModSts",2)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd0a,SESSION.EMPTY,'62dd0a02')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1UsgModSts",11)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd0a,SESSION.EMPTY,'62dd0a0b')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1UsgModSts",13)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd0a,SESSION.EMPTY,'62dd0a0d')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1UsgModSts",0)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd0a,SESSION.EMPTY,'62dd0a00')
        

    @pytest.mark.full
    @allure.story('功能诊断DID')
    @allure.title('验证DD0C功能')
    def test_caseid_1987389(self):
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1PwrLvlElecMai",0)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd0c,SESSION.EMPTY,'62dd0cff')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1PwrLvlElecMai",1)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd0c,SESSION.EMPTY,'62dd0c01')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1PwrLvlElecMai",2)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd0c,SESSION.EMPTY,'62dd0c02')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1PwrLvlElecMai",3)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd0c,SESSION.EMPTY,'62dd0c03')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1PwrLvlElecMai",4)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd0c,SESSION.EMPTY,'62dd0c04')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1PwrLvlElecMai",5)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd0c,SESSION.EMPTY,'62dd0c05')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1PwrLvlElecMai",0)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xdd0c,SESSION.EMPTY,'62dd0cff')

    @pytest.mark.full
    @allure.story('功能诊断DID')
    @allure.title('验证41AE功能')
    def test_caseid_1987388(self):
        data1 =self.sd_tester.read_did_and_check(TA.TCAM,0x41AE,SESSION.DEFAULT,'6241ae')
        data1 = ''.join([chr(int(data1[6:][i:i + 2],16)) for i in range(0, len(data1[6:]), 2)])
        data2 = self.get_command_result('cat /dev/smd8 & echo -en "at+iccid\\r\\n" > /dev/smd8','ICCID')
        assert data1 == data2 ,f'{data1}和{data2}不一致'

    @pytest.mark.full
    @allure.story('功能诊断DID')
    @allure.title('验证9003功能')
    def test_caseid_1987387(self):
        data1 =self.sd_tester.read_did_and_check(TA.TCAM,0x9003,SESSION.DEFAULT,'629003')
        data1 = ''.join([chr(int(data1[6:28][i:i + 2],16)) for i in range(0, len(data1[6:28]), 2)])
        data2 = self.get_command_result('cat /dev/smd8 & echo -en "AT+CNUM\\r\\n" > /dev/smd8','')
        assert data1 == data2 ,f'{data1}和{data2}不一致'
        
    @pytest.mark.full
    @allure.story('功能诊断DID')
    @allure.title('验证CF05功能')
    def test_caseid_1987386(self):
        data1 =self.sd_tester.read_did_and_check(TA.TCAM,0xCF05,SESSION.DEFAULT,'62cf05') 
        data1 = ''.join([chr(int(data1[6:][i:i + 2],16)) for i in range(0, len(data1[6:]), 2)])
        data2 = self.get_command_result('cat /dev/smd8 & echo -en "ATI\\r\\n" > /dev/smd8','IMEI')
        assert data1 == data2 ,f'{data1}和{data2}不一致'

    @pytest.mark.full
    @allure.story('功能诊断DID')
    @allure.title('验证D0B5功能')
    def test_caseid_1987385(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD0B5,SESSION.DEFAULT,'62d0b5')
        # 人工对比结果


    @pytest.mark.full
    @allure.story('功能诊断DID')
    @allure.title('验证D134功能')
    def test_caseid_1987383(self):
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1CarModSts1",0)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xd134,SESSION.EMPTY,'62d13400')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1CarModSts1",1)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xd134,SESSION.EMPTY,'62d13401')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1CarModSts1",2)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xd134,SESSION.EMPTY,'62d13402')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1CarModSts1",3)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xd134,SESSION.EMPTY,'62d13403')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1CarModSts1",5)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xd134,SESSION.EMPTY,'62d13405')
        self.bus_comm.set_singal("connectivitycanfd","VgmConnFr01", "VehModMngtGlbSafe1CarModSts1",0)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.TCAM,0xd134,SESSION.EMPTY,'62d13400')

    @pytest.mark.full
    @allure.story('功能诊断DID')
    @allure.title('验证D251功能')
    def test_caseid_1987382(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD251,SESSION.DEFAULT,'62d251c0')


    @pytest.mark.full
    @allure.story('功能诊断DID')
    @allure.title('验证D911功能')
    def test_caseid_1987381(self):
        self.sd_tester.read_did_and_check(TA.TCAM,0xD911,SESSION.DEFAULT,'62d911313131303033')

    @pytest.mark.full
    @allure.story('功能诊断DID')
    @allure.title('验证D912功能')
    def test_caseid_1987380(self):
        data1 = self.sd_tester.read_did_and_check(TA.TCAM,0xD912,SESSION.DEFAULT,'62d912')
        data2 = self.sd_tester.read_did_and_check(TA.TCAM,0xF18C,SESSION.EMPTY,'62f18c')
        assert data1[6:] == data2[6:],f'返回结果{data1},{data2}不一致'
         


    # @pytest.mark.full
    # @allure.story('功能诊断DID')
    # @allure.title('验证D9A0功能')
    # def test_caseid_1987379(self):
        # # self.sd_tester.read_did_and_check(TA.TCAM,0xD9A0,SESSION.DEFAULT,'62d9a0')
        # # self.serial.send(command='bb --temp \\r\\n',pattern='BB tem',timeout=10)
        # self.serial.send(command='bb --temp\r\n'.encode('utf-8'), pattern='BB tem', timeout=10)
        # ret_data = self.serial.receive()
        # logger.info(ret_data)
    # 需要手动接串口工具
        

    # @pytest.mark.full
    # @allure.story('功能诊断DID')
    # @allure.title('验证D9A2功能')
    # def test_caseid_1987378(self):
        # self.sd_tester.read_did_and_check(TA.TCAM,0xD9A2,SESSION.DEFAULT,'62d9a2')
        # self.serial.send(command='bb --voltage \\r\\n',pattern='BB voltage',timeout=10)
        # ret_data = self.serial.receive()
        # logger.info(ret_data)
    # # 需要手动接串口工具


    # @pytest.mark.full
    # @allure.story('功能诊断DID')
    # @allure.title('验证F102功能')
    # def test_caseid_1987377(self):
    #     self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
    #     # 默认FFFFFFFFFF常量算出来的key
    #     self.sd_tester.unlock_and_check(TA.TCAM,SESSION.PROGRAMMING,UnLock.L1,check_data='6702') 
    #     self.sd_tester.write_did_and_check(TA.TCAM,0xF102,SESSION.EMPTY,UnLock.L0,'FFFFFFFFEE','6ef102',check_method=Check_Method.response,recover=False)
    #     self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
    #     self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
    #     # 默认FFFFFFFFFF常量算出来的key
    #     self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EMPTY,UnLock.L1,check_data='7f2735') 
    #     # 步骤5写入的FFFFFFFFEE常量算出来的key
    #     self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EMPTY,UnLock.L1,check_data='6702') 

    # 只能写一次


    # @pytest.mark.full
    # @allure.story('功能诊断DID')
    # @allure.title('验证D01C,D03A功能')
    # def test_caseid_1987376(self):
    #     self.sd_tester.read_did_and_check(TA.TCAM,0xD03A,SESSION.DEFAULT,'7f2231')
    #     self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
    #     self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EMPTY,UnLock.L1,check_data='6702') 
    #     self.sd_tester.read_did_and_check(TA.TCAM,0xD01C,SESSION.EMPTY,'7f2222')
    #     self.sd_tester.write_did_and_check(TA.TCAM,0xD01C,SESSION.EMPTY,UnLock.L0,'A2C837613E12B712ADF3F540751F77A24E82B9E01C61D152FA1DFAA3D699E8A4670FB350628FB490732E948473A9273FB76D62DFEC15CDF8AB8310199A23FCBF2EA3C91593E855968626E197F30D048D90F0BB95CB2C501E09DBCFA3BA4A8CE6F8461EF1EE4527732D976E5D494D43DE009F02A91329A44E26EDF3CD61E1B02633B9E9AC196D79072203F9F009FEC94E4A1BB9B0040346BC6B645C29E614ED2C9B82C681C8374817231298F716DD8CA26E5D18B9E8BD05AC14339B81C0C6E2EEB27ED1F570C0425147B2429665E11F08675E3FDAE30D0A336A2897231B8A8BEDD965E3464943085A3DA026C807FB52BEE8B0972AFDFC477EB2F88187305D381F00010001C0E7686676D89205A740DEE5A0E8E269FFCA903A3C36EC1309A76825A6C54DC0','6ed01c',check_method=Check_Method.response,recover=False)
    #     self.sd_tester.read_did_and_check(TA.TCAM,0xD01C,SESSION.EMPTY,'62d01cc0e7686676d89205a740dee5a0e8e269ffca903a3c36ec1309a76825a6c54dc0')
    #     self.sd_tester.write_did_and_check(TA.TCAM,0xD01C,SESSION.EMPTY,UnLock.L0,'A2C837613E12B712ADF3F540751F77A24E82B9E01C61D152FA1DFAA3D699E8A4670FB350628FB490732E948473A9273FB76D62DFEC15CDF8AB8310199A23FCBF2EA3C91593E855968626E197F30D048D90F0BB95CB2C501E09DBCFA3BA4A8CE6F8461EF1EE4527732D976E5D494D43DE009F02A91329A44E26EDF3CD61E1B02633B9E9AC196D79072203F9F009FEC94E4A1BB9B0040346BC6B645C29E614ED2C9B82C681C8374817231298F716DD8CA26E5D18B9E8BD05AC14339B81C0C6E2EEB27ED1F570C0425147B2429665E11F08675E3FDAE30D0A336A2897231B8A8BEDD965E3464943085A3DA026C807FB52BEE8B0972AFDFC477EB2F88187305D381F00010001C0E7686676D89205A740DEE5A0E8E269FFCA903A3C36EC1309A76825A6C54DC0','7f2222',check_method=Check_Method.response,recover=False)
    #     self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
    #     self.sd_tester.read_did_and_check(TA.TCAM,0xD03A,SESSION.EMPTY,'62d03ac0e7686676d89205a740dee5a0e8e269ffca903a3c36ec1309a76825a6c54dc0')
    #     # 只能写一次

    # @pytest.mark.full
    # @allure.story('功能诊断DID')
    # @allure.title('验证D12F功能')
    # def test_caseid_1987375(self):
    #     self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
    #     # 默认的安全常量算出来的key
    #     self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EMPTY,UnLock.L11,check_data='6712')
    #     self.sd_tester.read_did_and_check(TA.TCAM,0xD12F,SESSION.EMPTY,'62d12fffffffffff')
    #     self.sd_tester.write_did_and_check(TA.TCAM,0xd12f,SESSION.EMPTY,UnLock.L0,'FFFFFFFFEE','6ed12f',check_method=Check_Method.response,recover=False)
    #     self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.DEFAULT,'62f18601')
    #     self.sd_tester.session_ctrl_and_check(TA.TCAM,SESSION.PROGRAMMING,'62f18602')
    #     # 默认FFFFFFFFFF常量算出来的key
    #     self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EMPTY,UnLock.L11,check_data='7f2735') 
    #     # 步骤5写入的FFFFFFFFEE常量算出来的key
    #     self.sd_tester.unlock_and_check(TA.TCAM,SESSION.EMPTY,UnLock.L11,check_data='6712') 
    #     self.sd_tester.read_did_and_check(TA.TCAM,0xD12F,SESSION.EMPTY,'62d12fffffffffee')
    # # 只能写一次


# 功能DID共22条用例，一条不能实现自动化，3条非易失性验证在刷写里，5条写好了注释掉，需要接MCU串口和新板子才可以执行
# 一条不能实现自动化的是1987384


    # pytest basetech/diagnostics/Diagnosing_DID_function.py -k test_caseid_1987391 --disable_env=true
    
    # ./setpcan.sh