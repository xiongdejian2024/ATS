#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_digital_key_other_abc.py
@Time         :2024/03/16 19:50:00
@Author       :hui.zhao@jiduauto.com
@Description  :数字钥匙其他未定义
"""

from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass_abc import *
from xat_ecu.api.abc_interface import *
NotifyTi = 1


@allure.feature("互联服务")
@allure.story("数字钥匙和账号/其他/KeyID同步")
class TestDigitalKeyOther(TestDigitalKeyBase):

    def pe_unlock_commom_operation(self,pe_pos:DoorPos,key_type:KeyType = KeyType.BLE_Key,key_sts:InternalExternalStatus = InternalExternalStatus.ExternalSearchSts_Found,unlock_sts:CenLockSts = CenLockSts.Unlock):
        self.mix.set_common_precontion()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
        self.bus_comm.set_4_door_lock_status(Locksts.SafeLockd)
        sleep(3)
        self.bus_comm.dk.update_keyinfos(1, [KeyInfo(key_type, key_id1, key_sts.value)])
        self.bus_comm.dk.empty_dk_data_queue()
        self.soa.empty_all()
        sleep(1)
        self.mix.push_door_outer_switch(pos=pe_pos,time_interval=0.5,pe_test=True)
        self.bus_comm.dk.ck_search_key_req(1, 2)
        self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
        sleep(1)
        self.bus_comm.check_central_lock_sts(exp_sts=unlock_sts,exp_trigsrc=LockTrigerSource.Keyls)

    @allure.title("靠近迎宾_KeyID同步")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111996?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111996(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.LightOnApproache,value=1)
        self.bus_comm.dk.send_approach_light_cmd(key_type=2, key_id=key_id4)
        self.soa.ck_key_service_unlock_event(keyid=key_id4,key_type=DigitalKeyType.BLE_Key,trigger=DigitalKeyIdTrigger.ApproachLight)

    @allure.title("靠近迎宾_KeyID同步_遍历所有KeyType")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/109810?projectId=46')
    @pytest.mark.smoke
    def test_caseid_109810(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.LightOnApproache,value=1)
        for key_type in DigitalKeyType:
            if key_type.name != "NoKeyConnected":
                self.bus_comm.dk.send_approach_light_cmd(key_type=key_type.value, key_id=key_id4)
                self.soa.ck_key_service_unlock_event(keyid=key_id4,key_type=key_type,trigger=DigitalKeyIdTrigger.ApproachLight)
            else:
                self.bus_comm.dk.send_approach_light_cmd(key_type=key_type.value, key_id=key_id4)
            sleep(1)

    @allure.title("NFC解锁_KeyID同步")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111993?projectId=46')
    @pytest.mark.smoke
    @pytest.mark.s2s_prebuild
    def test_caseid_111993(self):
        self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
        sleep(5)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.soa.ck_key_service_unlock_event(keyid=key_id1,key_type=DigitalKeyType.NFC_Card,trigger=DigitalKeyIdTrigger.Unlock)

    @allure.title("BLE解锁_KeyID同步")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111995?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111995(self):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(2)
        self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
        sleep(2)
        self.bus_comm.dk.send_rke_unlock(key_id2)
        sleep(2)
        self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,exp_trigsrc=LockSource.Telm)
        self.soa.ck_key_service_unlock_event(keyid=key_id2,key_type=DigitalKeyType.BLE_Key,trigger=DigitalKeyIdTrigger.Unlock)

    @allure.title("PE解锁_KeyID同步")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111997?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111997(self):
        self.mix.set_common_precontion()
        self.pe_unlock_commom_operation(pe_pos=DoorPos.Dirver,key_sts=InternalExternalStatus.ExternalSearchSts_Found)
        self.soa.ck_key_service_unlock_event(keyid=key_id1,key_type=DigitalKeyType.BLE_Key,trigger=DigitalKeyIdTrigger.Unlock)
        sleep(3)
                     

    @allure.title("Approach解锁KeyID同步")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111998?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111998(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave,value=1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock,value=0)
        self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.empty_dk_data_queue()
        sleep(1)
        self.bus_comm.dk.send_approach_unlock_cmd(key_type=2, key_id=key_id3)
        self.soa.ck_key_service_unlock_event(keyid=key_id3,key_type=DigitalKeyType.BLE_Key,trigger=DigitalKeyIdTrigger.Unlock)
        

    @allure.title("靠近迎宾+Approach解锁_KeyID同步")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111994?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111994(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave,value=1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.LightOnApproache,value=1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock,value=0)
        self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
        self.bus_comm.dk.send_approach_light_cmd(key_type=2, key_id=key_id4)
        self.soa.ck_key_service_unlock_event(keyid=key_id4,key_type=DigitalKeyType.BLE_Key,trigger=DigitalKeyIdTrigger.ApproachLight)
        sleep(3)
        self.bus_comm.dk.send_approach_unlock_cmd(key_type=2, key_id=key_id4)
        self.soa.ck_key_service_unlock_event(keyid=key_id4,key_type=DigitalKeyType.BLE_Key,trigger=DigitalKeyIdTrigger.Unlock)
       



    @allure.title("NFC解锁_KeyID同步+LockTrUnlckd -> LockUnlckd")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111993?projectId=46')
    @pytest.mark.smoke
    @pytest.mark.s2s_prebuild
    def test_caseid_1988833(self):
        self.bus_comm.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.io.set_door(Trunk=Door.open)
        sleep(0.5)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(5)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.soa.ck_key_service_unlock_event(keyid=key_id1,key_type=DigitalKeyType.NFC_Card,trigger=DigitalKeyIdTrigger.Unlock)

    @allure.title("连续相同触发源KeyID同步")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111995?projectId=46')
    @pytest.mark.full
    def test_caseid_1984825(self):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(2)
        self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
        sleep(2)
        self.bus_comm.dk.send_rke_unlock(key_id2)
        sleep(2)
        self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,exp_trigsrc=LockSource.Telm)
        self.soa.ck_key_service_unlock_event(keyid=key_id2,key_type=DigitalKeyType.BLE_Key,trigger=DigitalKeyIdTrigger.Unlock)

    @allure.title("设置项_近车解锁开门设置开启_诊断重启NVM存储记忆")
    @pytest.mark.restart
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994468(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0)  
        self.bus_comm.check_ApproachUnlockHmi(1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=1)  
        self.bus_comm.check_ApproachUnlockHmi(0)
        sleep(5)  # 等待NVM存储5s可存储可接受
        self.sd_tester.reset_bgm()
        time.sleep(5)
        self.bus_comm.check_ApproachUnlockHmi(0)
 
    @allure.title("设置项_近车解锁开门设置开启_休眠唤醒NVM存储记忆")
    @pytest.mark.restart
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994469(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=0)  
        self.bus_comm.check_ApproachUnlockHmi(1)  
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach, value=1)  
        self.bus_comm.check_ApproachUnlockHmi(0)
        sleep(5)  # 等待NVM存储5s可存储可接受
        self.mix.network_sleep()
        time.sleep(5)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.bus_comm.check_ApproachUnlockHmi(0)

    @allure.title("设置项_离车闭锁仅开主驾门设置开启_诊断重启NVM存储记忆")
    @pytest.mark.restart
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994472(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=0)       
        self.bus_comm.check_WalkAwayLockHmi(0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)    
        self.bus_comm.check_WalkAwayLockHmi(2)
        sleep(5)  # 等待NVM存储5s可存储可接受
        self.sd_tester.reset_bgm()
        sleep(5)
        self.bus_comm.check_WalkAwayLockHmi(2)

    @allure.title("设置项_离车闭锁仅开主驾门设置开启_休眠唤醒NVM存储记忆")
    @pytest.mark.restart
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994473(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=0)      
        self.bus_comm.check_WalkAwayLockHmi(0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)    
        self.bus_comm.check_WalkAwayLockHmi(2)
        sleep(5)  # 等待NVM存储5s可存储可接受
        self.mix.network_sleep()
        sleep(5)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.bus_comm.check_WalkAwayLockHmi(2)

    @allure.title("设置项_离车闭锁关侧门设置项开启_诊断重启NVM存储记忆")
    @pytest.mark.restart
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994470(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=0)      
        self.bus_comm.check_WalkAwayLockHmi(0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)    
        self.bus_comm.check_WalkAwayLockHmi(3)
        sleep(5)  # 等待NVM存储5s可存储可接受
        self.sd_tester.reset_bgm()
        sleep(5)
        self.bus_comm.check_WalkAwayLockHmi(3)

    @allure.title("设置项_离车闭锁关侧门设置项开启_休眠唤醒NVM存储记忆")
    @pytest.mark.restart
    @pytest.mark.full
    @pytest.mark.nvm
    def test_caseid_1994471(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=0)      
        self.bus_comm.check_WalkAwayLockHmi(0)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=3)    
        self.bus_comm.check_WalkAwayLockHmi(3)
        sleep(5)  # 等待NVM存储5s可存储可接受
        self.mix.network_sleep()
        sleep(5)
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.bus_comm.check_WalkAwayLockHmi(3)

    @allure.title("NFC解锁_HMI闭锁_60s内RKE解锁_KeyID同步")
    @pytest.mark.full
    def test_caseid_1989023(self):
        self.bus_comm.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.io.set_door(Trunk=Door.open)
        sleep(0.5)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(5)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.soa.ck_key_service_unlock_event(keyid=key_id1,key_type=DigitalKeyType.NFC_Card,trigger=DigitalKeyIdTrigger.Unlock)

    @allure.title("PE解锁_车速闭锁_60s内PE解锁_KeyID同步")
    @pytest.mark.full
    def test_caseid_1989022(self):
        self.mix.set_common_precontion()
        self.pe_unlock_commom_operation(pe_pos=DoorPos.Dirver,key_sts=InternalExternalStatus.ExternalSearchSts_Found)
        self.soa.ck_key_service_unlock_event(keyid=key_id1,key_type=DigitalKeyType.BLE_Key,trigger=DigitalKeyIdTrigger.Unlock)

    @allure.title("PE解锁_远控闭锁_60s内PE解锁_KeyID同步")
    @pytest.mark.full
    def test_caseid_1989021(self):
        self.mix.set_common_precontion()
        self.pe_unlock_commom_operation(pe_pos=DoorPos.Dirver,key_sts=InternalExternalStatus.ExternalSearchSts_Found)
        self.soa.ck_key_service_unlock_event(keyid=key_id1,key_type=DigitalKeyType.BLE_Key,trigger=DigitalKeyIdTrigger.Unlock)

    @allure.title("BLE解锁_KeyID同步_61s时EveKeyTyp变为默认值")
    @pytest.mark.full
    def test_caseid_1988821(self):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(2)
        self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
        sleep(2)
        self.bus_comm.dk.send_rke_unlock(key_id2)
        sleep(2)
        self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,exp_trigsrc=LockSource.Telm)
        self.soa.ck_key_service_unlock_event(keyid=key_id2,key_type=DigitalKeyType.BLE_Key,trigger=DigitalKeyIdTrigger.Unlock)

    @allure.title("PE解锁_NFC锁车_KeyID同步")
    @pytest.mark.full
    def test_caseid_1988836(self):
        self.mix.set_common_precontion()
        self.pe_unlock_commom_operation(pe_pos=DoorPos.Dirver,key_sts=InternalExternalStatus.ExternalSearchSts_Found)
        self.soa.ck_key_service_unlock_event(keyid=key_id1,key_type=DigitalKeyType.BLE_Key,trigger=DigitalKeyIdTrigger.Unlock)

    @allure.title("NFC解锁_BLE闭锁_KeyID同步")
    @pytest.mark.full
    def test_caseid_1988834(self):
        self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
        sleep(5)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.RKE)
        self.soa.ck_key_service_unlock_event(keyid=key_id1,key_type=DigitalKeyType.NFC_Card,trigger=DigitalKeyIdTrigger.Unlock)

    @allure.title("Approach解锁_BLE闭锁_KeyID同步")
    @pytest.mark.full
    def test_caseid_1988832(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave,value=1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock,value=0)
        self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.empty_dk_data_queue()
        sleep(1)
        self.bus_comm.dk.send_approach_unlock_cmd(key_type=2, key_id=key_id3)
        self.soa.ck_key_service_unlock_event(keyid=key_id3,key_type=DigitalKeyType.BLE_Key,trigger=DigitalKeyIdTrigger.Unlock)

    @allure.title("PE解锁_KeyID同步_61s时EveKeyTyp变为默认值")
    @pytest.mark.full
    def test_caseid_1988835(self):
        self.mix.set_common_precontion()
        self.pe_unlock_commom_operation(pe_pos=DoorPos.Dirver,key_sts=InternalExternalStatus.ExternalSearchSts_Found)
        self.soa.ck_key_service_unlock_event(keyid=key_id1,key_type=DigitalKeyType.BLE_Key,trigger=DigitalKeyIdTrigger.Unlock)

    @allure.title("Approach解锁KeyID同步_61s时EveKeyTyp变为默认值")
    @pytest.mark.full
    def test_caseid_1988830(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave,value=1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock,value=0)
        self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.empty_dk_data_queue()
        sleep(1)
        self.bus_comm.dk.send_approach_unlock_cmd(key_type=2, key_id=key_id3)
        self.soa.ck_key_service_unlock_event(keyid=key_id3,key_type=DigitalKeyType.BLE_Key,trigger=DigitalKeyIdTrigger.Unlock)

    @allure.title("BLE解锁_NFC锁车_KeyID同步")
    @pytest.mark.full
    def test_caseid_1988824(self):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(2)
        self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
        sleep(2)
        self.bus_comm.dk.send_rke_unlock(key_id2)
        sleep(2)
        self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,exp_trigsrc=LockSource.Telm)
        self.soa.ck_key_service_unlock_event(keyid=key_id2,key_type=DigitalKeyType.BLE_Key,trigger=DigitalKeyIdTrigger.Unlock)