#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename     : test_diag_bgm_did.py
@time         : 2023/11/26 14:19
@author       : o_jingyuan.chen@external.jiduauto.com
@description  : 
'''
import pytest
from xat_cases.legacy.bgm.BaseTech.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature('BGM BaseTech/诊断功能/诊断DID')
class TestDIDApp(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        logger.info("before_class")
        with allure.step("初始化环境"):
            self.mix.init_boot_per()
        self.f1aa = self.sd_tester.get_ecu_core_assembly_part_number()
        self.f1ab = self.sd_tester.get_ecu_delivery_assembly_part_number()
        self.f18c = self.sd_tester.get_ecu_serial_number()
        self.vin = self.sd_tester.get_vehicle_identification_number()
        self.f1f0 = self.sd_tester.get_mcu_software_part_number()
        # self.f1a5 = self.sd_tester.get_primary_bootloader_software_part_number()
        # self.fl02 = hex(self.tc_config['sec_con']['BGM'][0])[2:] if len(hex(self.tc_config['sec_con']['BGM'][0])[2:]) % 2 == 0 else '0' + hex(self.tc_config['sec_con']['BGM'][0])[2:]

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.sd_tester.update_serverdoipid(0x1002)
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86])
        if recv_data_list[3] == 0x2:
            self.sd_tester.quit_boot()
        self.sd_tester.update_serverdoipid(0x1001)
        err_code, recv_data_list = self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86])
        if recv_data_list[3] == 0x2:
            self.sd_tester.quit_boot()

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        logger.info("after_class")
        with allure.step("恢复环境"):
            self.mix.init_boot_per()
        super().after_class(self, ecu)

    # APP ECU完整零件序列号（APP+SBL+PBL）
    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_CompleteSetOfECUPart|SerialNumbersInAPP_ED20')
    def test_caseid_1981701(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xED20, SESSION.DEFAULT,
                                          f'62ed20f1aa{self.f1aa}f1ab{self.f1ab}f18c{self.f18c}')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xED20, SESSION.DEFAULT,
                                          f'62ed20f1aa{self.f1aa}f1ab{self.f1ab}f18c{self.f18c}')

        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xED20, SESSION.EXTENDED,
                                          f'62ed20f1aa{self.f1aa}f1ab{self.f1ab}f18c{self.f18c}')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xED20, SESSION.EXTENDED,
                                          f'62ed20f1aa{self.f1aa}f1ab{self.f1ab}f18c{self.f18c}')

    # 当前诊断会话（APP+SBL+PBL）
    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_ActiveDiagSessionDataRecord_F186')
    def test_caseid_1981700(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xF186, SESSION.DEFAULT, '62f18601')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xF186, SESSION.DEFAULT, '62f18601')

        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xF186, SESSION.EXTENDED, '62f18603')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xF186, SESSION.EXTENDED, '62f18603')

    # ECU序列号（APP+SBL+PBL）
    # BGM_SOC,BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_ECU Serial Number_F18C')
    def test_caseid_1981699(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xF18C, SESSION.DEFAULT, '62f18c', check_length=14)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xF18C, SESSION.DEFAULT, '62f18c', check_length=14)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xF18C, SESSION.EXTENDED, '62f18c', check_length=14)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xF18C, SESSION.EXTENDED, '62f18c', check_length=14)

    # VIN码（APP）
    # BGM_SOC,BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_Vehicle Identification Number_F190')
    def test_caseid_1981697(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xF190, SESSION.DEFAULT, check_data='62f190', check_length=40)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xF190, SESSION.DEFAULT, check_data='62f190', check_length=40)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xF190, SESSION.EXTENDED, '62f190', check_length=40)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xF190, SESSION.EXTENDED, '62f190', check_length=40)

    # VIN码（APP） EOL车架号写入——VIN_write
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)_Vehicle Identification Number_F190')
    def test_caseid_1981696(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xf190, SESSION.EXTENDED, UnLock.L5,
                                           'ffffffffffffffffffffffffffffffffff',
                                           '62f190ffffffffffffffffffffffffffffffffff', check_method=Check_Method.reset)

        self.mix.write_did_and_check(TA.BGM_MCU, 0xf190, SESSION.EXTENDED, UnLock.L5,
                                           'ffffffffffffffffffffffffffffffffff',
                                           '62f190ffffffffffffffffffffffffffffffffff', check_method=Check_Method.kl30)

     # APP诊断数据库零件号（APP）
    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_Application Diagnostic Database Part Number_F1A0')
    def test_caseid_1981695(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf1a0, SESSION.DEFAULT, '62f1a0', check_length=22)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1a0, SESSION.DEFAULT, '62f1a0', check_length=22)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf1a0, SESSION.EXTENDED, '62f1a0', check_length=22)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1a0, SESSION.EXTENDED, '62f1a0', check_length=22)

    # #ECU硬件号（APP+SBL+PBL）
    # #BGM_SOC,BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_ECU Core Assembly Part Number_F1AA')
    def test_caseid_1981694(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf1aa, SESSION.DEFAULT, '62f1aa', check_length=22)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1aa, SESSION.DEFAULT, '62f1aa', check_length=22)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf1aa, SESSION.EXTENDED, '62f1aa', check_length=22)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1aa, SESSION.EXTENDED, '62f1aa', check_length=22)

    # #ECU总成号（APP+SBL+PBL）
    # #BGM_SOC,BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_ECU Delivery Assembly Part Number_F1AB')
    def test_caseid_1981693(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf1ab, SESSION.DEFAULT, '62f1ab', check_length=22)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1ab, SESSION.DEFAULT, '62f1ab', check_length=22)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1ab, SESSION.EXTENDED, '62f1ab', check_length=22)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf1ab, SESSION.EXTENDED, '62f1ab', check_length=22)

    # #ECU软件号ECU软件号数量2+ECU软件号8+MCU bootloader号8（APP）
    # #BGM_SOC
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)ECU Software Part Numbers_F1AE')
    def test_caseid_1981692(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf1ae, SESSION.DEFAULT, '62f1ae', check_length=40)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf1ae, SESSION.EXTENDED, '62f1ae', check_length=40)

    # SBL软件版本号（SBL）需要DSA烧录BGM_MCU_APP文件后，才可以读f124,这个搞不来自动化 需要在sbl刷完之后读
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Secondary Bootloader Software Version Number_F124')
    def test_caseid_1981691(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf124, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf124, SESSION.EXTENDED, '7f2231')
        # self.sd_tester.read_did_and_check(TA.BGM_MCU,0xf124,SESSION.PROGRAMMING,'62f124',check_length=20)
        # pass

    # 子节点总数（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Total number of Private ECU(s) / component(s) Serial Numbers_F13F')
    def test_caseid_1981690(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf13f, SESSION.DEFAULT, '62f13f', check_length=584)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf13f, SESSION.EXTENDED, '62f13f', check_length=584)

    # PBL软件号（APP+SBL+PBL）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Primary Bootloader Software Part Number_F1A5')
    def test_caseid_1981689(self):
        self.f1a5 = self.sd_tester.get_primary_bootloader_software_part_number()
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1a5, SESSION.DEFAULT, f'62f1a5{self.f1a5}', check_length=22)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1a5, SESSION.EXTENDED, f'62f1a5{self.f1a5}', check_length=22)

    # MCU软件号（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)MCU Software part number_F1F0')
    def test_caseid_1981688(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1f0, SESSION.DEFAULT, f'62f1f0{self.f1f0}', check_length=24)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1f0, SESSION.EXTENDED, f'62f1f0{self.f1f0}', check_length=24)

    # 公钥（PBL）#公钥（PBL）仅能写入一次
    # BGM _SOC
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Public Key_D01C')
    def test_caseid_1981687(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xd01c, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xd01c, SESSION.EXTENDED, '7f2231')
    
    # BGM _SOC
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Public Key_D01C')
    def test_caseid_1981686(self):
        self.mix.delete_vehicleInfo_json()  # 删除密钥后重启并等待10s,最终删除后等待40S贴合工厂实际情况
        time.sleep(30)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xd01c, SESSION.PROGRAMMING, '7f2222')
        self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xd01c, SESSION.EMPTY, UnLock.L1,
                                           'a49cb766e25b71fc084de0524ad46442f5a3f847219dc9f729a7e6d76bbc9b14fb7e15d7bd9ffb3f1bcfdc5448154c5bf39492aabc8716f2486c234efc96a614a01b43a923d8cf5401de5115878fe86cfd2e9adfa9f28dc3d090f825cba54e6193aa8a6cdb842eced5b34be4428609312d1783055a1bbb0a740286357e115deb2874b121e5dccfee6f10d059cfc0dc7049de08e518eeeb7564d0a64e483df1768afbca3484a99cb79e12597c89cca1bd4d70ba74606db8bbec10f3b3a9118c4e40d233e6f1bbba5a9038c9cdda644d1e40b6c419535beab8e9a3b73b4251358c012aee2961e1bca3d2abf684a28209b058c0091c857055d5c8826388dd7dffe100010001fc2a8b1665746be6425d05c3d81bf9d03c9115a54b50c4a7dd9ad4ec99429577',
                                           '62d01cfc2a8b1665746be6425d05c3d81bf9d03c9115a54b50c4a7dd9ad4ec99429577',
                                           recover=False)
        self.sd_tester.reset_0x1181()
        vid=self.tc_config['vid']        
        self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xb163, SESSION.EXTENDED, UnLock.L7,
                                           vid, f'62b163{vid}',
                                           check_method=Check_Method.reset, recover=False)
                                           
    # L1安全常数（PBL）
    # BGM _SOC
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Security Constant_Level 01_F102')
    def test_caseid_1981685(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf102, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf102, SESSION.EXTENDED, '7f2231')

    # 软件证书公钥校验（APP）
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)swAuth Public Key CheckSum_D03A')  # D03A读取前提是先写入D01C的值
    def test_caseid_1981683(self):
        response = self.sd_tester.read_did_and_check(TA.BGM_SOC,0xd01c,SESSION.PROGRAMMING)
        if response == '7f2222':
            self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xd01c, SESSION.EMPTY, UnLock.L1,
                                               'a49cb766e25b71fc084de0524ad46442f5a3f847219dc9f729a7e6d76bbc9b14fb7e15d7bd9ffb3f1bcfdc5448154c5bf39492aabc8716f2486c234efc96a614a01b43a923d8cf5401de5115878fe86cfd2e9adfa9f28dc3d090f825cba54e6193aa8a6cdb842eced5b34be4428609312d1783055a1bbb0a740286357e115deb2874b121e5dccfee6f10d059cfc0dc7049de08e518eeeb7564d0a64e483df1768afbca3484a99cb79e12597c89cca1bd4d70ba74606db8bbec10f3b3a9118c4e40d233e6f1bbba5a9038c9cdda644d1e40b6c419535beab8e9a3b73b4251358c012aee2961e1bca3d2abf684a28209b058c0091c857055d5c8826388dd7dffe100010001fc2a8b1665746be6425d05c3d81bf9d03c9115a54b50c4a7dd9ad4ec99429577',
                                               '62d01cfc2a8b1665746be6425d05c3d81bf9d03c9115a54b50c4a7dd9ad4ec99429577',
                                               recover=False)
            self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xd03a, SESSION.DEFAULT, '62d03a', check_length=70)
            self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xd03a, SESSION.EXTENDED, '62d03a', check_length=70)
            self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xd03a, SESSION.PROGRAMMING, '7f2231')
        else:
            self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xd03a, SESSION.DEFAULT, '62d03a', check_length=70)
            self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xd03a, SESSION.EXTENDED, '62d03a', check_length=70)
            self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xd03a, SESSION.PROGRAMMING, '7f2231')

    # 车辆配置错误参数（APP）#SOC删掉
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Car Configuration Parameter Faults_E103')
    def test_caseid_1981682(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xe103, SESSION.DEFAULT, '62e103', check_length=68)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xe103, SESSION.EXTENDED, '62e103', check_length=68)

    # 整车基线版本号（APP）
    # BGM _SOC
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Vehicle baseline number_F150')  # 先写才能读出
    def test_caseid_1981679(self):
        self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xf150, SESSION.EXTENDED, UnLock.L5, '6100000200204141',
                                           '62f1506100000200204141', check_method=Check_Method.reset, recover=False)
        self.mix.write_did_and_check(TA.BGM_SOC, 0xf150, SESSION.EXTENDED, UnLock.L5, '6100000200204141',
                                           '62f1506100000200204141', check_method=Check_Method.kl30, recover=False)

    # 整车基线版本号（APP）
    # BGM _SOC
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle baseline number_F150')
    def test_caseid_1981680(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf150, SESSION.DEFAULT, '62f150', check_length=22)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf150, SESSION.EXTENDED, '62f150', check_length=22)

    # VID（APP）
    # BGM _SOC
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle Identification_B163')
    def test_caseid_1981678(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb163, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb163, SESSION.EXTENDED, '7f2233')

    # VID（APP）
    # BGM _SOC
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle Identification_B163_L5')
    def test_caseid_1981677(self):
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EXTENDED, UnLock.L5)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb163, SESSION.EMPTY, '62b163', check_length=38)

    # VID（APP）
    # BGM _SOC
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle Identification_B163_L7')
    def test_caseid_1981676(self):
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EXTENDED, UnLock.L7, constant=self.bgm_l7)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb163, SESSION.EMPTY, '62b163', check_length=38)

    # VID（APP）
    # BGM _SOC
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Vehicle Identification_B163')
    def test_caseid_1981675(self):
        vid=self.tc_config['vid']        
        self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xb163, SESSION.EXTENDED, UnLock.L7,
                                           vid, f'62b163{vid}',
                                           check_method=Check_Method.reset, recover=False)
        
        self.mix.write_did_and_check(TA.BGM_SOC, 0xb163, SESSION.EXTENDED, UnLock.L7,
                                           vid, f'62b163{vid}',
                                           check_method=Check_Method.kl30, recover=False)

    # FOTA升级状态（APP）
    # BGM _SOC
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)FOTA result_F154')
    def test_caseid_1981674(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf154, SESSION.DEFAULT, '62f154')
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf154, SESSION.EXTENDED, '62f154')

    # FOTA升级状态（APP）
    # BGM _SOC
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)FOTA result_F154')
    def test_caseid_1981673(self):
        self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xf154, SESSION.EXTENDED, UnLock.L5, '000000', '62f154',
                                           check_method=Check_Method.reset)
        self.mix.write_did_and_check(TA.BGM_SOC, 0xf154, SESSION.EXTENDED, UnLock.L5, '000000', '62f154',
                                           check_method=Check_Method.kl30)

    # fw major version；minor version；build version；fw and config version（APP）
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Switch Firmware and CFG version_FD50')
    def test_caseid_1981672(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xfd50, SESSION.DEFAULT, '62fd50', check_length=30)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xfd50, SESSION.EXTENDED, '62fd50', check_length=30)

    # 整车展示的版本号（APP）
    # BGM _SOC
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle Diaplay Baseline Number_F151')
    def test_caseid_1981671(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf151, SESSION.DEFAULT, '62f151', check_length=70)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf151, SESSION.EXTENDED, '62f151', check_length=70)

    # 整车展示的版本号（APP）
    # BGM _SOC
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Vehicle Diaplay Baseline Number_F151')
    def test_caseid_1981670(self):
        self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xf151, SESSION.EXTENDED, UnLock.L5,
                                           '067b9e1c3c61ac0e776decd18c05ee61067b9e1c3c61ac0e776decd18c05ee61',
                                           '62f151067b9e1c3c61ac0e776decd18c05ee61067b9e1c3c61ac0e776decd18c05ee61',
                                           check_method=Check_Method.reset)
        self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.EXTENDED,UnLock.L5)
        data = self.sd_tester.send_data_and_check(TA.BGM_SOC,'22f151','62f151')[6:]
        # self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xf151, SESSION.EXTENDED, UnLock.L5,
        #                                    '56302e302e300000000000000000000000000000000000000000000000000000',
        #                                    '62f15156302e302e300000000000000000000000000000000000000000000000000000',
        #                                    check_method=Check_Method.read,recover=False)
        self.sd_tester.send_data_and_check(TA.BGM_SOC,'2ef151067b9e1c3c61ac0e776decd18c05ee61067b9e1c3c61ac0e776decd18c05ee61','6ef151')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.send_data_and_check(TA.BGM_SOC,'22f151','62f151067b9e1c3c61ac0e776decd18c05ee61067b9e1c3c61ac0e776decd18c05ee61')
        self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xf151, SESSION.EXTENDED, UnLock.L5,
                                           data,
                                           f'62f151{data}',
                                           check_method=Check_Method.read,recover=False)

    # OBD防火墙状态（APP）
    # BGM _SOC
    @pytest.mark.sanity
    @allure.story('诊断DID')  # 02会话下不可读，现在可读,需求写错了，需求也想可读
    @allure.title('UDS_ReadDataByIdentifier(0x22)OBD Firewall status_B165')
    def test_caseid_1981669(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb165, SESSION.DEFAULT, '62b165', check_length=8)
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb165, SESSION.EXTENDED, '62b165', check_length=8)
        # pass

    # 工厂模式下自动解锁时间设置（APP）
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Fartory mode AutoUnlock TimeSetting_B200')
    def test_caseid_1981668(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xB200, SESSION.DEFAULT, '62b200')
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xB200, SESSION.EXTENDED, '62b200')

    # 工厂模式下自动解锁时间设置（APP）
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Fartory mode AutoUnlock TimeSetting_B200')
    def test_caseid_1981667(self):
        self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xb200, SESSION.EXTENDED, UnLock.L5, '02', '62b20002',
                                           check_method=Check_Method.reset)
        self.sd_tester.unlock_and_check(TA.BGM_SOC,SESSION.EXTENDED,UnLock.L5)
        data = self.sd_tester.send_data_and_check(TA.BGM_SOC,'22b200','62b200')[6:]
        # self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xf151, SESSION.EXTENDED, UnLock.L5,
        #                                    '56302e302e300000000000000000000000000000000000000000000000000000',
        #                                    '62f15156302e302e300000000000000000000000000000000000000000000000000000',
        #                                    check_method=Check_Method.read,recover=False)
        self.sd_tester.send_data_and_check(TA.BGM_SOC,'2eb20002','6eb200')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.send_data_and_check(TA.BGM_SOC,'22b200','62b20002')
        self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xb200, SESSION.EXTENDED, UnLock.L5,
                                           data,
                                           f'62b200{data}',
                                           check_method=Check_Method.read,recover=False)
                                           

    # 转向灯状态（APP）
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Get TurnLamp Status_B250')
    def test_caseid_1981666(self):
        p = self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xB250, SESSION.DEFAULT, '62b250')
        assert p[-4:-2] == '00' or p[-4:-2] == '01' or p[-4:-2] == '10' or p[-4:-2] == '11'
        assert 0 <= int(p[-2:], 16) <= 255
        p = self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xB250, SESSION.EXTENDED, '62b250')
        assert p[-4:-2] == '00' or p[-4:-2] == '01' or p[-4:-2] == '10' or p[-4:-2] == '11'
        assert 0 <= int(p[-2:], 16) <= 255

    # 整车埋点配置信息（APP） v131only
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)vehicle data tracking config_EA40')
    def test_caseid_1981665(self):
        # self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xea40, SESSION.DEFAULT, '62ea40')
        # self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xea40, SESSION.EXTENDED, '62ea40')
        pass

    # SOA服务埋点配置信息（APP） v131only
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)SOA service data tracking config_EA41')
    def test_caseid_1981664(self):
        # self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xea41, SESSION.DEFAULT, '62ea41')
        # self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xea41, SESSION.EXTENDED, '62ea41')
        pass

    # 展车模式（APP）
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Exhibition Mode Status_B300')
    def test_caseid_1981663(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb300, SESSION.DEFAULT, '62b300',
                                          check_in=[0x01, 0x00, 0x10, 0x11])
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb300, SESSION.EXTENDED, '62b300',
                                          check_in=[0x01, 0x00, 0x10, 0x11])

    # 洗车模式（APP）
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Wash Mode Status_B301')
    def test_caseid_1981662(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb301, SESSION.DEFAULT, '62b301', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb301, SESSION.EXTENDED, '62b301', check_in=[0x00, 0x01])

    # 维修模式（APP）
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Maintain Mode Status_B302')
    def test_caseid_1981661(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb302, SESSION.DEFAULT, '62b302', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb302, SESSION.EXTENDED, '62b302', check_in=[0x00, 0x01])

    # 维修模式（APP）
    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Maintain Mode Status_B302')
    def test_caseid_1981660(self):
        # self.sd_tester.write_did_and_check(TA.BGM_SOC,0xb302,SESSION.EXTENDED,UnLock.L5,'01','6eb302',check_method=Check_Method.response,recover=False)
        # self.sd_tester.reset_0x1181()
        # self.sd_tester.write_did_and_check(TA.BGM_SOC,0xb302,SESSION.EXTENDED,UnLock.L5,'01','62b30201',check_method=Check_Method.reset)
        # self.sd_tester.write_did_and_check(TA.BGM_SOC,0xb302,SESSION.EXTENDED,UnLock.L5,'00','62b30200',check_method=Check_Method.reset,recover=False)
        self.sd_tester.unlock_and_check(TA.BGM_SOC, SESSION.EXTENDED, UnLock.L5)
        time.sleep(2)
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x2e, 0xb3, 0x02, 0x01], [0x6e, 0xb3, 0x02])
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x22, 0xb3, 0x02], [0x62, 0xb3, 0x02, 0x01])
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x2e, 0xb3, 0x02, 0x00], [0x6e, 0xb3, 0x02])
        self.sd_tester.send_data_and_check(TA.BGM_SOC, [0x22, 0xb3, 0x02], [0x62, 0xb3, 0x02, 0x00])
        # pass

    # 1认证密钥（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Secret Key For Immobilizer Target #1 ECM_40DE')
    def test_caseid_1981657(self):
        self.sd_tester.write_ccp({962: 0x00})
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40de, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40de, SESSION.EXTENDED, '6240de', check_length=70)
        # self.sd_tester.read_did_and_check(TA.BGM_MCU,0x40de,SESSION.PROGRAMMING,'7f2231')

    # 1认证密钥（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Secret Key For Immobilizer Target #1 ECM_40DE')
    def test_caseid_1981656(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x40de, SESSION.EXTENDED, UnLock.L11,
                                           'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550',
                                           '6240def442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550')
        self.mix.write_did_and_check(TA.BGM_MCU, 0x40de, SESSION.EXTENDED, UnLock.L11,
                                           'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550',
                                           '6240def442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550',check_method=Check_Method.kl30)

    ##2认证密钥（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Secret Key Immobilizer Target #2 IEM_40DF')
    def test_caseid_1981655(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40df, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40df, SESSION.EXTENDED, '6240df', check_length=70)

    ##2认证密钥（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Secret Key Immobilizer Target #2 IEM_40DF')
    def test_caseid_1981654(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x40df, SESSION.EXTENDED, UnLock.L11,
                                           'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23551',
                                           '6240dff442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23551')
        self.mix.write_did_and_check(TA.BGM_MCU, 0x40df, SESSION.EXTENDED, UnLock.L11,
                                           'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23551',
                                           '6240dff442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23551',check_method=Check_Method.kl30)

    ##3认证密钥（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Secret Key Immobilizer Target #3 MGM_40E0')
    def test_caseid_1981653(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40e0, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40e0, SESSION.EXTENDED, '6240e0', check_length=70)

    ##3认证密钥（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Secret Key Immobilizer Target #3 MGM_40E0')
    def test_caseid_1981652(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x40e0, SESSION.EXTENDED, UnLock.L11,
                                           'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550',
                                           '6240e0f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550')
        self.mix.write_did_and_check(TA.BGM_MCU, 0x40e0, SESSION.EXTENDED, UnLock.L11,
                                           'f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550',
                                           '6240e0f442c8a54b7059b5449c27537bc57937bbb1b4ec8f8500a894c1121e6ab23550',check_method=Check_Method.kl30)

    # 全局时间（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Globe real time_DD00')
    def test_caseid_1981651(self):
        pl = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd00, SESSION.DEFAULT, '62dd00', check_length=14)
        assert 0 <= int(pl[6:], 16) / 600 <= 7158278, "value out of range"
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd00, SESSION.EXTENDED, '62dd00')
        assert 0 <= int(pl[6:], 16) / 600 <= 7158278, "value out of range"

    # 总里程（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Total distance_DD01')
    def test_caseid_1981650(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd01, SESSION.DEFAULT, '62dd01', check_length=12,
                                          check_range=[0x0, 0xffffff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd01, SESSION.EXTENDED, '62dd01', check_length=12,
                                          check_range=[0x0, 0xffffff])

    # 总里程（APP）#里程最大值只能是418937 ,里程可以往小了写
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Total distance_DD01')
    def test_caseid_1981649(self):
        data = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd01, SESSION.DEFAULT, '62dd01', check_length=12,
                                                 check_range=[0x0, 0xffffff])[6:]
        if 255 < int(data, 16) < 4294967:
            new_data = data[:-1] + format((int(data[-1], 16) - 1) & 0xFF, 'x')
            self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xdd01, SESSION.EXTENDED, UnLock.L5, new_data,
                                               f'62dd01{data}', check_method=Check_Method.read, recover=False)
        elif 11 < int(data, 16) <= 255:
            new_data = data[:-1] + format((int(data[-1], 16) - 1) & 0xFF, 'x')
            self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xdd01, SESSION.EXTENDED, UnLock.L5, new_data,
                                               f'62dd01{new_data}', check_method=Check_Method.read, recover=True)
            self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xdd01, SESSION.EXTENDED, UnLock.L5, '00000a',
                                               f'62dd01{data}', check_method=Check_Method.read, recover=False)
        elif 0 < int(data, 16) <= 11:
            new_data = data[:-1] + format((int(data[-1], 16) - 1) & 0xFF, 'x')
            self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xdd01, SESSION.EXTENDED, UnLock.L5, new_data,
                                               f'62dd01{data}', check_method=Check_Method.read, recover=False)
        elif int(data, 16) == 4294967:
            new_data = data[:-1] + format((int(data[-1], 16) - 1) & 0xFF, 'x')
            self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xdd01, SESSION.EXTENDED, UnLock.L5, new_data,
                                               f'62dd01{data}', check_method=Check_Method.read, recover=False)
            self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xdd01, SESSION.EXTENDED, UnLock.L5, 'ffffff',
                                               '62dd01418937', recover=False)
        elif int(data, 16) == 0:
            pass

    # 车辆电池电压（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle Battery Voltage_DD02')
    def test_caseid_1981648(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd02, SESSION.DEFAULT, '62dd02', check_length=8,
                                          check_range=[0x0, 0xff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd02, SESSION.EXTENDED, '62dd02', check_length=8,
                                          check_range=[0x0, 0xff])

    # 车辆使用模式（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Usage Mode_DD0A')
    def test_caseid_1981647(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd0a, SESSION.DEFAULT, '62dd0a', check_length=8)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd0a, SESSION.EXTENDED, '62dd0a', check_length=8)

    # 供电等级（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)EIPowerLevel_DD0C')
    def test_caseid_1981646(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd0c, SESSION.DEFAULT, '62dd0c', check_length=8,
                                          check_in=[0x0f, 0x10, 0x11, 0x20, 0x21, 0x22, 0x23, 0x24, 0x30, 0x31, 0x02,
                                                    0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3a, 0x3b, 0x3c, 0x2d,
                                                    0x3e, 0x3f, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48,
                                                    0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f, 0x50, 0x51, 0x52, 0x53,
                                                    0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5a, 0x5b, 0x5c, 0x5d, 0x5e,
                                                    0x5f, 0xff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd0c, SESSION.EXTENDED, '62dd0c', check_length=8,
                                          check_in=[0x0f, 0x10, 0x11, 0x20, 0x21, 0x22, 0x23, 0x24, 0x30, 0x31, 0x02,
                                                    0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3a, 0x3b, 0x3c, 0x2d,
                                                    0x3e, 0x3f, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48,
                                                    0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f, 0x50, 0x51, 0x52, 0x53,
                                                    0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5a, 0x5b, 0x5c, 0x5d, 0x5e,
                                                    0x5f, 0xff])

    # CCP参数（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Car Configuration Parameter_F106')
    def test_caseid_1981645(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf106, SESSION.DEFAULT, '62f106', check_length=3122)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf106, SESSION.EXTENDED, '62f106', check_length=3122)

    # CCP参数（APP）EOL 配置字写入-CCP_write
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Car Configuration Parameter_F106')
    def test_caseid_1981644(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xf106, SESSION.EXTENDED, UnLock.L5,
                                           'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEAF1',
                                           '62f106ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeaf1')

    # 电池静态电流-低范围（APP）
    # BGM_MCU
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Quiesent Current - Low Range_4025')
    def test_caseid_1981643(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4025, SESSION.DEFAULT, '624025', check_range=[0x0, 0x01ff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4025, SESSION.EXTENDED, '624025', check_range=[0x0, 0x01ff])

    # 发动机关闭时电池的归一化累积放电（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Normalised Cumulated Discharge From Battery When Engine Off_4026')
    def test_caseid_1981642(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4026, SESSION.DEFAULT, '624026', check_range=[0x0, 0x0e10])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4026, SESSION.EXTENDED, '624026', check_range=[0x0, 0x0e10])

    # 车辆电池-使用时间（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle Battery - Time In Service_4027')
    def test_caseid_1981641(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4027, SESSION.DEFAULT, '624027', check_range=[0x0, 0x0fff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4027, SESSION.EXTENDED, '624027', check_range=[0x0, 0x0fff])

    # 车辆电池充电状态-预估（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle Battery State Of Charge - Estimated_4028')
    def test_caseid_1981640(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4028, SESSION.DEFAULT, '624028', check_range=[0x0, 0x0fff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4028, SESSION.EXTENDED, '624028', check_range=[0x0, 0x0fff])

    # 汽车电池温度-预估（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle Battery Temperature - Estimated_4029')
    def test_caseid_1981639(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4029, SESSION.DEFAULT, '624029', check_range=[0x0, 0x01fa])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4029, SESSION.EXTENDED, '624029', check_range=[0x0, 0x01fa])

    # 车载电池电压（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle Battery Voltage_402A')
    def test_caseid_1981638(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x402a, SESSION.DEFAULT, '62402a', check_range=[0x0, 0xfa])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x402a, SESSION.EXTENDED, '62402a', check_range=[0x0, 0xfa])

    # 远程车辆IMMO密钥（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Remote Vehicle Immobilization Secret Key_408F')
    def test_caseid_1981637(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x408f, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x408f, SESSION.EXTENDED, '7f2233')

    # 远程车辆IMMO密钥（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Remote Vehicle Immobilization Secret Key_408F_L11')
    def test_caseid_1981636(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L11)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x408f, SESSION.EMPTY, '62408f', check_length=38)

    # 远程车辆IMMO密钥（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Remote Vehicle Immobilization Secret Key_408F')
    def test_caseid_1981635(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L11)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x408f, SESSION.EMPTY, UnLock.L0,
                                           '55555555555555555555555555555555', '62408f55555555555555555555555555555555',
                                           check_method=Check_Method.read, recover=False)
        self.sd_tester.reset_0x1181()
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L11)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x408f, SESSION.EMPTY, '62408f55555555555555555555555555555555')


    # 电池电流（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Current_4090')
    def test_caseid_1981634(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4090, SESSION.DEFAULT, '624090', check_range=[0xffee, 0x7fff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4090, SESSION.EXTENDED, '624090', check_range=[0xffee, 0x7fff])

    # 电池状态充电统计计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery State of Charge Statistics Counter_4094')
    def test_caseid_1981633(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4094, SESSION.DEFAULT, '624094', check_length=30,
                                          check_range=[0x00, 0xffff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4094, SESSION.EXTENDED, '624094', check_length=30,
                                          check_range=[0x00, 0xffff])

    # 电荷平衡统计计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Charge Balance Statistics Counter_40A2')
    def test_caseid_1981632(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40a2, SESSION.DEFAULT, '6240a2', check_length=30,
                                          check_range=[0x00, 0xffff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40a2, SESSION.EXTENDED, '6240a2', check_length=30,
                                          check_range=[0x00, 0xffff])

    # 自上次重置后的秒数（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Seconds since last reset_40AF')
    def test_caseid_1981631(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40af, SESSION.DEFAULT, '6240af', check_range=[0x00, 0xffff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40af, SESSION.EXTENDED, '6240af', check_range=[0x00, 0xffff])

    # 电池容量（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Capacity Relative_40B0')
    def test_caseid_1981630(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40b0, SESSION.DEFAULT, '6240b0', check_range=[0x00, 0xfa])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40b0, SESSION.EXTENDED, '6240b0', check_range=[0x00, 0xfa])

    # 低电量报警统计寄存器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Low Battery Warning Statistics Register_40CA')
    def test_caseid_1981629(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40ca, SESSION.DEFAULT, '6240ca', check_range=[0x00, 0xfa])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40ca, SESSION.EXTENDED, '6240ca', check_range=[0x00, 0xfa])

    # 电池传感器一致性检查（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Sensor Consistency Check_40CB')
    def test_caseid_1981628(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40cb, SESSION.DEFAULT, '6240cb', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40cb, SESSION.EXTENDED, '6240cb', check_in=[0x00, 0x01])

    # 充电模式（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Charge Mode_40D1')
    def test_caseid_1981627(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40d1, SESSION.DEFAULT, '6240d1', check_in=[0x00, 0x01, 0x02])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40d1, SESSION.EXTENDED, '6240d1', check_in=[0x00, 0x01, 0x02])

    # 电池静态电流-统计（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Quiescent Current - Statistics_40D7')
    def test_caseid_1981626(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40d7, SESSION.DEFAULT, '6240d7', check_range=[0x00, 0xffff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40d7, SESSION.EXTENDED, '6240d7', check_range=[0x00, 0xffff])

    # 可用Delta电源信号输出（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Available Delta Power signal output_40E2')
    def test_caseid_1981625(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40e2, SESSION.DEFAULT, '6240e2', check_range=[0x00, 0x7fff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40e2, SESSION.EXTENDED, '6240e2', check_range=[0x00, 0x7fff])

    # 配电继电器状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Distribution Relays Status_40E3')
    def test_caseid_1981624(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40e3, SESSION.DEFAULT, '6240e3')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40e3, SESSION.EXTENDED, '6240e3')

    # 电力系统故障计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Power System Fault Counters_40E4')
    def test_caseid_1981623(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40e4, SESSION.DEFAULT, '6240e4', check_length=36)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40e4, SESSION.EXTENDED, '6240e4', check_length=36)

    # 司机门状态诊断计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Driver Door Status Diagnostics Counter_40E8')
    def test_caseid_1981622(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40e8, SESSION.DEFAULT, '6240e8', check_range=[0x00, 0xff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40e8, SESSION.EXTENDED, '6240e8', check_range=[0x00, 0xff])

    # Immo状态历史（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Immo Status History_40EE')
    def test_caseid_1981621(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40ee, SESSION.DEFAULT, '6240ee', check_length=146)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40ee, SESSION.EXTENDED, '6240ee', check_length=146)

    # 闭锁命令记录（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Locking Command History_40EF')
    def test_caseid_1981620(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40ef, SESSION.DEFAULT, '6240ef', check_length=566)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40ef, SESSION.EXTENDED, '6240ef', check_length=566)

    # 解锁命令记录（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Unlocking Command History_40F0')
    def test_caseid_1981619(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40f0, SESSION.DEFAULT, '6240f0', check_length=566)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40f0, SESSION.EXTENDED, '6240f0', check_length=566)

    # 防玩计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Play protection counter_40F2')
    def test_caseid_1981618(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40f2, SESSION.DEFAULT, '6240f2', check_range=[0x0, 0xff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40f2, SESSION.EXTENDED, '6240f2', check_range=[0x0, 0xff])

    # 方向盘调整（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Steering Wheel Tuning_4109')
    def test_caseid_1981616(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4109, SESSION.DEFAULT, '624109')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4109, SESSION.EXTENDED, '624109')

    # 方向盘调整（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Steering Wheel Tuning_4109')
    def test_caseid_1981615(self):
        data = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4109, SESSION.EXTENDED, '624109')[6:]
        time.sleep(5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x2e,0x41,0x09,0x01],'6e4109')
        time.sleep(5)
        self.sd_tester.reset_0x1181()
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4109, SESSION.EXTENDED, '62410901')
        time.sleep(5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,f'2e4109{data}','6e4109')
        time.sleep(5)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4109, SESSION.EMPTY, f'624109{data}')

    # 日/夜和暮光传感器状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Day/Night And Twilight Sensors Status_410B')
    def test_caseid_1981614(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x410b, SESSION.DEFAULT, '62410b')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x410b, SESSION.EXTENDED, '62410b')

    # 车辆电源插口控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Power Outlet Control_4110')
    def test_caseid_1981613(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4110, SESSION.DEFAULT, '624110', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4110, SESSION.EXTENDED, '624110', check_in=[0x00, 0x01])

    # 请求充电电压（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Requested Charge Voltage_411D')
    def test_caseid_1981612(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x411d, SESSION.DEFAULT, '62411d')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x411d, SESSION.EXTENDED, '62411d')

    # 防盗报警触发源（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Alarm Trigger Information_416B')
    def test_caseid_1981611(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x416b, SESSION.DEFAULT, '62416b', check_length=206)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x416b, SESSION.EXTENDED, '62416b', check_length=206)

    # 室内灯光白天至黑夜计时器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Interior Light Day to Night Timer_416D')
    def test_caseid_1981610(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x416d, SESSION.DEFAULT, '62416d')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x416d, SESSION.EXTENDED, '62416d')

    # 室内灯光白天至黑夜计时器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Interior Light Day to Night Timer_416D')
    def test_caseid_1981609(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x416d, SESSION.EXTENDED, UnLock.L0, '2710', '62416d2710',
                                           check_method=Check_Method.reset)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'22416d','62416d')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e416d2710','6e416d')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22416d','62416d2710')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x416d, SESSION.EXTENDED, UnLock.L0,
                                           data,
                                           f'62416d{data}',
                                           check_method=Check_Method.read,recover=False)

    # 室内灯光黑夜至白天计时器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Interior Light Night to Day Timer_416E')
    def test_caseid_1981608(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x416e, SESSION.DEFAULT, '62416e')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x416e, SESSION.EXTENDED, '62416e')

    # 室内灯光黑夜至白天计时器（APP）failed
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Interior Light Night to Day Timer_416E')
    def test_caseid_1981607(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e416e2710','6e416e')
        time.sleep(30)
        self.io.io_reset_bgm(times=3)
        time.sleep(25)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22416e','62416e2710')
        time.sleep(25)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x416e, SESSION.EXTENDED, UnLock.L0, '2000',
                                           '6e416e', check_method=Check_Method.response, recover=False)
        time.sleep(10)
        self.sd_tester.reset_0x1181()
        time.sleep(10)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x416e, SESSION.EXTENDED, '62416e2000')
        

    # 在运输模式时的主电池计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Main Battery Counter In Transport Mode_4187')
    def test_caseid_1981606(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4187, SESSION.DEFAULT, '624187', check_range=[0x0000, 0xffff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4187, SESSION.EXTENDED, '624187', check_range=[0x0000, 0xffff])

    # 雨刷停止位状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Wiper Park Position Status_418F')
    def test_caseid_1981605(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x418f, SESSION.DEFAULT, '62418f', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x418f, SESSION.EXTENDED, '62418f', check_in=[0x00, 0x01])

    # 运输模式下电池的充电状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Transport Mode Battery State Of Charge_41CE')
    def test_caseid_1981604(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41ce, SESSION.DEFAULT, '6241ce')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41ce, SESSION.EXTENDED, '6241ce')

    # 内灯控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Interior Lights Control_41E5')
    def test_caseid_1981603(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41e5, SESSION.DEFAULT, '6241e5')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41e5, SESSION.EXTENDED, '6241e5')

    # 节电继电器控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Power Saver Relay Control_41E9')
    def test_caseid_1981602(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41e9, SESSION.DEFAULT, '6241e9', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41e9, SESSION.EXTENDED, '6241e9', check_in=[0x00, 0x01])

    # 车辆关闭返回到汽车模式计时器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Timer Vehicle Off Return To Car Mode_41F8')
    def test_caseid_1981601(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41f8, SESSION.DEFAULT, '6241f8', check_range=[0x00, 0xff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41f8, SESSION.EXTENDED, '6241f8', check_range=[0x00, 0xff])

    # 车辆关闭返回到汽车模式计时器（APP）reserved
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Timer Vehicle Off Return To Car Mode_41F8')
    def test_caseid_1981600(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x41f8, SESSION.EXTENDED, UnLock.L0, 'ff', '6241f8ff',
                                           check_method=Check_Method.read)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x41f8, SESSION.EXTENDED, UnLock.L0, '01', '6241f801',
                                           check_method=Check_Method.read)

    # 激活主驾侧后视镜除霜（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Activate Driver Side Mirror Defroster_4219')
    def test_caseid_1981599(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4219, SESSION.DEFAULT, '624219', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4219, SESSION.EXTENDED, '624219', check_in=[0x00, 0x01])

    # 激活副驾侧后视镜除霜（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Activate Passenger Side Mirror Defroster_421A')
    def test_caseid_1981598(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x421a, SESSION.DEFAULT, '62421a', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x421a, SESSION.EXTENDED, '62421a', check_in=[0x00, 0x01])

    # 激活电动前挡风玻璃（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Activate Electrical Front Windscreen_421D')
    def test_caseid_1981597(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x421d, SESSION.DEFAULT, '62421d', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x421d, SESSION.EXTENDED, '62421d', check_in=[0x00, 0x01])

    # 激活电动后挡风玻璃（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Activate Electrical Rear Window_421E')
    def test_caseid_1981596(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x421e, SESSION.DEFAULT, '62421e', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x421e, SESSION.EXTENDED, '62421e', check_in=[0x00, 0x01])

    # 控制台后按钮状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Overhead Console Rear Button Status_422F')
    def test_caseid_1981595(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x422f, SESSION.DEFAULT, '62422f',
                                          check_in=[0x00, 0x01, 0x10, 0x11])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x422f, SESSION.EXTENDED, '62422f', check_in=[0x00, 0x01])

    # 控制台按钮状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Overhead Console Button Status_4230')
    def test_caseid_1981594(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4230, SESSION.DEFAULT, '624230',
                                          check_in=[0x00, 0x01, 0x10, 0x11])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4230, SESSION.EXTENDED, '624230',
                                          check_in=[0x00, 0x01, 0x10, 0x11])

    # 车辆模式为工厂暂停模式计时器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Timer Car Mode Factory Pause_4231')
    def test_caseid_1981593(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4231, SESSION.DEFAULT, '624231', check_range=[0x00, 0xff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4231, SESSION.EXTENDED, '624231', check_range=[0x00, 0xff])

    # 车辆模式为工厂暂停模式计时器（APP）failed reserved
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Timer Car Mode Factory Pause_4231')
    def test_caseid_1981592(self):
        # # data = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4231, SESSION.EXTENDED, '624231')[6:]
        # # self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4231, SESSION.EMPTY, UnLock.L0, '15', '6e4231',
        # #                                    check_method=Check_Method.response, recover=False)
        # # time.sleep(1)
        # # self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4231, SESSION.EMPTY, '62423115')
        # # self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4231, SESSION.EMPTY, UnLock.L0, data, '6e4231',
        # #                                    check_method=Check_Method.response, recover=False)
        # # time.sleep(10)
        # self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        # data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'224231','624231')[6:]
        # self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e423115','6e4231')
        # time.sleep(35)
        # self.io.io_reset_bgm(times=3)
        # time.sleep(30)
        # self.sd_tester.send_data_and_check(TA.BGM_MCU,'224231','62423115')
        # self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4231, SESSION.EXTENDED, UnLock.L0,
        #                                    data,
        #                                    f'624231{data}',
        #                                    check_method=Check_Method.read,recover=False)
        pass

    # 延时进入车辆模式计时器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Delay to Enter Car Mode_4232')
    def test_caseid_1981591(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4232, SESSION.DEFAULT, '624232', check_range=[0x00, 0xff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4232, SESSION.EXTENDED, '624232', check_range=[0x00, 0xff])

    # 延时进入车辆模式计时器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Delay to Enter Car Mode_4232')
    def test_caseid_1981590(self):
        data = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4232, SESSION.EXTENDED, '624232')[6:]
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4232, SESSION.EMPTY, UnLock.L0, 'fe', '6e4232',
                                           check_method=Check_Method.response, recover=False)
        time.sleep(1)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4232, SESSION.EMPTY, '624232fe')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4232, SESSION.EMPTY, UnLock.L0, data, '6e4232',
                                           check_method=Check_Method.response, recover=False)

    # 雨水传感器高温检测（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Rain Sensor High Temperature Detected_4282')
    def test_caseid_1981589(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4282, SESSION.DEFAULT, '624282', check_range=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4282, SESSION.EXTENDED, '624282', check_range=[0x00, 0x01])

    # 雨水传感器高压检测（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Rain Sensor High Voltage Detected_4283')
    def test_caseid_1981588(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4283, SESSION.DEFAULT, '624283', check_range=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4283, SESSION.EXTENDED, '624283', check_range=[0x00, 0x01])

    # 解锁后的NFC持续时间（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)NFC duration after unlock_4297')
    def test_caseid_1981587(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4297, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4297, SESSION.EXTENDED, '624297', check_range=[0x00, 0xff])

    # 解锁后的NFC持续时间（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)NFC duration after unlock_4297')
    def test_caseid_1981586(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4297, SESSION.EXTENDED, UnLock.L11, '01', '62429701')
        self.mix.write_did_and_check(TA.BGM_MCU, 0x4297, SESSION.EXTENDED, UnLock.L11, '01', '62429701',check_method=Check_Method.kl30)

    # 电池平均静态电流-统计（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Average Quiescent Current - Statistics_42CD')
    def test_caseid_1981585(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42cd, SESSION.DEFAULT, '6242cd')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42cd, SESSION.EXTENDED, '6242cd')

    # 电池容量统计计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Capacity Statistics Counter_42CF')
    def test_caseid_1981584(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42cf, SESSION.DEFAULT, '6242cf')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42cf, SESSION.EXTENDED, '6242cf')

    # 电池内阻统计计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Internal Resistance Statistics Counter_42D1')
    def test_caseid_1981583(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42d1, SESSION.DEFAULT, '6242d1', check_length=50)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42d1, SESSION.EXTENDED, '6242d1', check_length=50)

    # 电池归一化内阻统计计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Normalized Internal Resistance Statistics Counter_42D2')
    def test_caseid_1981582(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42d2, SESSION.DEFAULT, '6242d2', check_length=50)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42d2, SESSION.EXTENDED, '6242d2', check_length=50)

    # 电池内阻（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Internal Resistance_42D3')
    def test_caseid_1981581(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42d3, SESSION.DEFAULT, '6242d3', check_length=26)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42d3, SESSION.EXTENDED, '6242d3', check_length=26)

    # 电池静态电流短时间滤波_低范围（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Quiescent Current Short Time Filtering_Low Range_42E3')
    def test_caseid_1981580(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42e3, SESSION.EMPTY, '6242e3')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42e3, SESSION.EXTENDED, '6242e3')

    # 电池平均静态电流_高范围（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Average Quiescent Current_High Range_42E4')
    def test_caseid_1981579(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42e4, SESSION.DEFAULT, '6242e4')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42e4, SESSION.EXTENDED, '6242e4')

    # 防盗报警状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Alarm Status_42E5')
    def test_caseid_1981578(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42e5, SESSION.DEFAULT, '6242e5', check_in=[0x00, 0x01, 0x02])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42e5, SESSION.EXTENDED, '6242e5', check_in=[0x00, 0x01, 0x02])

    # 中控锁防玩保护（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Central Locking Play Protection_42E9')
    def test_caseid_1981577(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42e9, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42e9, SESSION.EXTENDED, '6242e9', check_in=[0x01, 0x00])

    # 中控锁防玩保护（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Central Locking Play Protection_42E9')
    def test_caseid_1981576(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x42e9, SESSION.EXTENDED, UnLock.L0, '01', '6242e901')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'2242e9','6242e9')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e42e901','6e42e9')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2242e9','6242e901')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x42e9, SESSION.EXTENDED, UnLock.L0,
                                           data,
                                           f'6242e9{data}',
                                           check_method=Check_Method.read,recover=False)

    # Ajar开关状态（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Ajar Switch Status_42F2')
    def test_caseid_1981575(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42f2, SESSION.DEFAULT, '6242f2')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42f2, SESSION.EXTENDED, '6242f2')

    # 手套箱解锁状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Private Unlock Status_42F4')
    def test_caseid_1981574(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42f4, SESSION.DEFAULT, '6242f4', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42f4, SESSION.EXTENDED, '6242f4', check_in=[0x00, 0x01])

    # ITO信号频率状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)ITO Signal Frequency Status_42FB')
    def test_caseid_1981573(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42fb, SESSION.DEFAULT, '6242fb', check_range=[0x0000, 0xffff])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42fb, SESSION.EXTENDED, '6242fb', check_range=[0x0000, 0xffff])

    # 危险警报灯开关状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Hazard Switch Status_4300')
    def test_caseid_1981572(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4300, SESSION.DEFAULT, '624300', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4300, SESSION.EXTENDED, '624300', check_in=[0x00, 0x01])

    # IGN供电继电器反馈（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Ignition Power Relay Feedback_4305')
    def test_caseid_1981571(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4305, SESSION.DEFAULT, '624305')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4305, SESSION.EXTENDED, '624305')

    # 雨刮电机通信错误检测（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Wiper Motor Communication Error Detection_430B')
    def test_caseid_1981570(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x430b, SESSION.DEFAULT, '62430b', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x430b, SESSION.EXTENDED, '62430b', check_in=[0x00, 0x01])

    # 雨刮电机节点错误检测（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Wiper Motor Node Error Detection_430C')
    def test_caseid_1981569(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x430c, SESSION.DEFAULT, '62430c', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x430c, SESSION.EXTENDED, '62430c', check_in=[0x00, 0x01])

    # 使用模式扩展信息统计（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Usage Mode Extention Statistics_430E')
    def test_caseid_1981568(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x430e, SESSION.DEFAULT, '62430e', check_length=90)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x430e, SESSION.EXTENDED, '62430e', check_length=90)

    # 使用模式时间统计（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Usage Mode Time Statistics_430F')
    def test_caseid_1981567(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x430f, SESSION.DEFAULT, '62430f', check_length=60)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x430f, SESSION.EXTENDED, '62430f', check_length=60)

    # 燃油泵/碰撞控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Fuel Pump / crash relay Control_4310')
    def test_caseid_1981566(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4310, SESSION.DEFAULT, '624310', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4310, SESSION.EXTENDED, '624310', check_in=[0x00, 0x01])

    # 车轮测功器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Dynamometer Wheels_4313')
    def test_caseid_1981565(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4313, SESSION.DEFAULT, '624313', check_in=[0x01, 0x02])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4313, SESSION.EXTENDED, '624313', check_in=[0x01, 0x02])

    # 车轮测功器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Dynamometer Wheels_4313')
    def test_caseid_1981564(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4313, SESSION.EXTENDED, UnLock.L0, '01', '62431301')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4313, SESSION.EXTENDED, UnLock.L0, '02', '62431302')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'224313','624313')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e431301','6e4313')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'224313','62431301')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4313, SESSION.EXTENDED, UnLock.L0,
                                           data,
                                           f'624313{data}',
                                           check_method=Check_Method.read,recover=False)

    # 雨刮单次挂水（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Single Stroke Wiping_4328')
    def test_caseid_1981563(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4328, SESSION.DEFAULT, '624328', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4328, SESSION.EXTENDED, '624328', check_in=[0x00, 0x01])

    # 室内灯光脚灯状态反馈（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Interior Light Footwell Status Feedback_432D')
    def test_caseid_1981562(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x432D, SESSION.DEFAULT, '62432d')
        assert int(p1[6:8], 16) in [0, 1, 3, 4] and 0 <= int(p1[8:12], 16) * 0.001 <= 25.576 and int(p1[12:],
                                                                                                     16) in range(0,
                                                                                                                  65536)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x432D, SESSION.EXTENDED, '62432d')
        # pass

    # 空调继电器控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Climate Relay Control_432E')
    def test_caseid_1981561(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x432e, SESSION.DEFAULT, '62432e', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x432e, SESSION.EXTENDED, '62432e', check_in=[0x00, 0x01])

    # 运输模式下低压电池SoC（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Low Battery SoC in Transport Mode_433E')
    def test_caseid_1981560(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x433e, SESSION.DEFAULT, '62433e', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x433e, SESSION.EXTENDED, '62433e', check_in=[0x00, 0x01])

    # 外灯继电器控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Exterior Light Relay Control_439F')
    def test_caseid_1981559(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x439f, SESSION.DEFAULT, '62439f')
        pl = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x439f, SESSION.EXTENDED, '62439f')
        assert 0 <= int(pl[6:8], 16) <= 255, '前外灯继电器返回值不在0-255内'
        assert 0 <= int(pl[8:], 16) <= 255, '后外灯继电器返回值不在0-255内'

    # 雨量传感器重新采用（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Rain Sensor ReAdaption_43B8')
    def test_caseid_1981558(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x43b8, SESSION.DEFAULT, '6243b8', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x43b8, SESSION.EXTENDED, '6243b8', check_in=[0x00, 0x01])

    # 车辆模式包括子状态（APP）
    # BGM_MCU 03/l3才可读
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Car Mode including subtypes_43C4')
    def test_caseid_1981557(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x43c4, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x43c4, SESSION.EXTENDED, '7f2233')
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EMPTY, UnLock.L3)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x43c4, SESSION.EMPTY, '6243c4',
                                          check_in=[0x00, 0x01, 0x02, 0x03, 0x08, 0x10, 0x18, 0x28, 0x29])

    # SWDL的门状态和锁状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Door and Lock status for SWDL_43D6')
    def test_caseid_1981556(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x43d6, SESSION.DEFAULT, '6243d6',
                                          check_in=[0x00, 0x01, 0x02, 0x03, 0x04])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x43d6, SESSION.EXTENDED, '6243d6',
                                          check_in=[0x00, 0x01, 0x02, 0x03, 0x04])

    # 工厂模式下低压电池SOC（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Low Battery SoC In Factory Mode_4516')
    def test_caseid_1981553(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4516, SESSION.DEFAULT, '624516', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4516, SESSION.EXTENDED, '624516', check_in=[0x00, 0x01])

    # IMMO管理状态
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Immobilize Mangement status_45A1')
    def test_caseid_1981552(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x45a1, SESSION.DEFAULT, '6245a1',
                                          check_in=[0x00, 0x01, 0x02, 0x03])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x45a1, SESSION.EXTENDED, '6245a1',
                                          check_in=[0x00, 0x01, 0x02, 0x03])

    # 雨量传感器阈值（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Rain Sensor Threshold value_45A4')
    def test_caseid_1981551(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x45a4, SESSION.DEFAULT, '6245a4')
        assert -40 <= int(p1[7:], 16) * 5 - 40 <= 35
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x45a4, SESSION.EXTENDED, '6245a4')

    # 雨量传感器阈值（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Rain Sensor Threshold value_45A4')
    def test_caseid_1981550(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x45a4, SESSION.EXTENDED, UnLock.L11, '01', '6245a401')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x45a4, SESSION.EXTENDED, UnLock.L11, '0f', '6245a40f')
        self.mix.write_did_and_check(TA.BGM_MCU, 0x45a4, SESSION.EXTENDED, UnLock.L11, '0f', '6245a40f',check_method=Check_Method.kl30)

    # 车窗短降（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Windows Short Drop_45BF')
    def test_caseid_1981549(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x45bf, SESSION.DEFAULT, '6245bf', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x45bf, SESSION.EXTENDED, '6245bf', check_in=[0x00, 0x01])

    # 外灯状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Exterior Lighting Status_7000')
    def test_caseid_1981548(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x7000, SESSION.DEFAULT, '627000', check_length=38)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x7000, SESSION.EXTENDED, '627000', check_length=38)

    # 外灯控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Exterior Lights Control_7022')
    def test_caseid_1981547(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x7022, SESSION.DEFAULT, '627022', check_length=12)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x7022, SESSION.EXTENDED, '627022', check_length=12)

    # L11/L12安全常数（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Security Constant Level 11/12_D12F')
    def test_caseid_1981546(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd12f, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd12f, SESSION.EXTENDED, '7f2233')

    # L11/L12安全常数（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Security Constant Level 11/12_L11_D12F')
    def test_caseid_1981545(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L11)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd12f, SESSION.EMPTY, '62d12f', check_length=16)

    # L11/L12安全常数（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Security Constant Level 11/12_D12F')
    def test_caseid_1981544(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L11)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xd12f, SESSION.EMPTY, UnLock.L0, 'ffffffffff',
                                           '62d12fffffffffff', check_method=Check_Method.read, recover=False)
        self.sd_tester.reset_0x1181()
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L11)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd12f, SESSION.EMPTY, '62d12fffffffffff')

    # 车辆模式（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Car Mode_D134')
    def test_caseid_1981543(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd134, SESSION.DEFAULT, '62d134', check_length=8)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd134, SESSION.EXTENDED, '62d134',
                                          check_length=8)  # check_in=['01','02']

    # BNCM和BGM的安全密钥（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Security Key between BNCM and BGM (Digital Key)_D903/Erase_D905')
    def test_caseid_1981542(self):
        self.sd_tester.write_bncm_key(bncm_key=self.tc_config['BNCM_KEY'])

    # BNCM和BGM的安全密钥（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Security Key between BNCM and BGM (Digital Key)_D904')
    def test_caseid_1981541(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd904, SESSION.DEFAULT, '62d904', check_length=8,
                                          check_in=[0x00, 0x01])  # 62d90400 未写入 or 62d90401 已写入
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd904, SESSION.EXTENDED, '62d904', check_length=8,
                                          check_in=[0x00, 0x01])

    # BNCM和BGM的安全密钥的擦除状态（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Security Key between BNCM and BGM (Digital Key) Erase_D905')
    def test_caseid_1981540(self):
        self.sd_tester.write_bncm_key(bncm_key=self.tc_config['BNCM_KEY'])

    # BNCM和BGM的安全密钥的Mac状态（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Security Key between BNCM and BGM (Digital Key) Mac_D906')
    def test_caseid_1981539(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd906, SESSION.DEFAULT, '62d906', check_length=70)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd906, SESSION.EXTENDED, '62d906', check_length=70)

    # 电池可用Delta能量（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Available Delta Energy_D934')
    def test_caseid_1981538(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd934, SESSION.DEFAULT, '62d934')
        assert -16 <= int(p1[6:], 16) - 16 <= 47
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd934, SESSION.EXTENDED, '62d934')

    # 电池能量可用警告（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Energy Available To Warning_D935')
    def test_caseid_1981537(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd935, SESSION.DEFAULT, '62d935')
        assert -16 <= int(p1[6:], 16) - 16 <= 47
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd935, SESSION.EXTENDED, '62d935')

    # VFC Vector框架设置（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)VFCVectorFrame Setting_E503')
    def test_caseid_1981536(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xe503, SESSION.DEFAULT, '62e503', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xe503, SESSION.EXTENDED, '62e503', check_in=[0x00, 0x01])

    # VFC Vector框架设置（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)VFCVectorFrame Setting_E503')
    def test_caseid_1981535(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xe503, SESSION.EXTENDED, UnLock.L5, '01', '62e50301')
        self.mix.write_did_and_check(TA.BGM_MCU, 0xe503, SESSION.EXTENDED, UnLock.L5, '01', '62e50301',check_method=Check_Method.kl30)

    # 后备箱供电状态反馈（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Luggage Supply Status Feedback_EE94')
    def test_caseid_1981534(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xee94, SESSION.DEFAULT, '62ee94')
        assert 0 <= int(p1[6:10], 16) <= 4292967295
        assert 0 <= int(p1[10:14], 16) <= 4292967295
        assert 0 <= int(p1[14:18], 16) <= 4292967295
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xee94, SESSION.EXTENDED, '62ee94')

    # 喇叭统计信息（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Statistic Information for Horn_EE99')
    def test_caseid_1981533(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xee99, SESSION.DEFAULT, '62ee99')
        assert 0 <= int(p1[6:10], 16) <= 4292967295
        assert 0 <= int(p1[10:14], 16) <= 4292967295
        assert 0 <= int(p1[14:18], 16) <= 4292967295
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xee99, SESSION.EXTENDED, '62ee99')

    # 后挡风玻璃加热器控制#1（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Rear Windscreen Heater Control #1_EF99')
    def test_caseid_1981532(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xef99, SESSION.DEFAULT, '62ef99', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xef99, SESSION.EXTENDED, '62ef99', check_in=[0x00, 0x01])

    # BGM唤醒原因（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)BGM Wake Up Cause_F010')
    def test_caseid_1981531(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf010, SESSION.DEFAULT, '62f010',check_length=306)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf010, SESSION.EXTENDED, '62f010',check_length=306)

    # BGM保持唤醒的原因（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)BGM Keep Active Cause_F011')
    def test_caseid_1981530(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf011, SESSION.DEFAULT, '62f011')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf011, SESSION.EXTENDED, '62f011')

    # 专用ECU交付总成部件编号（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Private ECU(s) Delivery Assembly Part Number(s)_F1BB')
    def test_caseid_1981529(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1bb, SESSION.DEFAULT, '62f1bb', check_length=440)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1bb, SESSION.EXTENDED, '62f1bb', check_length=440)

    # 转向灯诊断状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Direction Indication Diagnostics Status_FD07')
    def test_caseid_1981527(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xfd07, SESSION.DEFAULT, '62fd07')
        assert int(p1[6:], 16) == 0 or int(p1[6:], 16) == 1
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xfd07, SESSION.EXTENDED, '62fd07')

    # 以太网链接状态（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Ethernet Link Status_D250')
    def test_caseid_1981526(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd250, SESSION.DEFAULT, '62d250')
        assert 0 <= int(p1[6:8], 16) <= 255
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd250, SESSION.EXTENDED, '62d250')

    # 单一质量指数（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Single Quality Index_D260')
    def test_caseid_1981525(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd260, SESSION.DEFAULT, '62d260')
        assert 0 <= int(p1[6:8], 16) <= 7
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd260, SESSION.EXTENDED, '62d260')

    # 控制WMM激活前洗涤（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Activate frontwasher_420A')
    def test_caseid_1981524(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x420a, SESSION.DEFAULT, '62420a',
                                          check_in=[0x00, 0x01, 0x02, 0x03])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x420a, SESSION.EXTENDED, '62420a',
                                          check_in=[0x00, 0x01, 0x02, 0x03])

    # 从CDC来的雨刮挡位信息（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Wiper’s lever information from CDC_4218')
    def test_caseid_1981523(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4218, SESSION.DEFAULT, '624218')
        assert int(p1[6:8], 16) in [0, 1, 2, 3, 4, 5, 6, 7]
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4218, SESSION.EXTENDED, '624218')

    # 智能补电使能（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Voltage Wake Up Charging At Sleep Enable_4530')
    def test_caseid_1981522(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4530, SESSION.DEFAULT, '624530', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4530, SESSION.EXTENDED, '624530', check_in=[0x00, 0x01])

    # 智能补电使能（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Voltage Wake Up Charging At Sleep Enable_4530')
    def test_caseid_1981521(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4530, SESSION.EXTENDED, UnLock.L5, '01', '62453001')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'224530','624530')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e453001','6e4530')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'224530','62453001')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4530, SESSION.EXTENDED, UnLock.L5,
                                           data,
                                           f'624530{data}',
                                           check_method=Check_Method.read,recover=False)

    # 智能补电电压（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Voltage Wake Up Charging At Sleep_4531')
    def test_caseid_1981520(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4531, SESSION.DEFAULT, '624531')
        assert 8 <= int(p1[6:8], 16) / 10 <= 16
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4531, SESSION.EXTENDED, '624531')

    # 智能补电电压（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Voltage Wake Up Charging At Sleep_4531')
    def test_caseid_1981519(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4531, SESSION.EXTENDED, UnLock.L5, '77', '62453177')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'224531','624531')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e453177','6e4531')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'224531','62453177')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4531, SESSION.EXTENDED, UnLock.L5,
                                           data,
                                           f'624531{data}',
                                           check_method=Check_Method.read,recover=False)

    # 智能补电定时器使能（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Timer Wake Up Charging At Sleep Enable_4532')
    def test_caseid_1981518(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4532, SESSION.DEFAULT, '624532', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4532, SESSION.EXTENDED, '624532', check_in=[0x00, 0x01])

    # 智能补电定时器使能（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Timer Wake Up Charging At Sleep Enable_4532')
    def test_caseid_1981517(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4532, SESSION.EXTENDED, UnLock.L5, '01', '62453201')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'224532','624532')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e453201','6e4532')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'224532','62453201')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4532, SESSION.EXTENDED, UnLock.L5,
                                           data,
                                           f'624532{data}',
                                           check_method=Check_Method.read,recover=False)

    # 停车时的原始能量可用充电中止（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Prim Energy Available Charge Required for Parked_4533')
    def test_caseid_1981516(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4533, SESSION.DEFAULT, '624533')
        assert 0 <= int(p1[6:], 16) <= 127
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4533, SESSION.EXTENDED, '624533')

    # 停车时的原始能量可用充电中止（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Prim Energy Available Charge Required for Parked_4533')
    def test_caseid_1981515(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4533, SESSION.EXTENDED, UnLock.L5, '50', '62453350')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'224533','624533')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e453350','6e4533')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'224533','62453350')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4533, SESSION.EXTENDED, UnLock.L5,
                                           data,
                                           f'624533{data}',
                                           check_method=Check_Method.read,recover=False)

    # inactive下充电电压值（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Voltage Value Charging At Inactive_4534')
    def test_caseid_1981514(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4534, SESSION.DEFAULT, '624534')
        assert 8 <= int(p1[6:], 16) / 10 <= 16
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4534, SESSION.EXTENDED, '624534')

    # inactive下充电电压值（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Voltage Value Charging At Inactive_4534')
    def test_caseid_1981513(self):
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4534, SESSION.EXTENDED, UnLock.L5, '50', '62453450')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'224534','624534')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e453450','6e4534')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'224534','62453450')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4534, SESSION.EXTENDED, UnLock.L5,
                                           data,
                                           f'624534{data}',
                                           check_method=Check_Method.read,recover=False)
        # data=self.sd_tester.read_did_and_check(TA.BGM_MCU,0x4534,SESSION.EXTENDED,'624534')[6:]
        # self.sd_tester.write_did_and_check(TA.BGM_MCU,0x4534,SESSION.EXTENDED,UnLock.L5,'50','6e4534',check_method=Check_Method.response,recover=False)
        # time.sleep(1)
        # self.sd_tester.read_did_and_check(TA.BGM_MCU,0x4534,SESSION.EXTENDED,'62453450')
        # self.sd_tester.write_did_and_check(TA.BGM_MCU,0x4534,SESSION.EXTENDED,UnLock.L5,data,'6e4534',check_method=Check_Method.response,recover=False)

    # 停车时的原始能量可用充电（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Prim Energy Available Charge Required for Parked_4535')
    def test_caseid_1981512(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4535, SESSION.DEFAULT, '624535')
        assert 0 <= int(p1[6:], 16) <= 127
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4535, SESSION.EXTENDED, '624535')

    # 停车时的原始能量可用充电（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Prim Energy Available Charge Required for Parked_4535')
    def test_caseid_1981511(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4535, SESSION.EXTENDED, UnLock.L5, '50', '62453550')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'224535','624535')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e453550','6e4535')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'224535','62453550')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4535, SESSION.EXTENDED, UnLock.L5,
                                           data,
                                           f'624535{data}',
                                           check_method=Check_Method.read,recover=False)

    # 低压能量等级替代（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Energy Level Electric Substitution_429D')
    def test_caseid_1981510(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429d, SESSION.DEFAULT, '62429d')
        assert 0 <= int(p1[6:], 16) <= 15
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429d, SESSION.EXTENDED, '62429d')

    # 低压功率等级替代（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Power Level Electric Substitution_429E')
    def test_caseid_1981509(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429e, SESSION.DEFAULT, '62429e')
        assert 0 <= int(p1[6:], 16) <= 15
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429e, SESSION.EXTENDED, '62429e')

    # 局部网络管理集群PNC（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Partial Network Cluster (PNC)_DD0B')
    def test_caseid_1981508(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd0b, SESSION.DEFAULT, '62dd0b')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd0b, SESSION.EXTENDED, '62dd0b')

    # FOTA状态（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)FotaStatus_F153')
    def test_caseid_1981507(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf153, SESSION.DEFAULT, '62f153',
                                          check_in=[0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf153, SESSION.EXTENDED, '62f153',
                                          check_in=[0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06])

    # FOTA状态（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)FotaStatus_F153')
    def test_caseid_1981506(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xf153, SESSION.EXTENDED, UnLock.L5, '01', '62f15301',
                                           check_method=Check_Method.read, recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xf153, SESSION.EMPTY, UnLock.L0, '02', '62f15302',
                                           check_method=Check_Method.read, recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xf153, SESSION.EMPTY, UnLock.L0, '03', '62f15303',
                                           check_method=Check_Method.read, recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xf153, SESSION.EMPTY, UnLock.L0, '04', '62f15304',
                                           check_method=Check_Method.read, recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xf153, SESSION.EMPTY, UnLock.L0, '05', '62f15305',
                                           check_method=Check_Method.read, recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xf153, SESSION.EXTENDED, UnLock.L5, '06', '62f15306',
                                           check_method=Check_Method.reset)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'22f153','62f153')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2ef15301','6ef153')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22f153','62f15301')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xf153, SESSION.EXTENDED, UnLock.L5,
                                           data,
                                           f'62f153{data}',
                                           check_method=Check_Method.read,recover=False)
        

    # 后备箱打开/关闭计数器
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Tailgate/bootlid Open/Close Counter_A00A')
    def test_caseid_1981505(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xa00a, SESSION.DEFAULT, '62a00a')
        i = 0
        j = 6
        for i in range(0, 11):
            assert int(p1[j: j + 2], 16) in range(0, 65536), "out of range"
            i += 1
            j = j + 2
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xa00a, SESSION.EXTENDED, '62a00a')

    # 数字钥匙当前UTC时间
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Digital Key Current UTC Time_C008')
    def test_caseid_1981504(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xc008, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xc008, SESSION.EXTENDED, '7f2233')

    # 数字钥匙当前UTC时间
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Digital Key Current UTC Time_L5_C008')
    def test_caseid_1981503(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU, SESSION.EXTENDED, UnLock.L5, check_data='6706')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xc008, SESSION.EMPTY, '62c008', check_length=14)

    # TPMS传感器IDs（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Tire Pressure Monitoring System (TPMS) Sensor IDs_281F')
    def test_caseid_1981502(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x281f, SESSION.DEFAULT, '62281f')
        assert 0 <= int(p1[6:14], 16) <= 4294967294
        assert 0 <= int(p1[14:22], 16) <= 4294967294
        assert 0 <= int(p1[22:30], 16) <= 4294967294
        assert 0 <= int(p1[30:], 16) <= 4294967294
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x281f, SESSION.EXTENDED, '62281f')

    # TPMS传感器IDs（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Tire Pressure Monitoring System (TPMS) Sensor IDs_281F')
    def test_caseid_1981501(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x281f, SESSION.EXTENDED, UnLock.L5,
                                           '00000000000000000000000000000000', '62281f00000000000000000000000000000000')
        self.mix.write_did_and_check(TA.BGM_MCU, 0x281f, SESSION.EXTENDED, UnLock.L5,
                                           '00000000000000000000000000000000', '62281f00000000000000000000000000000000',check_method=Check_Method.kl30)

    # 转向灯优先级（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)DI Priority_F108')
    def test_caseid_1981500(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4533, SESSION.DEFAULT, '624533', check_length=8)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4533, SESSION.EXTENDED, '624533', check_length=8)

    # Sensata TPMS软件版本（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Sensata TPMS Software Version_4503')
    def test_caseid_1981499(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4503, SESSION.DEFAULT, '624503')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4503, SESSION.EXTENDED, '624503')

    # TPMS开发帧状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)TPMS Development log message status_4504')
    def test_caseid_1981498(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4504, SESSION.DEFAULT, '624504',
                                          check_in=[0x00, 0x01, 0x02, 0x03, 0x04])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, '624504',
                                          check_in=[0x00, 0x01, 0x02, 0x03, 0x04])

    # TPMS开发帧状态（APP）存在7f2e31的情况
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E))TPMS Development log message status_4504')
    def test_caseid_1981497(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EXTENDED, UnLock.L5, '01', '6e4504',
                                           check_method=Check_Method.response, recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EMPTY, UnLock.L5, '02', '6e4504',
                                           check_method=Check_Method.response, recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EMPTY, UnLock.L5, '03', '6e4504',
                                           check_method=Check_Method.response, recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EMPTY, UnLock.L5, '04', '6e4504',
                                           check_method=Check_Method.response, recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4504, SESSION.EMPTY, UnLock.L5, '00', '6e4504',
                                           check_method=Check_Method.response, recover=False)


    # 调节内灯目标亮度值的系统状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Adjust the system state of Interiorlight target value_4600')
    def test_caseid_1981496(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4600, SESSION.DEFAULT, '624600')
        assert 0 <= int(p1[6:8], 16) <= 100
        assert 0 <= int(p1[8:10], 16) <= 100
        assert 0 <= int(p1[10:12], 16) <= 100
        assert 0 <= int(p1[12:14], 16) <= 100
        assert 0 <= int(p1[14:], 16) <= 100
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4600, SESSION.EXTENDED, '624600')

    # 调节内灯目标亮度值的系统状态（APP）存在恢复失败的情况
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Adjust the system state of Interiorlight target value_4600')
    def test_caseid_1981495(self):
        # data=self.sd_tester.read_did_and_check(TA.BGM_MCU,0x4600,SESSION.EXTENDED,'624600')[6:]
        # self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4600, SESSION.EXTENDED, UnLock.L5, '0064323c64',
        #                                    '6246000064000064',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4600, SESSION.EXTENDED, UnLock.L5, '0000000001',
                                           '6e4600',check_method=Check_Method.response,recover=False)
        time.sleep(10)
        self.sd_tester.reset_0x1181()
        time.sleep(10)
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0x4600,SESSION.EXTENDED,'6246000000000001')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e46000064323c64','6e4600')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0x4600,SESSION.EXTENDED,'6246000064323c64')

    # 内灯白天至黑夜值（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Interior Light Day to Night Value_416F')
    def test_caseid_1981494(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x416f, SESSION.DEFAULT, '62416f')
        assert 400 <= int(p1[6:], 16) <= 700
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x416f, SESSION.EXTENDED, '62416f')

    # 内灯白天至黑夜值（APP）存在recover失败的情况，写成功，但没写进去
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Interior Light Day to Night Value_416F')
    def test_caseid_1981493(self):
        data = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x416f, SESSION.EMPTY, '62416f')[6:]
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x416f, SESSION.EXTENDED, UnLock.L5, '0190', '62416f0190',
                                           recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x416f, SESSION.EXTENDED, UnLock.L5, data, '6e416f',
                                           check_method=Check_Method.response, recover=False)

    # 内灯黑夜至白天值（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Interior Light Night to Day Value_4170')
    def test_caseid_1981492(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4170, SESSION.DEFAULT, '624170')
        assert 800 <= int(p1[6:], 16) <= 1300
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4170, SESSION.EXTENDED, '624170')

    # 内灯黑夜至白天值（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Interior Light Night to Day Value_4170')
    def test_caseid_1981491(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4170, SESSION.EXTENDED, UnLock.L5, '0320', '6241700320')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'224170','624170')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e41700320','6e4170')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'224170','6241700320')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4170, SESSION.EXTENDED, UnLock.L5,
                                           data,
                                           f'624170{data}',
                                           check_method=Check_Method.read,recover=False)

    # AWM LIN消息检测（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)AWM LIN Message Detection_DA00')
    def test_caseid_1981490(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xda00, SESSION.DEFAULT, '62da00', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xda00, SESSION.EXTENDED, '62da00', check_in=[0x00, 0x01])

    # 展车模式（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Exhibition Mode_D135')
    def test_caseid_1981489(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd135, SESSION.DEFAULT, '62d135', check_in=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd135, SESSION.EXTENDED, '62d135', check_in=[0x00, 0x01])

    # 展车模式（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Exhibition Mode_D135')
    def test_caseid_1981488(self):
        data = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd135, SESSION.EXTENDED,'62d135')[6:]
        time.sleep(5)
        self.sd_tester.unlock_and_check(0x1002,SESSION.EMPTY,UnLock.L5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,[0x2e,0xd1,0x35,0x01],'6ed135')
        time.sleep(5)
        self.sd_tester.reset_0x1181()
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd135, SESSION.EXTENDED, '62d13501')
        time.sleep(5)
        self.sd_tester.unlock_and_check(0x1002,SESSION.EMPTY,UnLock.L5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,f'2ed135{data}','6ed135')
        time.sleep(5)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd135, SESSION.EMPTY, f'62d135{data}')

    # 方向盘加热控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Steering Wheel Heating Control_7023')
    def test_caseid_1981487(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x7023, SESSION.DEFAULT, '627023')
        assert 0 <= int(p1[6:10], 16) <= 600
        assert 0 <= int(p1[10:14], 16) <= 600
        assert 0 <= int(p1[14:16], 16) * 0.1 <= 10
        assert 0 <= int(p1[16:18], 16) * 0.1 <= 10
        assert 0 <= int(p1[18:20], 16) * 0.5 <= 60
        assert 0 <= int(p1[20:22], 16) * 0.5 <= 60
        assert 0 <= int(p1[22:], 16) * 0.5 <= 60
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x7023, SESSION.EXTENDED, '627023')

    # 方向盘加热控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Steering Wheel Heating Control_7023')
    def test_caseid_1981486(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x7023, SESSION.EXTENDED, UnLock.L5, '010101010101010101',
                                           '627023010101010101010101')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'227023','627023')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e7023010101010101010101','6e7023')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'227023','627023010101010101010101')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x7023, SESSION.EXTENDED, UnLock.L5,
                                           data,
                                           f'627023{data}',
                                           check_method=Check_Method.read,recover=False)

    # AWM初始化激活触发计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)The counter of trigger to active AWM initialization_4200')
    def test_caseid_1981485(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4200, SESSION.DEFAULT, '624200')
        assert 0 <= int(p1[6:10], 16) <= 500, '电动尾翼展开次数上限超过0-500'
        assert 0 <= int(p1[10:], 16) <= 500, '电动尾翼收回次数上限超过0-500'
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4200, SESSION.EXTENDED, '624200')

    # AWM初始化激活触发计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)The counter of trigger to active AWM initialization_4200')
    def test_caseid_1981484(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4200, SESSION.EXTENDED, UnLock.L5, '00000000',
                                           '62420000000000')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x4200, SESSION.EXTENDED, UnLock.L5, '01f401f4',
                                           '62420001f401f4')
        self.mix.write_did_and_check(TA.BGM_MCU, 0x4200, SESSION.EXTENDED, UnLock.L5, '01f401f4',
                                           '62420001f401f4',check_method=Check_Method.kl30)

    # PowerManagement可标定数据（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Power Management Config_F0F5')
    def test_caseid_1981483(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf0f5, SESSION.DEFAULT, '62f0f5')
        assert 0 <= int(p1[6:8], 16) <= 40
        assert 0 <= int(p1[8:10], 16) <= 20
        assert 0 <= int(p1[10:12], 16) <= 10
        assert 0 <= int(p1[12:14], 16) <= 10
        assert 0 <= int(p1[14:16], 16) <= 5
        assert 0 <= int(p1[16:], 16) <= 10
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf0f5, SESSION.EXTENDED, '62f0f5')

    # 转向灯角度自动关闭触发角度配置值_Max（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)AutoOffAg_Max_7024')
    def test_caseid_1981481(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x7024, SESSION.DEFAULT, '627024')
        assert 0 <= int(p1[6:], 16) <= 255
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x7024, SESSION.EXTENDED, '627024')

    # 转向灯角度自动关闭触发角度配置值_Max（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)AutoOffAg_Max_7024')
    def test_caseid_1981480(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x7024, SESSION.EMPTY, UnLock.L5, '01', '62702401',
                                           recover=False)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'227024','627024')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e702401','6e7024')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'227024','62702401')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x7024, SESSION.EXTENDED, UnLock.L5,
                                           data,
                                           f'627024{data}',
                                           check_method=Check_Method.read,recover=False)

    # 转向灯角度自动关闭关闭角度配置值_Min（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)AutoOffAg_Min_7025')
    def test_caseid_1981479(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x7025, SESSION.PROGRAMMING, '7f2231')

    # 转向灯角度自动关闭触发角度配置值_Min（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)AutoOffAg_Min_7025')
    def test_caseid_1981478(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x7025, SESSION.EXTENDED, UnLock.L5, '01', '62702501')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'227025','627025')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e702501','6e7025')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'227025','62702501')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x7025, SESSION.EXTENDED, UnLock.L5,
                                           data,
                                           f'627025{data}',
                                           check_method=Check_Method.read,recover=False)
        
    # BGM计算的小电池SOC值（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)BattSoc2Fild（Vehicle Battery State Of Charge-BGM）_4444')
    def test_caseid_1981477(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4444, SESSION.DEFAULT, '624444')
        assert 0 <= int(p1[6:], 16) * 0.1 <= 100
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4444, SESSION.EXTENDED, '624444')

    # SALM灯带休眠（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)SALM Sleep_D136')
    def test_caseid_1981475(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd136, SESSION.DEFAULT, '62d136')
        assert 0 <= int(p1[6:8], 16) <= 2, 'value out of range'
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd136, SESSION.EXTENDED, '62d136')

    # 开始补电的小电池SOC阈值
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb00')
    def test_caseid_1984767(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb00, SESSION.DEFAULT, '62bb00')
        assert 0 <= int(p1[6:8], 16) <= 100, 'value out of range'
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb00, SESSION.EXTENDED, '62bb00')

    # 开始补电的小电池SOC阈值
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)PrmEgyAvlDchaChrgnStartParked_bb00')
    def test_caseid_1984766(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xBB00, SESSION.EXTENDED, UnLock.L3, '00', '62bb0000')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb00','62bb00')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2ebb0000','6ebb00')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb00','62bb0000')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xbb00, SESSION.EXTENDED, UnLock.L3,
                                           data,
                                           f'62bb00{data}',
                                           check_method=Check_Method.read,recover=False)

    # BMS低SOC唤醒网络设置
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb01')
    def test_caseid_1984761(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb01, SESSION.DEFAULT, '62bb01', check_range=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb01, SESSION.EXTENDED, '62bb01', check_range=[0x00, 0x01])

    # BMS低SOC唤醒网络设置
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)PrmEgyAvlDchaChrgnStartParked_bb01')
    def test_caseid_1984760(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xBB01, SESSION.EXTENDED, UnLock.L3, '01', '62bb0101')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb01','62bb01')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2ebb0101','6ebb01')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb01','62bb0101')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xbb01, SESSION.EXTENDED, UnLock.L3,
                                           data,
                                           f'62bb01{data}',
                                           check_method=Check_Method.read,recover=False)

    # BMS唤醒网络的SOC阈值
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb02')
    def test_caseid_1984765(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb02, SESSION.DEFAULT, '62bb02')
        assert 0 <= int(p1[6:8], 16) <= 100, 'value out of range'
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb02, SESSION.EXTENDED, '62bb02')

    # BMS唤醒网络的SOC阈值
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)PrmEgyAvlDchaChrgnStartParked_bb02')
    def test_caseid_1984764(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xBB02, SESSION.EXTENDED, UnLock.L3, '00', '62bb0200')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb02','62bb02')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2ebb0200','6ebb02')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb02','62bb0200')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xbb02, SESSION.EXTENDED, UnLock.L3,
                                           data,
                                           f'62bb02{data}',
                                           check_method=Check_Method.read,recover=False)

    # BMS低电压唤醒网络设置
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb03')
    def test_caseid_1984759(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb03, SESSION.DEFAULT, '62bb03', check_range=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb03, SESSION.EXTENDED, '62bb03', check_range=[0x00, 0x01])

    # BMS低电压唤醒网络设置
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)PrmEgyAvlDchaChrgnStartParked_bb03')
    def test_caseid_1984758(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xBB03, SESSION.EXTENDED, UnLock.L3, '01', '62bb0301')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb03','62bb03')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2ebb0301','6ebb03')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb03','62bb0301')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xbb03, SESSION.EXTENDED, UnLock.L3,
                                           data,
                                           f'62bb03{data}',
                                           check_method=Check_Method.read,recover=False)

    # BMS唤醒网络的电压阈值
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb04')
    def test_caseid_1984763(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb04, SESSION.DEFAULT, '62bb04')
        assert 80 <= int(p1[6:8], 16) <= 160, 'value out of range'
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb04, SESSION.EXTENDED, '62bb04')

    # BMS唤醒网络的电压阈值
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)PrmEgyAvlDchaChrgnStartParked_bb04')
    def test_caseid_1984762(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xBB04, SESSION.EXTENDED, UnLock.L3, '50', '62bb0450')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb04','62bb04')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2ebb0450','6ebb04')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb04','62bb0450')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xbb04, SESSION.EXTENDED, UnLock.L3,
                                           data,
                                           f'62bb04{data}',
                                           check_method=Check_Method.read,recover=False)

    # BMS充电电流唤醒设置
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb05')
    def test_caseid_1984757(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb05, SESSION.DEFAULT, '62bb05', check_range=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb05, SESSION.EXTENDED, '62bb05', check_range=[0x00, 0x01])

    # BMS充电电流唤醒设置
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)PrmEgyAvlDchaChrgnStartParked_bb05')
    def test_caseid_1984756(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xBB05, SESSION.EXTENDED, UnLock.L3, '01', '62bb0501')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb05','62bb05')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2ebb0501','6ebb05')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb05','62bb0501')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xbb05, SESSION.EXTENDED, UnLock.L3,
                                           data,
                                           f'62bb05{data}',
                                           check_method=Check_Method.read,recover=False)

    # BMS充电电流唤醒阈值
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb06')
    def test_caseid_1984753(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb06, SESSION.DEFAULT, '62bb06')
        assert 0 <= int(p1[6:], 16) <= 65536, 'value out of range'
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb06, SESSION.EXTENDED, '62bb06')

    # BMS充电电流唤醒阈值
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)PrmEgyAvlDchaChrgnStartParked_bb06')
    def test_caseid_1984752(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xBB06, SESSION.EXTENDED, UnLock.L3, '2a2a', '62bb062a2a')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb06','62bb06')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2ebb062a2a','6ebb06')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb06','62bb062a2a')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xbb06, SESSION.EXTENDED, UnLock.L3,
                                           data,
                                           f'62bb06{data}',
                                           check_method=Check_Method.read,recover=False)

    # BMS放电电量唤醒设置
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb07')
    def test_caseid_1984755(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb07, SESSION.DEFAULT, '62bb07', check_range=[0x00, 0x01])
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb07, SESSION.EXTENDED, '62bb07', check_range=[0x00, 0x01])

    # BMS放电电量唤醒设置
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)PrmEgyAvlDchaChrgnStartParked_bb07')
    def test_caseid_1984754(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xBB07, SESSION.EXTENDED, UnLock.L3, '01', '62bb0701')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb07','62bb07')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2ebb0701','6ebb07')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb07','62bb0701')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xbb07, SESSION.EXTENDED, UnLock.L3,
                                           data,
                                           f'62bb07{data}',
                                           check_method=Check_Method.read,recover=False)

    # BMS放电电量唤醒阈值
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb08')
    def test_caseid_1984751(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb08, SESSION.DEFAULT, '62bb08')
        assert 0 <= int(p1[6:], 16) <= 65536, 'value out of range'
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb08, SESSION.EXTENDED, '62bb08')

    # BMS放电电量唤醒阈值
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)PrmEgyAvlDchaChrgnStartParked_bb08')
    def test_caseid_1984750(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xBB08, SESSION.EXTENDED, UnLock.L3, '5050', '62bb085050')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb08','62bb08')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2ebb085050','6ebb08')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb08','62bb085050')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xbb08, SESSION.EXTENDED, UnLock.L3,
                                           data,
                                           f'62bb08{data}',
                                           check_method=Check_Method.read,recover=False)

    # BGM网络休眠期间主动唤醒的时间间隔
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb09')
    def test_caseid_1984749(self):
        p1 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb09, SESSION.DEFAULT, '62bb09')
        assert 0 <= int(p1[6:], 16) <= 65535, 'value out of range'
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb09, SESSION.EXTENDED, '62bb09')

    # BGM网络休眠期间主动唤醒的时间间隔
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)PrmEgyAvlDchaChrgnStartParked_bb09')
    def test_caseid_1984748(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xBB09, SESSION.EXTENDED, UnLock.L3, 'ffff', '62bb09ffff')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb09','62bb09')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2ebb09ffff','6ebb09')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb09','62bb09ffff')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xbb09, SESSION.EXTENDED, UnLock.L3,
                                           data,
                                           f'62bb09{data}',
                                           check_method=Check_Method.read,recover=False)

    ##1认证密钥_800V  V2.0实现
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Secret Key For Immobilizer Target #1 ECM 800V_41DE')
    def test_caseid_1985550(self):
        self.sd_tester.write_ccp({962: 0x02})
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41de, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41de, SESSION.EXTENDED,
                                          '6241de55555555555555555555555555555555', check_length=38)

    ##1认证密钥_800V V2.0
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Secret Key For Immobilizer Target #1 ECM 800V_41DE')
    def test_caseid_1985549(self):
        # self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x41de, SESSION.EXTENDED, UnLock.L11,
        #                                    '55555555555555555555555555555555', '6241de55555555555555555555555555555555',check_method=Check_Method.read,recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x41de, SESSION.EXTENDED, UnLock.L11,
                                           '55555555555555555555555555555550', '6241de55555555555555555555555555555550',
                                           check_method=Check_Method.reset)
        self.mix.write_did_and_check(TA.BGM_MCU, 0x41de, SESSION.EXTENDED, UnLock.L11,
                                           '55555555555555555555555555555550', '6241de55555555555555555555555555555550',check_method=Check_Method.kl30)

    ##2认证密钥_800V  V2.0实现
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Secret Key For Immobilizer Target #2 IEM 800V_41DF')
    def test_caseid_1985548(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41df, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41df, SESSION.EXTENDED,
                                          '6241df55555555555555555555555555555555', check_length=38)

    ##2认证密钥_800V V2.0
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Secret Key For Immobilizer Target #2 IEM 800V_41DF')
    def test_caseid_1985547(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x41df, SESSION.EXTENDED, UnLock.L11,
                                           '55555555555555555555555555555550', '6241df55555555555555555555555555555550',
                                           check_method=Check_Method.reset)
        self.mix.write_did_and_check(TA.BGM_MCU, 0x41df, SESSION.EXTENDED, UnLock.L11,
                                           '55555555555555555555555555555550', '6241df55555555555555555555555555555550',check_method=Check_Method.kl30)

    ##3认证密钥_800V  V2.0实现
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Secret Key For Immobilizer Target #3 MGM 800V_41E0')
    def test_caseid_1985546(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41e0, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41e0, SESSION.EXTENDED,
                                          '6241e055555555555555555555555555555555', check_length=38)

    ##3认证密钥_800V V2.0
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Secret Key For Immobilizer Target #3 MGM 800V_41E0')
    def test_caseid_1985545(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x41e0, SESSION.EXTENDED, UnLock.L11,
                                           '55555555555555555555555555555550', '6241e055555555555555555555555555555550',
                                           check_method=Check_Method.reset)
        self.mix.write_did_and_check(TA.BGM_MCU, 0x41e0, SESSION.EXTENDED, UnLock.L11,
                                           '55555555555555555555555555555550', '6241e055555555555555555555555555555550',check_method=Check_Method.kl30)

    ##SK IV 800V  V2.0
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Secret Key IV used in challenge/respond_41E1')
    def test_caseid_1985544(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41e1, SESSION.DEFAULT, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41e1, SESSION.EXTENDED,
                                          '6241e1696d6d6f6b6579303030303030303030', check_length=38)

    ##SK IV 800V V2.0
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Secret Key IV used in challenge/respond_41E1')
    def test_caseid_1985543(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x41e1, SESSION.EXTENDED, UnLock.L11,
                                           '696d6d6f6b6579303030303030303031', '6241e1696d6d6f6b6579303030303030303031',
                                           check_method=Check_Method.reset)
        self.mix.write_did_and_check(TA.BGM_MCU, 0x41e1, SESSION.EXTENDED, UnLock.L11,
                                           '696d6d6f6b6579303030303030303031', '6241e1696d6d6f6b6579303030303030303031',check_method=Check_Method.kl30)

    # 司机门状态诊断计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_WriteDataByIdentifier(0x2E)Driver Door Status Diagnostics Counter_40E8')
    def test_caseid_1988696(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x40e8, SESSION.DEFAULT, UnLock.L0, 'ff', '7f2e31',
                                           check_method=Check_Method.response, recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x40e8, SESSION.EXTENDED, UnLock.L0, 'ff', '7f2e33',
                                           check_method=Check_Method.response, recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x40e8, SESSION.EXTENDED, UnLock.L5, 'ff', '6240e8ff',
                                           check_method=Check_Method.reset)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'2240e8','6240e8')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2e40e8ff','6e40e8')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2240e8','6240e8ff')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0x40e8, SESSION.EXTENDED, UnLock.L5,
                                           data,
                                           f'6240e8{data}',
                                           check_method=Check_Method.read,recover=False)

    #BGM检测左前门端电压触发闭合冗余回路的电压阈值
    #BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)ULoFLDoorSysThd_BB0A')
    def test_caseid_1990646(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xbb0a,SESSION.DEFAULT,'62bb0a5a')
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xbb0a,SESSION.EXTENDED,'62bb0a5a')

    #BGM检测左前门端电压触发闭合冗余回路的电压阈值
    #BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)ULoFLDoorSysThd_BB0A')
    def test_caseid_1990649(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xbb0a,SESSION.DEFAULT,UnLock.L0,'7e','7f2e31',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xbb0a,SESSION.EXTENDED,UnLock.L0,'7e','7f2e33',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xbb0a,SESSION.EXTENDED,UnLock.L3,'7e','62bb0a7e')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb0a','62bb0a')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2ebb0a7e','6ebb0a')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb0a','62bb0a7e')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xbb0a, SESSION.EXTENDED, UnLock.L3,
                                           data,
                                           f'62bb0a{data}',
                                           check_method=Check_Method.read,recover=False)
        
    #BGM检测IPM端电压触发闭合冗余回路的电压阈值
    #BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)ULoIPMSysThd_BB0B')
    def test_caseid_1990647(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xbb0b,SESSION.DEFAULT,'62bb0b5a')
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xbb0b,SESSION.EXTENDED,'62bb0b5a')

    #BGM检测IPM端电压触发闭合冗余回路的电压阈值
    #BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)ULoIPMSysThd_BB0B')
    def test_caseid_1990650(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xbb0b,SESSION.DEFAULT,UnLock.L0,'7e','7f2e31',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xbb0b,SESSION.EXTENDED,UnLock.L0,'7e','7f2e33',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xbb0b,SESSION.EXTENDED,UnLock.L3,'7e','62bb0b7e')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb0b','62bb0b')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2ebb0b7e','6ebb0b')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb0b','62bb0b7e')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xbb0b, SESSION.EXTENDED, UnLock.L3,
                                           data,
                                           f'62bb0b{data}',
                                           check_method=Check_Method.read,recover=False)

    #BGM检测IPM端电压断开冗余回路的电压阈值
    #BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)ULoIPMSysRecoveryThd_BB0C')
    def test_caseid_1990648(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xbb0c,SESSION.DEFAULT,'62bb0c73')
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xbb0c,SESSION.EXTENDED,'62bb0c73')

    #BGM检测IPM端电压断开冗余回路的电压阈值
    #BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)ULoIPMSysRecoveryThd_BB0C')
    def test_caseid_1990651(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xbb0c,SESSION.DEFAULT,UnLock.L0,'7e','7f2e31',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xbb0c,SESSION.EXTENDED,UnLock.L0,'7e','7f2e33',check_method=Check_Method.response,recover=False)
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xbb0c,SESSION.EXTENDED,UnLock.L3,'7e','62bb0c7e')
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        data = self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb0c','62bb0c')[6:]
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'2ebb0c7e','6ebb0c')
        time.sleep(20)
        self.io.io_reset_bgm(times=3)
        time.sleep(20)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L3)
        self.sd_tester.send_data_and_check(TA.BGM_MCU,'22bb0c','62bb0c7e')
        self.sd_tester.write_did_and_check(TA.BGM_MCU, 0xbb0c, SESSION.EXTENDED, UnLock.L3,
                                           data,
                                           f'62bb0c{data}',
                                           check_method=Check_Method.read,recover=False)

    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Inhibit Drive Car Status_F155')
    def test_caseid_1994869(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xF155, SESSION.DEFAULT, '62f15500')
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xF155, SESSION.EXTENDED, '62f15500')
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xF155, SESSION.PROGRAMMING, '7f2231')

    # BGM_SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)BGM certificate status_B160')
    def test_caseid_1994870(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb160, SESSION.DEFAULT, '62b16002')
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb160, SESSION.EXTENDED, '62b16002')
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb160, SESSION.PROGRAMMING, '7f2231')

@allure.feature('BGM BaseTech/诊断功能/诊断DID')
class TestDIDBoot(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        logger.info("before_class")
        with allure.step("初始化环境"):
            self.mix.init_boot_per()
        self.f1aa = self.sd_tester.get_ecu_core_assembly_part_number()
        self.f1ab = self.sd_tester.get_ecu_delivery_assembly_part_number()
        self.f18c = self.sd_tester.get_ecu_serial_number()
        self.vin = self.sd_tester.get_vehicle_identification_number()
        self.f1f0 = self.sd_tester.get_mcu_software_part_number()

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.sd_tester.update_serverdoipid(0x1002)
        self.sd_tester.enter_boot()
        self.sd_tester.update_serverdoipid(0x1001)
        self.sd_tester.send_request_and_recv_response([0x10, 0x02], recv=[0x50, 0x02])
        self.sd_tester.send_request_and_recv_response([0x22, 0xf1, 0x86], recv=[0x62, 0xf1, 0x86, 0x02])

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        logger.info("after_class")
        super().after_class(self, ecu)
        self.sd_tester.exit_muc_boot()

    # APP ECU完整零件序列号（APP+SBL+PBL）
    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_CompleteSetOfECUPart|SerialNumbersInAPP_ED20')
    def test_caseid_1981701_00(self):
        self.sd_tester.read_did_and_check([TA.BGM_SOC, TA.BGM_MCU], 0xED20, SESSION.PROGRAMMING,
                                          [f'62ed20f1aa{self.f1aa}f1ab{self.f1ab}f18c{self.f18c}',
                                           f'62ed20f1aa{self.f1aa}f1ab{self.f1ab}f18c{self.f18c}'])

    # 当前诊断会话（APP+SBL+PBL）
    # BGM_SOC,BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_ActiveDiagSessionDataRecord_F186')
    def test_caseid_1981700_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xF186, SESSION.PROGRAMMING, '62f18602')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xF186, SESSION.PROGRAMMING, '62f18602')

    # ECU序列号（APP+SBL+PBL）
    # BGM_SOC,BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_ECU Serial Number_F18C')
    def test_caseid_1981699_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xF18C, SESSION.PROGRAMMING, '62f18c', check_length=14)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xF18C, SESSION.PROGRAMMING, '62f18c', check_length=14)

    # VIN码（APP）
    # BGM_SOC,BGM_MCU

    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_Vehicle Identification Number_F190')
    def test_caseid_1981697_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xF190, SESSION.PROGRAMMING, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xF190, SESSION.PROGRAMMING, '7f2231')

    # APP诊断数据库零件号（APP）
    # BGM_SOC,BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_Application Diagnostic Database Part Number_F1A0')
    def test_caseid_1981695_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf1a0, SESSION.PROGRAMMING, '7f2231')
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1a0, SESSION.PROGRAMMING, '7f2231')

    # #ECU硬件号（APP+SBL+PBL）
    # #BGM_SOC,BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_ECU Core Assembly Part Number_F1AA')
    def test_caseid_1981694_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf1aa, SESSION.PROGRAMMING, '62f1aa', check_length=22)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1aa, SESSION.PROGRAMMING, '62f1aa', check_length=22)

    # #ECU总成号（APP+SBL+PBL）
    # #BGM_SOC,BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)_ECU Delivery Assembly Part Number_F1AB')
    def test_caseid_1981693_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf1ab, SESSION.PROGRAMMING, '62f1ab', check_length=22)
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1ab, SESSION.PROGRAMMING, '62f1ab', check_length=22)

    # #ECU软件号ECU软件号数量2+ECU软件号8+MCU bootloader号8（APP）
    # #BGM_SOC
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)ECU Software Part Numbers_F1AE')
    def test_caseid_1981692_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf1ae, SESSION.PROGRAMMING, '7f2231')

    # 子节点总数（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Total number of Private ECU(s) / component(s) Serial Numbers_F13F')
    def test_caseid_1981690_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf13f, SESSION.PROGRAMMING, '7f2231')

    # PBL软件号（APP+SBL+PBL）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Primary Bootloader Software Part Number_F1A5')
    def test_caseid_1981689_00(self):
        self.f1a5 = self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xF1A5, SESSION.PROGRAMMING, '62f1a5')[6:]
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1a5, SESSION.PROGRAMMING, f'62f1a5{self.f1a5}',
                                          check_length=22)

    # MCU软件号（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)MCU Software part number_F1F0')
    def test_caseid_1981688_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1f0, SESSION.PROGRAMMING, '7f2231')

    # L1安全常数（PBL）
    # BGM _SOC
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Security Constant_Level 01_F102')
    def test_caseid_1981685_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf102, SESSION.PROGRAMMING, '7f2231')

    # L1安全常数（PBL）仅能写入一次
    # BGM _SOC
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)Security Constant_Level 01_F102')
    def test_caseid_1981684(self):
        #self.mix.delete_vehicleInfo_json()
        # with allure.step("删除密钥后重启并等待10s"):
        #     commands = "rm -rf /data/certificate/vbf_pk.pem /data/vehicleInfo.json; sync"
        #     self.ssh.bgm_ssh.type_commands(commands)
        #     self.sd_tester.reset_0x1181()
        #     time.sleep(10)
        #self.sd_tester.write_did_and_check(TA.BGM_SOC, 0xf102, SESSION.PROGRAMMING, UnLock.L1, write_data='FFFFFFFFFF',
         #                                  check_data='6ef102', check_method=Check_Method.response, recover=False)
         pass

    # 车辆配置错误参数（APP）#SOC删掉
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Car Configuration Parameter Faults_E103')
    def test_caseid_1981682_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xe103, SESSION.PROGRAMMING, '7f2231', )

    # 整车基线版本号（APP）
    # BGM _SOC
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle baseline number_F150')
    def test_caseid_1981680_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf150, SESSION.PROGRAMMING, '7f2231')

    # VID（APP）
    # BGM _SOC
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle Identification_B163')
    def test_caseid_1981678_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb163, SESSION.PROGRAMMING, '7f2231')

    # FOTA升级状态（APP）
    # BGM _SOC
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)FOTA result_F154')
    def test_caseid_1981674_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf154, SESSION.PROGRAMMING, '7f2231')

    # fw major version；minor version；build version；fw and config version（APP）
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Switch Firmware and CFG version_FD50')
    def test_caseid_1981672_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xfd50, SESSION.PROGRAMMING, '7f2231')

    # 整车展示的版本号（APP）
    # BGM _SOC
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle Diaplay Baseline Number_F151')
    def test_caseid_1981671_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xf151, SESSION.PROGRAMMING, '7f2231')

    # OBD防火墙状态（APP）
    # BGM _SOC
    @pytest.mark.sanity
    @allure.story('诊断DID')  # 02会话下不可读，现在可读,需求写错了，需求也想可读
    @allure.title('UDS_ReadDataByIdentifier(0x22)OBD Firewall status_B165')
    def test_caseid_1981669_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb165, SESSION.PROGRAMMING, '62b165')

    # 工厂模式下自动解锁时间设置（APP）
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Fartory mode AutoUnlock TimeSetting_B200')
    def test_caseid_1981668_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xB200, SESSION.PROGRAMMING, '7f2231')

    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Get TurnLamp Status_B250')
    def test_caseid_1981666_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xB250, SESSION.PROGRAMMING, '7f2231')

    # 整车埋点配置信息（APP） v131only
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)vehicle data tracking config_EA40')
    def test_caseid_1981665_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xea40, SESSION.PROGRAMMING, '7f2231')

    # SOA服务埋点配置信息（APP） v131only
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)SOA service data tracking config_EA41')
    def test_caseid_1981664_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xea41, SESSION.PROGRAMMING, '7f2231')

    # 展车模式（APP）
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Exhibition Mode Status_B300')
    def test_caseid_1981663_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb300, SESSION.PROGRAMMING, '7f2231')

    # 洗车模式（APP）
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Wash Mode Status_B301')
    def test_caseid_1981662_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb301, SESSION.PROGRAMMING, '7f2231')

    # 维修模式（APP）
    # BGM _SOC
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Maintain Mode Status_B302')
    def test_caseid_1981661_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_SOC, 0xb302, SESSION.PROGRAMMING, '7f2231')

    # 1认证密钥（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Secret Key For Immobilizer Target #1 ECM_40DE')
    def test_caseid_1981657_00(self):
        self.sd_tester.write_ccp({962: 0x00})
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40de, SESSION.PROGRAMMING, '7f2231')

    ##2认证密钥（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Secret Key Immobilizer Target #2 IEM_40DF')
    def test_caseid_1981655_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40df, SESSION.PROGRAMMING, '7f2231')

    ##3认证密钥（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Secret Key Immobilizer Target #3 MGM_40E0')
    def test_caseid_1981653_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40e0, SESSION.PROGRAMMING, '7f2231')

    # 全局时间（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Globe real time_DD00')
    def test_caseid_1981651_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd00, SESSION.PROGRAMMING, '7f2231')

    # 总里程（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Total distance_DD01')
    def test_caseid_1981650_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd01, SESSION.PROGRAMMING, '7f2231')

    # 车辆电池电压（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle Battery Voltage_DD02')
    def test_caseid_1981648_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd02, SESSION.PROGRAMMING, '7f2231')

    # 车辆使用模式（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Usage Mode_DD0A')
    def test_caseid_1981647_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd0a, SESSION.PROGRAMMING, '7f2231')

    # 供电等级（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)EIPowerLevel_DD0C')
    def test_caseid_1981646_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd0c, SESSION.PROGRAMMING, '7f2231')

    # CCP参数（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Car Configuration Parameter_F106')
    def test_caseid_1981645_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf106, SESSION.PROGRAMMING, '7f2231')

    # 电池静态电流-低范围（APP）
    # BGM_MCU
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Quiesent Current - Low Range_4025')
    def test_caseid_1981643_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4025, SESSION.PROGRAMMING, '7f2231')

    # 发动机关闭时电池的归一化累积放电（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Normalised Cumulated Discharge From Battery When Engine Off_4026')
    def test_caseid_1981642_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4026, SESSION.PROGRAMMING, '7f2231')

    # 车辆电池-使用时间（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle Battery - Time In Service_4027')
    def test_caseid_1981641_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4027, SESSION.PROGRAMMING, '7f2231')

    # 车辆电池充电状态-预估（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle Battery State Of Charge - Estimated_4028')
    def test_caseid_1981640_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4028, SESSION.PROGRAMMING, '7f2231')

    # 汽车电池温度-预估（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle Battery Temperature - Estimated_4029')
    def test_caseid_1981639_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4029, SESSION.PROGRAMMING, '7f2231')

    # 车载电池电压（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Vehicle Battery Voltage_402A')
    def test_caseid_1981638_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x402a, SESSION.PROGRAMMING, '7f2231')

    # 远程车辆IMMO密钥（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Remote Vehicle Immobilization Secret Key_408F')
    def test_caseid_1981637_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x408f, SESSION.PROGRAMMING, '7f2231')

    # 电池电流（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Current_4090')
    def test_caseid_1981634_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4090, SESSION.PROGRAMMING, '7f2231')

    # 电池状态充电统计计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery State of Charge Statistics Counter_4094')
    def test_caseid_1981633_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4094, SESSION.PROGRAMMING, '7f2231')

    # 电荷平衡统计计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Charge Balance Statistics Counter_40A2')
    def test_caseid_1981632_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40a2, SESSION.PROGRAMMING, '7f2231')

    # 自上次重置后的秒数（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Seconds since last reset_40AF')
    def test_caseid_1981631_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40af, SESSION.PROGRAMMING, '7f2231')

    # 电池容量（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Capacity Relative_40B0')
    def test_caseid_1981630_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40b0, SESSION.PROGRAMMING, '7f2231')

    # 低电量报警统计寄存器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Low Battery Warning Statistics Register_40CA')
    def test_caseid_1981629_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40ca, SESSION.PROGRAMMING, '7f2231')

    # 电池传感器一致性检查（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Sensor Consistency Check_40CB')
    def test_caseid_1981628_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40cb, SESSION.PROGRAMMING, '7f2231')

    # 充电模式（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Charge Mode_40D1')
    def test_caseid_1981627_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40d1, SESSION.PROGRAMMING, '7f2231')

    # 电池静态电流-统计（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Quiescent Current - Statistics_40D7')
    def test_caseid_1981626_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40d7, SESSION.PROGRAMMING, '7f2231')

    # 可用Delta电源信号输出（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Available Delta Power signal output_40E2')
    def test_caseid_1981625_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40e2, SESSION.PROGRAMMING, '7f2231')

    # 配电继电器状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Distribution Relays Status_40E3')
    def test_caseid_1981624_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40e3, SESSION.PROGRAMMING, '7f2231')

    # 电力系统故障计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Power System Fault Counters_40E4')
    def test_caseid_1981623_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4044, SESSION.PROGRAMMING, '7f2231')

    # 司机门状态诊断计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Driver Door Status Diagnostics Counter_40E8')
    def test_caseid_1981622_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40e8, SESSION.PROGRAMMING, '7f2231')

    # Immo状态历史（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Immo Status History_40EE')
    def test_caseid_1981621_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40ee, SESSION.PROGRAMMING, '7f2231')

    # 闭锁命令记录（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Locking Command History_40EF')
    def test_caseid_1981620_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40ef, SESSION.PROGRAMMING, '7f2231')

    # 解锁命令记录（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Unlocking Command History_40F0')
    def test_caseid_1981619_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40f0, SESSION.PROGRAMMING, '7f2231')

    # 防玩计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Play protection counter_40F2')
    def test_caseid_1981618_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x40f2, SESSION.PROGRAMMING, '7f2231')

    # 方向盘调整（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Steering Wheel Tuning_4109')
    def test_caseid_1981616_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4109, SESSION.PROGRAMMING, '7f2231')

    # 日/夜和暮光传感器状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Day/Night And Twilight Sensors Status_410B')
    def test_caseid_1981614_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x410b, SESSION.PROGRAMMING, '7f2231')

    # 车辆电源插口控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Power Outlet Control_4110')
    def test_caseid_1981613_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4110, SESSION.PROGRAMMING, '7f2231')

    # 请求充电电压（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Requested Charge Voltage_411D')
    def test_caseid_1981612_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x411d, SESSION.PROGRAMMING, '7f2231')

    # 防盗报警触发源（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Alarm Trigger Information_416B')
    def test_caseid_1981611_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x416b, SESSION.PROGRAMMING, '7f2231')

    # 室内灯光白天至黑夜计时器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Interior Light Day to Night Timer_416D')
    def test_caseid_1981610_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x416d, SESSION.PROGRAMMING, '7f2231')

    # 室内灯光黑夜至白天计时器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Interior Light Night to Day Timer_416E')
    def test_caseid_1981608_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x416e, SESSION.PROGRAMMING, '7f2231')

    # 在运输模式时的主电池计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Main Battery Counter In Transport Mode_4187')
    def test_caseid_1981606_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4187, SESSION.PROGRAMMING, '7f2231')

    # 雨刷停止位状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Wiper Park Position Status_418F')
    def test_caseid_1981605_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x418f, SESSION.PROGRAMMING, '7f2231')

    # 运输模式下电池的充电状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Transport Mode Battery State Of Charge_41CE')
    def test_caseid_1981604_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41ce, SESSION.PROGRAMMING, '7f2231')

    # 内灯控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Interior Lights Control_41E5')
    def test_caseid_1981603_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41e5, SESSION.PROGRAMMING, '7f2231')

    # 节电继电器控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Power Saver Relay Control_41E9')
    def test_caseid_1981602_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41e9, SESSION.PROGRAMMING, '7f2231')

    # 车辆关闭返回到汽车模式计时器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Timer Vehicle Off Return To Car Mode_41F8')
    def test_caseid_1981601_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41f8, SESSION.PROGRAMMING, '7f2231')

    # 激活主驾侧后视镜除霜（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Activate Driver Side Mirror Defroster_4219')
    def test_caseid_1981599_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4219, SESSION.PROGRAMMING, '7f2231')

    # 激活副驾侧后视镜除霜（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Activate Passenger Side Mirror Defroster_421A')
    def test_caseid_1981598_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x421a, SESSION.PROGRAMMING, '7f2231')

    # 激活电动前挡风玻璃（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Activate Electrical Front Windscreen_421D')
    def test_caseid_1981597_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x421d, SESSION.PROGRAMMING, '7f2231')

    # 激活电动后挡风玻璃（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Activate Electrical Rear Window_421E')
    def test_caseid_1981596_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x421e, SESSION.PROGRAMMING, '7f2231')

    # 控制台后按钮状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Overhead Console Rear Button Status_422F')
    def test_caseid_1981595_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x422f, SESSION.PROGRAMMING, '7f2231')

    # 控制台按钮状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Overhead Console Button Status_4230')
    def test_caseid_1981594_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4230, SESSION.PROGRAMMING, '7f2231')

    # 车辆模式为工厂暂停模式计时器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Timer Car Mode Factory Pause_4231')
    def test_caseid_1981593_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4231, SESSION.PROGRAMMING, '7f2231')

    # 延时进入车辆模式计时器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Delay to Enter Car Mode_4232')
    def test_caseid_1981591_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4232, SESSION.PROGRAMMING, '7f2231')

    # 雨水传感器高温检测（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Rain Sensor High Temperature Detected_4282')
    def test_caseid_1981589_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4282, SESSION.PROGRAMMING, '7f2231')

    # 雨水传感器高压检测（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Rain Sensor High Voltage Detected_4283')
    def test_caseid_1981588_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4283, SESSION.PROGRAMMING, '7f2231')

    # 解锁后的NFC持续时间（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)NFC duration after unlock_4297')
    def test_caseid_1981587_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4297, SESSION.PROGRAMMING, '7f2231')

    # 电池平均静态电流-统计（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Average Quiescent Current - Statistics_42CD')
    def test_caseid_1981585_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42cd, SESSION.PROGRAMMING, '7f2231')

    # 电池容量统计计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Capacity Statistics Counter_42CF')
    def test_caseid_1981584_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42cf, SESSION.PROGRAMMING, '7f2231')

    # 电池内阻统计计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Internal Resistance Statistics Counter_42D1')
    def test_caseid_1981583_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42d1, SESSION.PROGRAMMING, '7f2231')

    # 电池归一化内阻统计计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Normalized Internal Resistance Statistics Counter_42D2')
    def test_caseid_1981582_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42d2, SESSION.PROGRAMMING, '7f2231')

    # 电池内阻（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Internal Resistance_42D3')
    def test_caseid_1981581_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42d3, SESSION.PROGRAMMING, '7f2231')

    # 电池静态电流短时间滤波_低范围（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Quiescent Current Short Time Filtering_Low Range_42E3')
    def test_caseid_1981580_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42e3, SESSION.PROGRAMMING, '7f2231')

    # 电池平均静态电流_高范围（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Average Quiescent Current_High Range_42E4')
    def test_caseid_1981579_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42e4, SESSION.PROGRAMMING, '7f2231')

    # 防盗报警状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Alarm Status_42E5')
    def test_caseid_1981578_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42e5, SESSION.PROGRAMMING, '7f2231')

    # 中控锁防玩保护（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Central Locking Play Protection_42E9')
    def test_caseid_1981577_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42e9, SESSION.PROGRAMMING, '7f2231')

    # Ajar开关状态（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Ajar Switch Status_42F2')
    def test_caseid_1981575_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42f2, SESSION.PROGRAMMING, '7f2231')

    # 手套箱解锁状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Private Unlock Status_42F4')
    def test_caseid_1981574_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42f4, SESSION.PROGRAMMING, '7f2231')

    # ITO信号频率状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)ITO Signal Frequency Status_42FB')
    def test_caseid_1981573_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x42fb, SESSION.PROGRAMMING, '7f2231')

    # 危险警报灯开关状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Hazard Switch Status_4300')
    def test_caseid_1981572_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4300, SESSION.PROGRAMMING, '7f2231')

    # IGN供电继电器反馈（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Ignition Power Relay Feedback_4305')
    def test_caseid_1981571_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4305, SESSION.PROGRAMMING, '7f2231')

    # 雨刮电机通信错误检测（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Wiper Motor Communication Error Detection_430B')
    def test_caseid_1981570_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x430b, SESSION.PROGRAMMING, '7f2231')

    # 雨刮电机节点错误检测（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Wiper Motor Node Error Detection_430C')
    def test_caseid_1981569_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x430c, SESSION.PROGRAMMING, '7f2231')

    # 使用模式扩展信息统计（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Usage Mode Extention Statistics_430E')
    def test_caseid_1981568_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x430e, SESSION.PROGRAMMING, '7f2231')

    # 使用模式时间统计（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Usage Mode Time Statistics_430F')
    def test_caseid_1981567_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x430f, SESSION.PROGRAMMING, '7f2231')

    # 燃油泵/碰撞控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Fuel Pump / crash relay Control_4310')
    def test_caseid_1981566_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4310, SESSION.PROGRAMMING, '7f2231')

    # 车轮测功器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Dynamometer Wheels_4313')
    def test_caseid_1981565_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4313, SESSION.PROGRAMMING, '7f2231')

    # 雨刮单次挂水（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Single Stroke Wiping_4328')
    def test_caseid_1981563_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4328, SESSION.PROGRAMMING, '7f2231')

    # 室内灯光脚灯状态反馈（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Interior Light Footwell Status Feedback_432D')
    def test_caseid_1981562_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x432D, SESSION.PROGRAMMING, '7f2231')

    # 空调继电器控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Climate Relay Control_432E')
    def test_caseid_1981561_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x432e, SESSION.PROGRAMMING, '7f2231')

    # 运输模式下低压电池SoC（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Low Battery SoC in Transport Mode_433E')
    def test_caseid_1981560_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x433e, SESSION.PROGRAMMING, '7f2231')

    # 外灯继电器控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Exterior Light Relay Control_439F')
    def test_caseid_1981559_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x439f, SESSION.PROGRAMMING, '7f2231')

    # 雨量传感器重新采用（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Rain Sensor ReAdaption_43B8')
    def test_caseid_1981558_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x43b8, SESSION.PROGRAMMING, '7f2231')

    # 车辆模式包括子状态（APP）
    # BGM_MCU 03/l3才可读
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Car Mode including subtypes_43C4')
    def test_caseid_1981557_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x43c4, SESSION.PROGRAMMING, '7f2231')

    # SWDL的门状态和锁状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Door and Lock status for SWDL_43D6')
    def test_caseid_1981556_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x43d6, SESSION.PROGRAMMING, '7f2231')

    # 工厂模式下低压电池SOC（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Low Battery SoC In Factory Mode_4516')
    def test_caseid_1981553_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4516, SESSION.PROGRAMMING, '7f2231')

    # IMMO管理状态
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Immobilize Mangement status_45A1')
    def test_caseid_1981552_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x45a1, SESSION.PROGRAMMING, '7f2231')

    # 雨量传感器阈值（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Rain Sensor Threshold value_45A4')
    def test_caseid_1981551_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x45a4, SESSION.PROGRAMMING, '7f2231')

    # 车窗短降（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Windows Short Drop_45BF')
    def test_caseid_1981549_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x45bf, SESSION.PROGRAMMING, '7f2231')

    # 外灯状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Exterior Lighting Status_7000')
    def test_caseid_1981548_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x7000, SESSION.PROGRAMMING, '7f2231')

    # 外灯控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Exterior Lights Control_7022')
    def test_caseid_1981547_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x7022, SESSION.PROGRAMMING, '7f2231')

    # L11/L12安全常数（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Security Constant Level 11/12_D12F')
    def test_caseid_1981546_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd12f, SESSION.PROGRAMMING, '7f2231')

    # 车辆模式（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Car Mode_D134')
    def test_caseid_1981543_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd134, SESSION.PROGRAMMING, '7f2231')

        # BNCM和BGM的安全密钥（APP）
        # BGM_MCU

    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Security Key between BNCM and BGM (Digital Key)_D904')
    def test_caseid_1981541_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd904, SESSION.PROGRAMMING, '7f2231')

    # BNCM和BGM的安全密钥的Mac状态（APP）
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Security Key between BNCM and BGM (Digital Key) Mac_D906')
    def test_caseid_1981539_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd906, SESSION.PROGRAMMING, '7f2231')

    # 电池可用Delta能量（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Available Delta Energy_D934')
    def test_caseid_1981538_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd934, SESSION.PROGRAMMING, '7f2231')

    # 电池能量可用警告（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Battery Energy Available To Warning_D935')
    def test_caseid_1981537_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd935, SESSION.PROGRAMMING, '7f2231')

    # VFC Vector框架设置（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)VFCVectorFrame Setting_E503')
    def test_caseid_1981536_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xe503, SESSION.PROGRAMMING, '7f2231')

    # 后备箱供电状态反馈（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Luggage Supply Status Feedback_EE94')
    def test_caseid_1981534_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xee94, SESSION.PROGRAMMING, '7f2231')

    # 喇叭统计信息（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Statistic Information for Horn_EE99')
    def test_caseid_1981533_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xee99, SESSION.PROGRAMMING, '7f2231')

    # 后挡风玻璃加热器控制#1（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Rear Windscreen Heater Control #1_EF99')
    def test_caseid_1981532_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xef99, SESSION.PROGRAMMING, '7f2231')

    # BGM唤醒原因（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)BGM Wake Up Cause_F010')
    def test_caseid_1981531_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf010, SESSION.PROGRAMMING, '7f2231')

    # BGM保持唤醒的原因（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)BGM Keep Active Cause_F011')
    def test_caseid_1981530_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf011, SESSION.PROGRAMMING, '7f2231')

    # 专用ECU交付总成部件编号（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Private ECU(s) Delivery Assembly Part Number(s)_F1BB')
    def test_caseid_1981529_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf1bb, SESSION.PROGRAMMING, '7f2231')

    # 转向灯诊断状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Direction Indication Diagnostics Status_FD07')
    def test_caseid_1981527_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xfd07, SESSION.PROGRAMMING, '7f2231')

    # 以太网链接状态（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Ethernet Link Status_D250')
    def test_caseid_1981526_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd250, SESSION.PROGRAMMING, '7f2231')

    # 单一质量指数（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Single Quality Index_D260')
    def test_caseid_1981525_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd260, SESSION.PROGRAMMING, '7f2231')

    # 控制WMM激活前洗涤（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Activate frontwasher_420A')
    def test_caseid_1981524_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x420a, SESSION.PROGRAMMING, '7f2231')

    # 从CDC来的雨刮挡位信息（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Wiper’s lever information from CDC_4218')
    def test_caseid_1981523_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4218, SESSION.PROGRAMMING, '7f2231')

    # 智能补电使能（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Voltage Wake Up Charging At Sleep Enable_4530')
    def test_caseid_1981522_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4530, SESSION.PROGRAMMING, '7f2231')

    # 智能补电电压（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Voltage Wake Up Charging At Sleep_4531')
    def test_caseid_1981520_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4531, SESSION.PROGRAMMING, '7f2231')

    # 智能补电定时器使能（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Timer Wake Up Charging At Sleep Enable_4532')
    def test_caseid_1981518_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4532, SESSION.PROGRAMMING, '7f2231')

    # 停车时的原始能量可用充电中止（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Prim Energy Available Charge Required for Parked_4533')
    def test_caseid_1981516_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4533, SESSION.PROGRAMMING, '7f2231')

    # inactive下充电电压值（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Voltage Value Charging At Inactive_4534')
    def test_caseid_1981514_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4534, SESSION.PROGRAMMING, '7f2231')

    # 停车时的原始能量可用充电（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Prim Energy Available Charge Required for Parked_4535')
    def test_caseid_1981512_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4535, SESSION.PROGRAMMING, '7f2231')

    # 低压能量等级替代（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Energy Level Electric Substitution_429D')
    def test_caseid_1981510_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429d, SESSION.PROGRAMMING, '7f2231')

    # 低压功率等级替代（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Power Level Electric Substitution_429E')
    def test_caseid_1981509_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x429e, SESSION.PROGRAMMING, '7f2231')

    # 局部网络管理集群PNC（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Partial Network Cluster (PNC)_DD0B')
    def test_caseid_1981508_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xdd0b, SESSION.PROGRAMMING, '7f2231')

    # FOTA状态（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)FotaStatus_F153')
    def test_caseid_1981507_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf153, SESSION.PROGRAMMING, '7f2231')

    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Tailgate/bootlid Open/Close Counter_A00A')
    def test_caseid_1981505_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xa00a, SESSION.PROGRAMMING, '7f2231')

    # 数字钥匙当前UTC时间
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Digital Key Current UTC Time_C008')
    def test_caseid_1981504_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xc008, SESSION.PROGRAMMING, '7f2231')

    # TPMS传感器IDs（APP）
    # BGM_MCU
    @pytest.mark.sanity
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Tire Pressure Monitoring System (TPMS) Sensor IDs_281F')
    def test_caseid_1981502_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x281f, SESSION.PROGRAMMING, '7f2231')

    # 转向灯优先级（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)DI Priority_F108')
    def test_caseid_1981500_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4533, SESSION.PROGRAMMING, '7f2231')

    # Sensata TPMS软件版本（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Sensata TPMS Software Version_4503')
    def test_caseid_1981499_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4503, SESSION.PROGRAMMING, '7f2231')

    # TPMS开发帧状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)TPMS Development log message status_4504')
    def test_caseid_1981498_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4504, SESSION.PROGRAMMING, '7f2231')

    # 调节内灯目标亮度值的系统状态（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Adjust the system state of Interiorlight target value_4600')
    def test_caseid_1981496_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4600, SESSION.PROGRAMMING, '7f2231')

    # 内灯白天至黑夜值（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Interior Light Day to Night Value_416F')
    def test_caseid_1981494_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x416f, SESSION.PROGRAMMING, '7f2231')

    # 内灯黑夜至白天值（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Interior Light Night to Day Value_4170')
    def test_caseid_1981492_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4170, SESSION.PROGRAMMING, '7f2231')

    # AWM LIN消息检测（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)AWM LIN Message Detection_DA00')
    def test_caseid_1981490_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xda00, SESSION.PROGRAMMING, '7f2231')

    # 展车模式（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Exhibition Mode_D135')
    def test_caseid_1981489_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd135, SESSION.PROGRAMMING, '7f2231')

    # 方向盘加热控制（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Steering Wheel Heating Control_7023')
    def test_caseid_1981487_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x7023, SESSION.PROGRAMMING, '7f2231')

    # AWM初始化激活触发计数器（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)The counter of trigger to active AWM initialization_4200')
    def test_caseid_1981485_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4200, SESSION.PROGRAMMING, '7f2231')

    # PowerManagement可标定数据（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Power Management Config_F0F5')
    def test_caseid_1981483_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xf0f5, SESSION.PROGRAMMING, '7f2231')

    # 转向灯角度自动关闭触发角度配置值_Max（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)AutoOffAg_Max_7024')
    def test_caseid_1981481_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x7024, SESSION.PROGRAMMING, '7f2231')

    # BGM计算的小电池SOC值（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)BattSoc2Fild（Vehicle Battery State Of Charge-BGM）_4444')
    def test_caseid_1981477_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x4444, SESSION.PROGRAMMING, '7f2231')

    # SALM灯带休眠（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)SALM Sleep_D136')
    def test_caseid_1981475_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xd136, SESSION.PROGRAMMING, '7f2231')

    # 开始补电的小电池SOC阈值
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb00')
    def test_caseid_1984767_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb00, SESSION.PROGRAMMING, '7f2231')

    # BMS低SOC唤醒网络设置
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb01')
    def test_caseid_1984761_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb01, SESSION.PROGRAMMING, '7f2231')

    # BMS唤醒网络的SOC阈值
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb02')
    def test_caseid_1984765_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb02, SESSION.PROGRAMMING, '7f2231')

    # BMS低电压唤醒网络设置
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb03')
    def test_caseid_1984759_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb03, SESSION.PROGRAMMING, '7f2231')

    # BMS唤醒网络的电压阈值
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb04')
    def test_caseid_1984763_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb04, SESSION.PROGRAMMING, '7f2231')

    # BMS充电电流唤醒设置
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb05')
    def test_caseid_1984757_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb05, SESSION.PROGRAMMING, '7f2231')

    # BMS充电电流唤醒阈值
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb06')
    def test_caseid_1984753_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb06, SESSION.PROGRAMMING, '7f2231')

    # BMS放电电量唤醒设置
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb07')
    def test_caseid_1984755_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb07, SESSION.PROGRAMMING, '7f2231')

    # BMS放电电量唤醒阈值
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb08')
    def test_caseid_1984751_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb08, SESSION.PROGRAMMING, '7f2231')

    # BGM网络休眠期间主动唤醒的时间间隔
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)PrmEgyAvlDchaChrgnStartParked_bb09')
    def test_caseid_1984749_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0xbb09, SESSION.PROGRAMMING, '7f2231')

    ##1认证密钥_800V  V2.0实现
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Secret Key For Immobilizer Target #1 ECM 800V_41DE')
    def test_caseid_1985550_00(self):
        self.sd_tester.write_ccp({962: 0x02})
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41de, SESSION.PROGRAMMING, '7f2231')

    ##2认证密钥_800V  V2.0实现
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Secret Key For Immobilizer Target #2 IEM 800V_41DF')
    def test_caseid_1985548_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41df, SESSION.PROGRAMMING, '7f2231')

    ##3认证密钥_800V  V2.0实现
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Secret Key For Immobilizer Target #3 MGM 800V_41E0')
    def test_caseid_1985546_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41e0, SESSION.PROGRAMMING, '7f2231')

    ##SK IV 800V  V2.0
    # BGM_MCU
    @pytest.mark.smoke
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)Secret Key IV used in challenge/respond_41E1')
    def test_caseid_1985544_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x41e1, SESSION.PROGRAMMING, '7f2231')

    # 转向灯角度自动关闭关闭角度配置值_Min（APP）
    # BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)AutoOffAg_Min_7025')
    def test_caseid_1981479_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU, 0x7025, SESSION.PROGRAMMING, '7f2231')

    #BGM检测左前门端电压触发闭合冗余回路的电压阈值
    #BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)ULoFLDoorSysThd_BB0A')
    def test_caseid_1990646_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xbb0a,SESSION.PROGRAMMING,'7f2231')

    #BGM检测左前门端电压触发闭合冗余回路的电压阈值
    #BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)ULoFLDoorSysThd_BB0A')
    def test_caseid_1990649_00(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xbb0a,SESSION.PROGRAMMING,UnLock.L0,'7e','7f2e11',check_method=Check_Method.response,recover=False)

    #BGM检测IPM端电压触发闭合冗余回路的电压阈值
    #BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)ULoIPMSysThd_BB0B')
    def test_caseid_1990647_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xbb0b,SESSION.PROGRAMMING,'7f2231')

    #BGM检测IPM端电压触发闭合冗余回路的电压阈值
    #BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)ULoIPMSysThd_BB0B')
    def test_caseid_1990650_00(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xbb0b,SESSION.PROGRAMMING,UnLock.L0,'7e','7f2e11',check_method=Check_Method.response,recover=False)

    #BGM检测IPM端电压断开冗余回路的电压阈值
    #BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x22)ULoIPMSysRecoveryThd_BB0C')
    def test_caseid_1990648_00(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xbb0c,SESSION.PROGRAMMING,'7f2231')

    #BGM检测IPM端电压断开冗余回路的电压阈值
    #BGM_MCU
    @pytest.mark.full
    @allure.story('诊断DID')
    @allure.title('UDS_ReadDataByIdentifier(0x2E)ULoIPMSysRecoveryThd_BB0C')
    def test_caseid_1990651_00(self):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xbb0c,SESSION.PROGRAMMING,UnLock.L0,'7e','7f2e11',check_method=Check_Method.response,recover=False)

# pytest BaseTech/DiagFlash/test_diag_bgm_did.py::TestDIDApp::test_caseid_1981615
