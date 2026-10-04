#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_charge_pile_open_charge_lid.py
@Time         :2023/1/31 17:54:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import os
import sys
import hashlib

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ""))
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
PRECHECKTI = 1

from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass_abc import *
from xat_ecu.api.abc_interface import *

@allure.feature("互联服务")
@allure.story("数字钥匙和账号/其他/SE")
class TestDigitalKeyDID(TestDigitalKeyBase):

    def before_class(self,ecu):
        super().before_class(self, ecu)
        ret_str = self.ssh.bgm_ssh.get_prop()
        self.key = ret_str[3].replace(' ', '')
        self.key = self.key.replace('\n', '')
        self.iv = ret_str[4].replace(' ', '')
        self.iv = self.iv.replace('\n', '')
        self.cmac = ret_str[5].replace(' ', '')
        self.cmac = self.cmac.replace('\n', '')
        logger.info(f"--------->:Aeskey:{self.key}")
        logger.info(f"--------->:idx_aesiv:{self.iv}")
        logger.info(f"--------->:idx_cmac:{self.cmac}")
        self.key = __import__("os").environ['XAT_CREDENTIAL_SCAN_4B3BC7EC4F7DF9F6DCCA']

    def after_class(self, ecu):
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xD905,SESSION.EXTENDED,UnLock.L5,self.key,check_method=Check_Method.response,recover=False)
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        pass
    
    def after_each_func(self, ecu):
        sleep(3)
    
    def calculate_sha256(self,data):
        sha256_hash = hashlib.sha256(data.encode()).hexdigest()
        return sha256_hash
    

    @allure.title("验证BGM支持2E 写入数字钥匙密钥MAC(DID:D905)")
    @pytest.mark.full
    def test_caseid_1987504(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xD904,SESSION.EMPTY,check_data="62d90400")
        sleep(1)
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xD903,SESSION.EXTENDED,UnLock.L5,self.key,check_data="6ed903",check_length=3,check_method=Check_Method.response,recover=False)
        sleep(1)
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xD905,SESSION.EXTENDED,UnLock.L5,self.key,check_data="6ed905",check_length=3,check_method=Check_Method.response,recover=False)
        sleep(1)
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xD904,SESSION.EMPTY,check_data="62d90400")
    
    
    @allure.title("验证BGM支持2E 写入数字钥匙安全密钥(DID:D903)同时验证BGM支持22读取数字钥匙安全密钥写入的状态(DID:DD904)")
    @pytest.mark.full
    def test_caseid_1987507(self):
        self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xD904,SESSION.EMPTY,check_data="62d90400")
        sleep(1)
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xD903,SESSION.EXTENDED,UnLock.L5,self.key,check_data="6ed903",check_length=3,check_method=Check_Method.response,recover=False)
        sleep(1)
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xD904,SESSION.EMPTY,check_data="62d90401")
        sleep(1)
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xD903,SESSION.EXTENDED,UnLock.L5,self.key,check_data="7f2e31",check_length=3,check_method=Check_Method.response,recover=False)

        # sleep(1)
        # self.bus_comm.dk.empty_dk_data_queue()
        # self.nfc_learning()
        # sleep(1)
        # self.bus_comm.dk.ck_nfc_learning_req()


    @allure.title("验证BGM不支持22读取数字钥匙安全密钥(DID:D903)")
    @pytest.mark.full
    def test_caseid_1987506(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xD903,SESSION.EMPTY,check_data="7f2231")


    @allure.title("验证写入数字钥匙安全密钥(DID:D905)时如果写入的值和存储的值不一致时，BGM会返回错误码31")
    @pytest.mark.full
    def test_caseid_1987505(self):
        error_key = __import__("os").environ['XAT_CREDENTIAL_SCAN_CE3BBDDA371F8C5CD795']
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0xD905,SESSION.EXTENDED,UnLock.L5,error_key,check_data="7f2e31",check_length=3,check_method=Check_Method.response,recover=False)

    
    @allure.title("验证BGM不支持22读取数字钥匙安全密钥(DID:D905)")
    @pytest.mark.full
    def test_caseid_1987503(self):
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xD905,SESSION.EMPTY,check_data="7f2231")

    
    @allure.title("验证BGM支持22读取数字钥匙密钥MAC(DID:D906)")
    @pytest.mark.full
    def test_caseid_1987502(self):
        KEY = int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", 16)
        logger.info(f"KEY:{KEY}")
        iv= "202122232425262728292A2B2C2D2E2F"
        IV = int(iv, 16)
        logger.info(f"iv:{IV}")

        data_1=KEY|IV
        data_2 = self.calculate_sha256(str(data_1))
        logger.info(f"MAC=SHA256（BNCM-BGM-Key||BNCM-BGM-KeyIV）计算之后的数据是: {data_2}")
        # self.sd_tester.read_did_and_check(TA.BGM_MCU,0xD906,SESSION.EMPTY,check_data="62d906"+str(data_2))
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xD906,SESSION.EMPTY,check_data="62d906")


    @allure.title("获取BGM数字钥匙当前UTC时间(DID:C008)")
    @pytest.mark.full
    def test_caseid_1987500(self):
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0xC008,SESSION.EMPTY,check_data="62c008",check_length=14)


    @allure.title("验证读写BGM解锁后的NFC持续时间(DID:4297)")
    @pytest.mark.full
    def test_caseid_1987501(self):
        #self.soa.update(["VehicleModeService_client", "VehicleSetStatusService_client"])
        self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 8)])
        sleep(5)
        self.sd_tester.write_did_and_check(TA.BGM_MCU,0x4297,SESSION.EXTENDED,UnLock.L11,"10",check_data="6e4297",check_length=4,check_method=Check_Method.response,recover=False)
        sleep(1)
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0x4297,SESSION.EMPTY,check_data="62429710")

        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        sleep(5)
        self.mix.set_PtActvnReq(up_type=UpType.SetUsageModeUp)
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_RunngRunng)
        self.bus_comm.check_usage_mode_status(usage_mode=UsageMode.DRIVING)
        self.bus_comm.check_hv_actv_for_vehmod_req(onoff=True)
        sleep(1)

        self.sd_tester.write_did_and_check(TA.BGM_MCU,0x4297,SESSION.EXTENDED,UnLock.L11,"2",check_data="6e4297",check_length=4,check_method=Check_Method.response,recover=False)
        sleep(1)
        self.sd_tester.read_did_and_check(TA.BGM_MCU,0x4297,SESSION.EMPTY,check_data="62429702")

