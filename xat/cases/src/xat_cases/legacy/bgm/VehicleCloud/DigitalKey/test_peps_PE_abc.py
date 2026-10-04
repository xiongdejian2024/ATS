#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_peps_PE_abc.py
@Time         :2024/03/23 11:50:00
@Author       :hui.zhao@jiduauto.com
@Description  :数字钥匙NFC相关功能
"""
import copy
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass_abc import *
from xat_ecu.api.abc_interface import *

# handle_ti = 0.5  # PE按下后寻钥匙
# OutdSwtPsdTi = 2.2  # 长按闭锁时间
key_id1_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

@allure.feature("互联服务")
@allure.story("数字钥匙和账号/PEPS/触碰解锁")
class TestDigitalKeyPepsPe(TestDigitalKeyBase):
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # self.set_config_info(3,1)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        self.io.set_five_door_sts(Door.close)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.HMI)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)    
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE, time_wait=1)
    
    def after_each_func(self, ecu):
        sleep(3)
        super().after_each_func(ecu)

    
    # def pe_unlock_commom_operation(self,pe_pos:DoorPos,key_type:KeyType = KeyType.BLE_Key,key_sts:InternalExternalStatus = InternalExternalStatus.ExternalSearchSts_Found,unlock_sts:CenLockSts = CenLockSts.Unlock):
    #     self.mix.set_common_precontion()
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
    #     sleep(3)
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
    #     self.bus_comm.set_4_door_lock_status(Locksts.SafeLockd)
    #     self.io.set_door(Pass=Door.close)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(key_type, key_id1, key_sts.value)])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=pe_pos,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
    #     self.io.set_door(Pass=Door.open)
    #     sleep(1)
    #     self.bus_comm.check_central_lock_sts(exp_sts=unlock_sts,exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("UWB钥匙遗留_NFC锁车")
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1990907(self):
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.NFC, timeout=3)
        self.bus_comm.set_blekeyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.BleUwbKey, zone=BLEKeyPrsntZone.Zone9)
        self.soa.check_notify_key_connect_sts(KeyType.BLE_UWB_KeyFob, isconnect=True, keyid=key_id1_1, zone=BLEKeyPrsntZone.Zone9)
        # self.bus_comm.dk.update_keyinfos(9, [KeyInfo(key_type=KeyType.BLE_UWB_KeyFob, key_id=key_id1_1, key_sts=InternalExternalStatus.SearchSts_Idle)])
        # self.soa.check_central_lock_sts_info(lock_sts=LockStatus.AllLocked,trigger_srcid=TriggerSourceId.NFC)

    @allure.title("UWB钥匙遗留_离车锁车")
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1990908(self):
        self.bus_comm.dk.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch, timeout=3)
        self.bus_comm.set_blekeyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.BleUwbKey, zone=BLEKeyPrsntZone.Zone7)
        self.soa.check_notify_key_connect_sts(KeyType.BLE_UWB_KeyFob, isconnect=True, keyid=key_id1_1, zone=BLEKeyPrsntZone.Zone7)
        # self.soa.check_central_lock_sts_info(lock_sts=LockStatus.AllLocked,trigger_srcid=TriggerSourceId.Approach)

    @allure.title("UWB钥匙遗留_远控锁车")
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1990909(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.Telm)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm, timeout=3)
        self.bus_comm.set_blekeyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.BleUwbKey, zone=BLEKeyPrsntZone.Zone6)
        self.soa.check_notify_key_connect_sts(KeyType.BLE_UWB_KeyFob, isconnect=True, keyid=key_id1_1, zone=BLEKeyPrsntZone.Zone6)
        # self.soa.check_central_lock_sts_info(lock_sts=LockStatus.AllLocked,trigger_srcid=TriggerSourceId.Telematices)

    @allure.title("UWB钥匙遗留_车外按钮锁车")
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1990910(self):
        self.mix.push_door_outer_switch()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls, timeout=3)
        self.bus_comm.set_blekeyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.BleUwbKey, zone=BLEKeyPrsntZone.Zone1)
        self.soa.check_notify_key_connect_sts(KeyType.BLE_UWB_KeyFob, isconnect=True, keyid=key_id1_1, zone=BLEKeyPrsntZone.Zone1)
        # self.soa.check_central_lock_sts_info(lock_sts=LockStatus.AllLocked,trigger_srcid=TriggerSourceId.KeyLessPassive)

    @allure.title("UWB钥匙遗留_蓝牙锁车")
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1990911(self):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=3)
        self.bus_comm.set_blekeyconnected_and_keytype_sts(keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.BleUwbKey, zone=BLEKeyPrsntZone.Zone3)
        self.soa.check_notify_key_connect_sts(KeyType.BLE_UWB_KeyFob, isconnect=True, keyid=key_id1_1, zone=BLEKeyPrsntZone.Zone3)
        # self.soa.check_central_lock_sts_info(lock_sts=LockStatus.AllLocked,trigger_srcid=TriggerSourceId.RemoteKey)

    # @allure.title("PE解锁成功_左前门_寻钥匙")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    # @pytest.mark.full
    # def test_caseid_110001(self):
    #     self.mix.set_common_precontion()
    #     for key_sts in [InternalExternalStatus.ExternalSearchSts_Found,InternalExternalStatus.ExternalSearchSts_FrntFound,
    #                     InternalExternalStatus.ExternalSearchSts_LeftFnd,InternalExternalStatus.ExternalSearchSts_LeftFnd_RearFnd,
    #                     InternalExternalStatus.ExternalSearchSts_RearFnd,InternalExternalStatus.ExternalSearchSts_RightFnd,
    #                     InternalExternalStatus.ExternalSearchSts_RightFnd_RearFnd,InternalExternalStatus.InternalSearchSts_Found]:
    #         self.pe_unlock_commom_operation(pe_pos=DoorPos.Dirver,key_sts=key_sts)
    #         sleep(3)

    
    # @allure.title("PE解锁成功_右前门_寻钥匙")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_2(self):
    #     self.mix.set_common_precontion()
    #     for key_sts in [InternalExternalStatus.ExternalSearchSts_Found,InternalExternalStatus.ExternalSearchSts_FrntFound,
    #                     InternalExternalStatus.ExternalSearchSts_LeftFnd,InternalExternalStatus.ExternalSearchSts_LeftFnd_RearFnd,
    #                     InternalExternalStatus.ExternalSearchSts_RearFnd,InternalExternalStatus.ExternalSearchSts_RightFnd,
    #                     InternalExternalStatus.ExternalSearchSts_RightFnd_RearFnd,InternalExternalStatus.InternalSearchSts_Found]:
    #         self.pe_unlock_commom_operation(pe_pos=DoorPos.Pass,key_sts=key_sts)
    #         sleep(3)
    
    # @allure.title("PE解锁成功_左后门_寻钥匙")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_3(self):
    #     self.mix.set_common_precontion()
    #     for key_sts in [InternalExternalStatus.ExternalSearchSts_Found,InternalExternalStatus.ExternalSearchSts_FrntFound,
    #                     InternalExternalStatus.ExternalSearchSts_LeftFnd,InternalExternalStatus.ExternalSearchSts_LeftFnd_RearFnd,
    #                     InternalExternalStatus.ExternalSearchSts_RearFnd,InternalExternalStatus.ExternalSearchSts_RightFnd,
    #                     InternalExternalStatus.ExternalSearchSts_RightFnd_RearFnd,InternalExternalStatus.InternalSearchSts_Found]:
    #         self.pe_unlock_commom_operation(pe_pos=DoorPos.RearLeft,key_sts=key_sts)
    #         sleep(3)
        
    
    # @allure.title("PE解锁成功_右后门_寻钥匙")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_4(self):
    #     self.mix.set_common_precontion()
    #     for key_sts in [InternalExternalStatus.ExternalSearchSts_Found,InternalExternalStatus.ExternalSearchSts_FrntFound,
    #                     InternalExternalStatus.ExternalSearchSts_LeftFnd,InternalExternalStatus.ExternalSearchSts_LeftFnd_RearFnd,
    #                     InternalExternalStatus.ExternalSearchSts_RearFnd,InternalExternalStatus.ExternalSearchSts_RightFnd,
    #                     InternalExternalStatus.ExternalSearchSts_RightFnd_RearFnd,InternalExternalStatus.InternalSearchSts_Found]:
    #         self.pe_unlock_commom_operation(pe_pos=DoorPos.RearRight,key_sts=key_sts)
    #         sleep(3)

    
    # @allure.title("PE解锁成功_尾门_寻钥匙")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_5(self):
    #     self.mix.set_common_precontion()
    #     for key_sts in [InternalExternalStatus.ExternalSearchSts_Found,InternalExternalStatus.ExternalSearchSts_FrntFound,
    #                     InternalExternalStatus.ExternalSearchSts_LeftFnd,InternalExternalStatus.ExternalSearchSts_LeftFnd_RearFnd,
    #                     InternalExternalStatus.ExternalSearchSts_RearFnd,InternalExternalStatus.ExternalSearchSts_RightFnd,
    #                     InternalExternalStatus.ExternalSearchSts_RightFnd_RearFnd,InternalExternalStatus.InternalSearchSts_Found]:
    #         self.pe_unlock_commom_operation(pe_pos=DoorPos.Tailgate,key_sts=key_sts,unlock_sts=CenLockSts.TrUnlock)
    #         sleep(3)
    

    # @allure.title("PE解锁失败_左前门_未能寻到钥匙")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_6(self):
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
    #     self.bus_comm.set_4_door_lock_status(Locksts.SafeLockd)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     sleep(2)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)



    # @allure.title("PE解锁失败_左前门_钥匙反馈状态为Idle/NotFound")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_7(self):
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
    #     self.bus_comm.set_4_door_lock_status(Locksts.SafeLockd)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 1)])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     sleep(2)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 9)])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     sleep(2)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
        
    
    # @allure.title("PE解锁失败_右前门_未能寻到钥匙")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_8(self):
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
    #     self.bus_comm.set_4_door_lock_status(Locksts.SafeLockd)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     sleep(2)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)



    # @allure.title("PE解锁失败_右前门_钥匙反馈状态为Idle/NotFound")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_9(self):
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
    #     self.bus_comm.set_4_door_lock_status(Locksts.SafeLockd)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 1)])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     sleep(2)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 9)])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     sleep(2)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
    
    # @allure.title("PE解锁失败_左后门_未能寻到钥匙")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_10(self):
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
    #     self.bus_comm.set_4_door_lock_status(Locksts.SafeLockd)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     sleep(2)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)



    # @allure.title("PE解锁失败_左后门_钥匙反馈状态为Idle/NotFound")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_11(self):
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
    #     self.bus_comm.set_4_door_lock_status(Locksts.SafeLockd)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 1)])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     sleep(2)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 9)])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     sleep(2)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
    
    # @allure.title("PE解锁失败_右后门_未能寻到钥匙")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_12(self):
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
    #     self.bus_comm.set_4_door_lock_status(Locksts.SafeLockd)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     sleep(2)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)



    # @allure.title("PE解锁失败_右后门_钥匙反馈状态为Idle/NotFound")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_13(self):
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
    #     self.bus_comm.set_4_door_lock_status(Locksts.SafeLockd)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 1)])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     sleep(2)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 9)])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     sleep(2)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
    
    # @allure.title("PE解锁失败_尾门_未能寻到钥匙")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_14(self):
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
    #     self.bus_comm.set_4_door_lock_status(Locksts.SafeLockd)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     sleep(2)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)

    # @allure.title("PE解锁失败_尾门_钥匙反馈状态为Idle/NotFound")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_15(self):
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
    #     self.bus_comm.set_4_door_lock_status(Locksts.SafeLockd)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 1)])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     sleep(2)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 9)])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     sleep(2)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)

    # '''
    # @allure.title("PE解锁成功_左前_寻的NFC钥匙,钥匙状态为InternalSearchSts_Found")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112276?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_16(self):
    #     self.mix.set_common_precontion()
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.RKE)
    #     sleep(3)
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.NFC_Card, key_id1, 0x8)])
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)
    
    # @allure.title("PE解锁成功_右前_寻的NFC钥匙,钥匙状态为InternalSearchSts_Found")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112276?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_17(self):
    #     self.mix.set_common_precontion()
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.RKE)
    #     sleep(3)
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.NFC_Card, key_id1, 0x8)])
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Pass,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)
    
    # @allure.title("PE解锁成功_左后_寻的NFC钥匙,钥匙状态为InternalSearchSts_Found")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112276?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_18(self):
    #     self.mix.set_common_precontion()
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.RKE)
    #     sleep(3)
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     self.mix.push_door_outer_switch(pos=DoorPos.RearLeft,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)
    
    # @allure.title("PE解锁成功_右后_寻的NFC钥匙,钥匙状态为InternalSearchSts_Found")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112276?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_19(self):
    #     self.mix.set_common_precontion()
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.RKE)
    #     sleep(3)
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     self.mix.push_door_outer_switch(pos=DoorPos.RearRight,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)

    
    # @allure.title("PE解锁成功_尾门_寻的NFC钥匙,钥匙状态为InternalSearchSts_Found")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112276?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_20(self):
    #     self.mix.set_common_precontion()
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.RKE)
    #     sleep(3)
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.NFC_Card, key_id1, 0x8)])
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock)
    # '''
    
    # @allure.title("PE解锁成功_左前_多个钥匙存在")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112276?projectId=46')
    # @pytest.mark.full
    # def test_caseid_100001_21(self):
    #     self.mix.set_common_precontion()
    #     # self.bus_comm.set_4_door_lock_status(Locksts.SafeLockd)
    #     # self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.RKE)
    #     self.bus_comm.dk.set_cenlock_sts(3)
    #     sleep(3)
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.NFC_Card, key_id1, 0x8),KeyInfo(KeyType.BLE_Key, key_id2, 0x1), KeyInfo(KeyType.BLE_Key, key_id3, 0x6)])
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,exp_trigsrc=LockTrigerSource.Keyls)

    
    
    # @allure.title("PE解锁失败_尾门_未能寻到钥匙")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112245?projectId=46')
    # @pytest.mark.full_01
    # def test_caseid_100001_22(self):
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
    #     self.bus_comm.set_4_door_lock_status(Locksts.SafeLockd)
    #     sleep(3)
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x1)])
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     sleep(1)
    #     self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(1, 2)
    #     sleep(2)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock)
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)


    # @allure.title("PE解锁开尾门成功_ACTIVE")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112261?projectId=46')
    # @pytest.mark.full
    # def test_caseid_112261(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,ccp={94: 0x02})
    #     self.bus_comm.dk.set_cenlock_sts(3)
    #     #self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
    #     self.bus_comm.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x0B)])
    #     sleep(3)
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     self.mix.push_door_outer_switch(pos=DoorPos.Tailgate,time_interval=0.5,pe_test=True)
    #     self.bus_comm.dk.ck_search_key_req(0x01, 0x02)
    #     self.bus_comm.dk.ck_cenlock_sts(2, 2)