#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_charge_lid_abc.py
@Time         :2024/03/15 10:50:21
@Author       :hui.zhao@jiduauto.com
@Description  :数字钥匙充电盖相关
"""

from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass_abc import *
from xat_ecu.api.abc_interface import *

@allure.feature("互联服务")
@allure.story("数字钥匙和账号/PEPS/近车自动解锁")
class TestDigitalKeyApproach(TestDigitalKeyBase):
    @allure.title("近车解锁_解锁成功_LockSts_LockTrUnlckd+ACTIVE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112306?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112306(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE,ccp={94: 0x80, 98: 0x2, 10: 0x2})
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach,value=1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock,value=0)
        sleep(1)
        self.bus_comm.dk.send_approach_unlock_cmd()
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver,door_req= DoorOpenerReq.OpenMinang,trigger_src=LockTrigerSource.KeyRem)
        self.bus_comm.check_door_lock_req(door_pos=DoorPos.Dirver,req=DoorLockCmd.Unlck)


    @allure.title("近车解锁_解锁成功_LockSts_LockTrUnlckd+CONVENIENCE+DrvrSeat_not_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112305?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112305(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,ccp={94: 0x80})
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnApproach,value=1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.DoorAutoOpenOnUnlock,value=0)
        sleep(1)
        self.bus_comm.dk.send_approach_unlock_cmd()
        self.bus_comm.check_door_opener_req(drv_opener=DoorPos.Dirver,door_req= DoorOpenerReq.OpenMinang,trigger_src=LockTrigerSource.KeyRem)
        self.bus_comm.check_door_lock_req(door_pos=DoorPos.Dirver,req=DoorLockCmd.Unlck)
