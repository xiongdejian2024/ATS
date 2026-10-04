#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_rke_car_locator_abc.py
@Time         :2024/03/21 10:50:21
@Author       :hui.zhao@jiduauto.com
@Description  :数字钥匙充电盖相关
"""

from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass_abc import *
from xat_ecu.api.abc_interface import *

@allure.feature("互联服务") 
@allure.story("数字钥匙和账号/RKE/蓝牙解闭锁")
class TestDigitalKeyRkeLockControl(TestDigitalKeyBase):
    
    def check_usage_mode_fail(self,usage:UsageMode,operation:str,seat_pres_sts:list=[]):
        logger.info(f"设置UsageMode为:{usage.name}")
        self.sd_tester.change_usage_mode(usage_mode=usage)
        sleep(0.5)
        
        for item in seat_pres_sts:
            if "Drv" == item:
                logger.info(f"设椅驾驶位座椅为在位状态")
                self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
            if "Pass" == item:
                logger.info(f"设置副驾驶位座椅为在位状态")
                self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
            if "RL" == item:
                logger.info(f"设置左后座椅在位为在位状态")
                self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
            if "RM" == item:
                logger.info(f"设置后中座椅在位为在位状态")
                self.mix.set_seats_present_sts(sec_mid=SeatPresSts.Pres)
            if "RR" == item:
                logger.info(f"设置右后座椅为在位状态")
                self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
            if "FrontAll" == item:
                logger.info(f"设置前排座椅为在位状态")
                self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
                self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
            if "RearAll" == item:
                logger.info(f"设置后排座椅为在位状态")
                self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
                self.mix.set_seats_present_sts(sec_mid=SeatPresSts.Pres)
                self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
            if "All" == item:
                logger.info(f"设置所有座椅为在位状态")
                self.mix.set_all_seats_present_sts(seat_pres_sts=SeatPresSts.Pres)
        sleep(0.5)

        if operation.lower() == "lock":
            self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.HMI)
            sleep(3)
            self.bus_comm.dk.empty_dk_data_queue()
            self.bus_comm.dk.send_rke_lock()
            self.bus_comm.dk.ck_rke_resp(1, 1, "UsageModeFail", exec_type=3)
            self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)
        elif operation.lower() == "unlock":
            self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.HMI)
            sleep(3)
            self.bus_comm.dk.empty_dk_data_queue()
            self.bus_comm.dk.send_rke_unlock()
            self.bus_comm.dk.ck_rke_resp(1, 1, "UsageModeFail", exec_type=3)
            self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
        elif operation.lower() == "lock_close_door":
            self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.HMI)
            sleep(3)
            self.bus_comm.dk.empty_dk_data_queue()
            self.bus_comm.dk.send_rke_close_door_and_lock()
            self.bus_comm.dk.ck_rke_resp(1, 1, "UsageModeFail", exec_type=3)
            self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)

    def check_lock_any_door_open_fail(self,usage:UsageMode,door_open_pos:list=[]):
        logger.info("设置中控锁为Unlock状态")
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.HMI)
        sleep(2)
        self.bus_comm.dk.empty_dk_data_queue()
        logger.info(f"设置UsageMode为:{usage.name}")
        self.sd_tester.change_usage_mode(usage_mode=usage)
        sleep(0.5)
        # self.mix.set_all_seats_present_sts(SeatPresSts.NoPres)
        for item in door_open_pos:
            if "Drv" == item:
                logger.info("主驾门打开")
                self.io.set_door(Drvr=Door.open)
                self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
            if "Pass" == item:
                logger.info(f"副驾驾门打开")
                self.io.set_door(Pass=Door.open)
                self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
            if "RL" == item:
                logger.info(f"左后门打开")
                self.io.set_door(LeRe=Door.open)
                self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullOpend)
            if "RR" == item:
                logger.info(f"右后门打开")
                self.io.set_door(RiRe=Door.open)
                self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullOpend)
            if "Tailgate" == item:
                logger.info(f"尾门打开")
                self.io.set_door(Trunk=Door.open)
                self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullOpend)
            if "FrontAll" == item:
                logger.info(f"前排门打开")
                self.io.set_door(Drvr=Door.open)
                self.io.set_door(Pass=Door.open)
                self.bus_comm.set_door_opener_sts(drv_opener=DoorOpenerSts.FullOpend)
                self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
            if "RearAll" == item:
                logger.info(f"后排门打开")
                self.io.set_door(LeRe=Door.open)
                self.io.set_door(RiRe=Door.open)
                self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullOpend)
                self.bus_comm.set_door_opener_sts(rire_opener=DoorOpenerSts.FullOpend)
            if "All" == item:
                logger.info(f"所有门打开")
                self.io.set_five_door_sts(Door.open)
                self.bus_comm.set_five_door_opener_sts(DoorOpenerSts.FullOpend)
        sleep(1)
        self.bus_comm.dk.send_rke_lock()
        self.bus_comm.dk.ck_rke_resp(1, 1, "AnyDoorOpenFail", exec_type=3)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock)

    def set_four_door_sts(self,sts:Door):
        if sts.name == "close":
            logger.info(f"设置四门状态为关闭")
            self.io.set_door(Drvr=Door.close,Pass=Door.close,LeRe=Door.close,RiRe=Door.close)
            self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        elif sts.name == "open":
            logger.info(f"设置四门状态为打开")
            self.io.set_door(Drvr=Door.open,Pass=Door.open,LeRe=Door.open,RiRe=Door.open)
            self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)

        

    @allure.title("RKE解锁_Success_INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112142(self):
        self.mix.set_common_precontion()
        self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
        sleep(1)
        self.bus_comm.dk.send_rke_unlock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_four_door_lock_cmd(1)
        self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(1)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)


    @allure.title("RKE联动关门_Success_INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359593?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112200(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id2, 0x8)])
        self.io.set_door(Pass=Door.open)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_close_door_and_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_door_opener_cmd(2, 2)
        self.io.set_door(Pass=Door.close)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.dk.ck_four_door_lock_cmd(2)
        self.bus_comm.set_4_door_lock_status(Locksts.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    
    @allure.title("联动关门_ResultOK_ABANDONED+车内无人")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112199?projectId=46')
    @pytest.mark.full
    def test_caseid_112199(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id2, 0x8)])
        self.io.set_door(Pass=Door.open)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_close_door_and_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_door_opener_cmd(2, 2)
        self.io.set_door(Pass=Door.close)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.dk.ck_four_door_lock_cmd(2)
        self.bus_comm.set_4_door_lock_status(Locksts.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    
    # @allure.title("验证在Abandoned模式下执行解锁命令，当锁状态从AllLocked跳转到Unlocked时，BGM会发出设置数字钥匙应用提供的解锁事件")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112199?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1987524(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
    #     self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
    #     sleep(3)
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     self.bus_comm.dk.send_rke_unlock()
    #     self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
    #     self.bus_comm.dk.ck_four_door_lock_cmd(1)
    #     self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,exp_trigsrc=LockTrigerSource.KeyRem)
    #     self.soa.ck_key_service_unlock_event(keyid=key_id2,key_type=DigitalKeyType.BLE_Key,trigger=DigitalKeyIdTrigger.Unlock)
    #     self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)


    @allure.title("RKE闭锁_Success_ABANDONED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112181?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112181(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_four_door_lock_cmd(2)
        self.bus_comm.set_4_door_lock_status(Locksts.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    # @allure.title("RKE闭锁_Success_ABANDONED")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112181?projectId=46')
    # @pytest.mark.smoke
    # def test_caseid_112181_1(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
    #     self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
    #     sleep(3)
    #     self.bus_comm.dk.empty_dk_data_queue()
    #     self.bus_comm.dk.send_rke_lock()
    #     self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
    #     self.bus_comm.dk.ck_four_door_lock_cmd(2)
    #     self.bus_comm.set_4_door_lock_status(Locksts.Lockd)
    #     self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,exp_trigsrc=LockTrigerSource.IntrSwt)
    #     self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)
    
    @allure.title("RKE解锁_Success_ABANDONED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359631?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112164(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_unlock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_four_door_lock_cmd(1)
        self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(1)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    
    @allure.title("闭锁_Success_ INACTIVE+车内无人")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112150?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112150(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.RKE)
        sleep(3)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_four_door_lock_cmd(2)
        self.bus_comm.set_4_door_lock_status(Locksts.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock)
        sleep(1)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)
    

    # @allure.title("RKE闭锁_AnyDoorOpenFail_Convenience+驾驶位门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_38(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["Drv"])
    
    # @allure.title("RKE闭锁_AnyDoorOpenFail_Convenience+副驾门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_39(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["Pass"])
    
    # @allure.title("RKE闭锁_AnyDoorOpenFail_Convenience+左前门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_40(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["RL"])
    
    # @allure.title("RKE闭锁_AnyDoorOpenFail_Convenience+右后门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_41(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["RR"])
    
    # @allure.title("RKE闭锁_AnyDoorOpenFail_Convenience+尾门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_42(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["Tailgate"])
    
    # @allure.title("RKE闭锁_AnyDoorOpenFail_Convenience+前排门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_43(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["FrontAll"])

    # @allure.title("RKE闭锁_AnyDoorOpenFail_Convenience+后排门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_44(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["RearAll"])
    
    # @allure.title("RKE闭锁_AnyDoorOpenFail_Convenience+所有门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_45(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["All"])
    
    # @allure.title("RKE闭锁_AnyDoorOpenFail_Abandoned+前排门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_19(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.ABANDONED,door_open_pos = ["FrontAll"])

    # @allure.title("RKE闭锁_AnyDoorOpenFail_Abandoned+后排门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_20(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.ABANDONED,door_open_pos = ["RearAll"])
    
    # @allure.title("RKE闭锁_AnyDoorOpenFail_Abandoned+所有门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_21(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.ABANDONED,door_open_pos = ["All"])

    
    # @allure.title("RKE闭锁_AnyDoorOpenFail_Abandoned+驾驶位门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_22(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["Drv"])
    
    # @allure.title("RKE闭锁_AnyDoorOpenFail_Abandoned+副驾门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_23(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["Pass"])
    
    # @allure.title("RKE闭锁_AnyDoorOpenFail_Abandoned+左前门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_24(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["RL"])
    
    # @allure.title("RKE闭锁_AnyDoorOpenFail_Abandoned+右后门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_25(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["RR"])
    
    # @allure.title("RKE闭锁_AnyDoorOpenFail_Abandoned+尾门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_26(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["Tailgate"])
    
    # @allure.title("RKE闭锁_AnyDoorOpenFail_Abandoned+前排门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_27(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["FrontAll"])

    # @allure.title("RKE闭锁_AnyDoorOpenFail_Abandoned+后排门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_28(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["RearAll"])
    
    # @allure.title("RKE闭锁_AnyDoorOpenFail_Abandoned+所有门开")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1000002_29(self):
    #     self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["All"])


    @allure.title("联动关门_ResultOK_Convenience +车内无人")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359593?projectId=46')
    @pytest.mark.smoke
    def test_caseid_1987334(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id2, 0x8)])
        self.set_four_door_sts(Door.open)
        self.bus_comm.dk.empty_dk_data_queue()

        self.bus_comm.dk.send_rke_close_door_and_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_door_opener_cmd(1, 2)
        self.bus_comm.dk.ck_door_opener_cmd(2, 2)
        self.bus_comm.dk.ck_door_opener_cmd(3, 2)
        self.bus_comm.dk.ck_door_opener_cmd(4, 2)
        self.set_four_door_sts(Door.close)
        self.bus_comm.dk.ck_four_door_lock_cmd(2)
        self.bus_comm.set_4_door_lock_status(Locksts.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    
    @allure.title("联动关门_ResultOK_Convenience +车内有人 + 副驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359593?projectId=46')
    @pytest.mark.smoke
    def test_caseid_1987335(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id2, 0x8)])
        self.io.set_door(Drvr=Door.open,Pass=Door.open,LeRe=Door.open,RiRe=Door.open)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.dk.empty_dk_data_queue()

        self.bus_comm.dk.send_rke_close_door_and_lock()
        self.soa.check_Play2_req(app='RKE',txt='关门请当心',param='{"isLoopPlay":False,"priority":1,"streamType":6,"zone":0}',timeout=10)
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_door_opener_cmd(2, 2)
        self.io.set_door(Drvr=Door.close,Pass=Door.close,LeRe=Door.close,RiRe=Door.close)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.dk.ck_four_door_lock_cmd(2)
        self.bus_comm.set_4_door_lock_status(Locksts.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("联动关门_ResultOK_INACTIVE +车内有人 + 左后占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987337?projectId=46')
    @pytest.mark.smoke
    def test_caseid_1987337(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id2, 0x8)])
        self.io.set_door(Drvr=Door.open,Pass=Door.open,LeRe=Door.open,RiRe=Door.open)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.dk.empty_dk_data_queue()

        self.bus_comm.dk.send_rke_close_door_and_lock()
        self.soa.check_Play2_req(app='RKE',txt='关门请当心',param='{"isLoopPlay":False,"priority":1,"streamType":6,"zone":0}',timeout=10)
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_door_opener_cmd(3, 2)
        self.io.set_door(Drvr=Door.close,Pass=Door.close,LeRe=Door.close,RiRe=Door.close)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.dk.ck_four_door_lock_cmd(2)
        self.bus_comm.set_4_door_lock_status(Locksts.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)
    
    @allure.title("解锁_Success_Convenience")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.smoke
    def test_caseid_1987338(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.dk.empty_dk_data_queue()
        sleep(3)
        self.bus_comm.dk.send_rke_unlock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_four_door_lock_cmd(1)
        self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(1)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    
    @allure.title("解锁_UsageModeFail_Active")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.full
    def test_caseid_1987299(self):
        self.check_usage_mode_fail(usage=UsageMode.ACTIVE,operation="unlock",seat_pres_sts=[])

    
    @allure.title("解锁_UsageModeFail_Convenience+挡位非P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.full
    def test_caseid_1987302(self):
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.check_usage_mode_fail(usage=UsageMode.ACTIVE,operation="unlock",seat_pres_sts=[])

    
    @allure.title("联动关门_UsageModeFail_Abandoned+挡位R挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.full
    def test_caseid_1987533(self):
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.check_usage_mode_fail(usage=UsageMode.DRIVING,operation="lock_close_door",seat_pres_sts=[])

    
    @allure.title("联动关门_UsageModeFail_Active")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.full
    def test_caseid_1987298(self):
        self.check_usage_mode_fail(usage=UsageMode.ACTIVE,operation="lock_close_door",seat_pres_sts=[])

    
    @allure.title("联动关门_UsageModeFail_Convenience+挡位非P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.full
    def test_caseid_1987301(self):
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.check_usage_mode_fail(usage=UsageMode.CONVENIENCE,operation="lock_close_door",seat_pres_sts=[])

    @allure.title("联动关门_UsageModeFail_Inactive+挡位D挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.full
    def test_caseid_1987532(self):
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.check_usage_mode_fail(usage=UsageMode.ACTIVE,operation="lock_close_door",seat_pres_sts=[])

    
    @allure.title("解锁_UsageModeFail_Abandoned+挡位R挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.full
    def test_caseid_1987531(self):
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.check_usage_mode_fail(usage=UsageMode.ACTIVE,operation="unlock",seat_pres_sts=[])

    
    @allure.title("解锁_UsageModeFail_Inactive+挡位D挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.full
    def test_caseid_1987530(self):
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.check_usage_mode_fail(usage=UsageMode.DRIVING,operation="unlock",seat_pres_sts=[])

    
    @allure.title("闭锁_UsageModeFail_Abandoned+挡位D挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.full
    def test_caseid_1987529(self):
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.check_usage_mode_fail(usage=UsageMode.ACTIVE,operation="lock",seat_pres_sts=[])
    
    @allure.title("闭锁_UsageModeFail_Active")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.full
    def test_caseid_1987300(self):
        self.check_usage_mode_fail(usage=UsageMode.ACTIVE,operation="lock",seat_pres_sts=[])
    
    @allure.title("闭锁_UsageModeFail_Convenience+挡位非P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.full
    def test_caseid_1987528(self):
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.check_usage_mode_fail(usage=UsageMode.CONVENIENCE,operation="lock",seat_pres_sts=[])

    @allure.title("闭锁_UsageModeFail_Convenience+挡位非P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.full
    def test_caseid_1987303(self):
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.check_usage_mode_fail(usage=UsageMode.CONVENIENCE,operation="lock",seat_pres_sts=[])

    @allure.title("闭锁_Success_ INACTIVE+车内有人 + 右后占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.smoke
    def test_caseid_1987342(self):
        self.mix.set_common_precontion()
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        # self.bus_comm.dk.ck_four_door_lock_cmd(1)
        self.bus_comm.set_4_door_lock_status(Locksts.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(1)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    
    @allure.title("闭锁_Success_ABANDONED+车内有人 + 副驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.smoke
    def test_caseid_1987341(self):
        self.mix.set_common_precontion()
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        # self.bus_comm.dk.ck_four_door_lock_cmd(1)
        self.bus_comm.set_4_door_lock_status(Locksts.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(1)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    
    @allure.title("闭锁_Success_Convenience+ 主驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.smoke
    def test_caseid_1987340(self):
        self.mix.set_common_precontion()
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(3)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        # self.bus_comm.dk.ck_four_door_lock_cmd(3)
        self.bus_comm.set_4_door_lock_status(Locksts.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,exp_trigsrc=LockTrigerSource.IntrSwt)
        sleep(1)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    
    @allure.title("闭锁_Success_Convenience+车内无人")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112142?projectId=46')
    @pytest.mark.smoke
    def test_caseid_1987339(self):
        self.mix.set_common_precontion()
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(3)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        # self.bus_comm.dk.ck_four_door_lock_cmd(3)
        self.bus_comm.set_4_door_lock_status(Locksts.Lockd)
        # self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(1)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    
    @allure.title("闭锁_AnyDoorOpenFail_右前门开+Abandoned")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    @pytest.mark.full
    def test_caseid_1987308(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.ABANDONED,door_open_pos = ["Pass"])

    
    @allure.title("闭锁_AnyDoorOpenFail_右前门开+Convenience")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    @pytest.mark.full
    def test_caseid_1987313(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["Pass"])

    
    @allure.title("闭锁_AnyDoorOpenFail_右后门开 + Abandoned")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    @pytest.mark.full
    def test_caseid_1987307(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.ABANDONED,door_open_pos = ["RR"])
    
    @allure.title("闭锁_AnyDoorOpenFail_右后门开 + Convenience")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    @pytest.mark.full
    def test_caseid_1987312(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["RR"])
    
    @allure.title("闭锁_AnyDoorOpenFail_尾门开+Abandoned")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    @pytest.mark.full
    def test_caseid_1987306(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.ABANDONED,door_open_pos = ["Tailgate"])
    
    @allure.title("闭锁_AnyDoorOpenFail_尾门开+Convenience")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    @pytest.mark.full
    def test_caseid_1987311(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.ABANDONED,door_open_pos = ["Tailgate"])
    
    @allure.title("闭锁_AnyDoorOpenFail_左前门开+Abandoned")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    @pytest.mark.full
    def test_caseid_1987305(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.ABANDONED,door_open_pos = ["Drv"])

    @allure.title("闭锁_AnyDoorOpenFail_左前门开+Convenience")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    @pytest.mark.full
    def test_caseid_1987310(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["Drv"])
    
    @allure.title("闭锁_AnyDoorOpenFail_左后门开+Abandoned")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    @pytest.mark.full
    def test_caseid_1987304(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.ABANDONED,door_open_pos = ["RL"])
    
    @allure.title("闭锁_AnyDoorOpenFail_左后门开+Convenience")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112180?projectId=46')
    @pytest.mark.full
    def test_caseid_1987309(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["RL"])

    
    @allure.title("闭锁_AnyDoorOpenFail_左后门开+Inactve")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112192?projectId=46')
    @pytest.mark.full
    def test_caseid_112192(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["RL"])
    

    @allure.title("闭锁_AnyDoorOpenFail_左前门开+Inactve")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112139?projectId=46')
    @pytest.mark.full
    def test_caseid_112139(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["Drv"])

    @allure.title("闭锁_AnyDoorOpenFail_尾门开+Inactve")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112190?projectId=46')
    @pytest.mark.full
    def test_caseid_112190(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["Tailgate"])


    @allure.title("闭锁_AnyDoorOpenFail_右后门开 + Inactive")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112178?projectId=46')
    @pytest.mark.full
    def test_caseid_112178(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["RR"])


    @allure.title("闭锁_AnyDoorOpenFail_右前门开+Inactive")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112141?projectId=46')
    @pytest.mark.sanity
    def test_caseid_112141(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["Pass"])
    
    @allure.title("联动关门_DoorCloseFail_左后门开+INACTIVE +车内无人")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112196?projectId=46')
    @pytest.mark.full
    def test_caseid_112196(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["RL"])


    @allure.title("联动关门_DoorCloseFail_左前门开+INACTIVE +车内无人")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112159?projectId=46')
    @pytest.mark.full
    def test_caseid_112159(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["Drv"])

    @allure.title("联动关门_DoorCloseFail_尾门开+INACTIVE +车内无人")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112143?projectId=46')
    @pytest.mark.full
    def test_caseid_112143(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["Tailgate"])


    @allure.title("联动关门_DoorCloseFail_右后门开+INACTIVE+车内有人")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112171?projectId=46')
    @pytest.mark.full
    def test_caseid_112171(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["RR"])


    @allure.title("联动关门_DoorCloseFail_右前门开+INACTIVE+车内有人")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112149?projectId=46')
    @pytest.mark.full
    def test_caseid_112149(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["Pass"])


    @allure.title("RKE解锁_UsageModeFail_DRIVING")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112135?projectId=46')
    @pytest.mark.sanity
    def test_caseid_112135(self):
        self.check_usage_mode_fail(usage=UsageMode.DRIVING,operation="unlock",seat_pres_sts=[])


    @allure.title("RKE闭锁_UsageModeFail_DRIVING")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359634?projectId=46')
    @pytest.mark.full
    def test_caseid_112161(self):
        self.check_usage_mode_fail(usage=UsageMode.DRIVING,operation="lock",seat_pres_sts=[])

    
    @allure.title("RKE联动关门_UsageModeFail_DRIVING")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112186?projectId=46')
    @pytest.mark.full
    def test_caseid_112186(self):
        self.check_usage_mode_fail(usage=UsageMode.DRIVING,operation="lock_close_door",seat_pres_sts=[])

    
    @allure.title("RKE解锁_UsageModeFail_CONVENIENCE+PassSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111798?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111798(self):
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.check_usage_mode_fail(usage=UsageMode.CONVENIENCE,operation="unlock",seat_pres_sts=["Pass"])

    
    @allure.title("RKE解锁_UsageModeFail_CONVENIENCE+RowSecLeSeat_occupied")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111794?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111794(self):
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        self.check_usage_mode_fail(usage=UsageMode.CONVENIENCE,operation="unlock",seat_pres_sts=["RL"])

    @allure.title("验证联动关门时如果车内有人，先提示”关门请当心“之后等待【1】5秒之后才执行关门动作")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1359593?projectId=46')
    @pytest.mark.smoke
    def test_caseid_1987527(self):
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.RKE)
        sleep(3)
        self.bus_comm.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id2, 0x8)])
        self.io.set_door(Drvr=Door.open,Pass=Door.open,LeRe=Door.open,RiRe=Door.open)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_close_door_and_lock()
        self.soa.check_Play2_req(app='RKE',txt='关门请当心',param='{"isLoopPlay":False,"priority":1,"streamType":6,"zone":0}',timeout=10)
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_door_opener_cmd(2, 2)
        self.io.set_door(Drvr=Door.close,Pass=Door.close,LeRe=Door.close,RiRe=Door.close)
        self.bus_comm.set_door_opener_sts(pass_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.dk.ck_four_door_lock_cmd(2)
        self.bus_comm.set_4_door_lock_status(Locksts.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("联动关门_ResultOK_ABANDONED+车内有人 + 主驾占座")
    @pytest.mark.full
    def test_caseid_1987336(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id2, 0x8)])
        self.io.set_door(Drvr=Door.open,Pass=Door.open,LeRe=Door.open,RiRe=Door.open)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullOpend)
        self.bus_comm.dk.empty_dk_data_queue()

        self.bus_comm.dk.send_rke_close_door_and_lock()
        self.soa.check_Play2_req(app='RKE',txt='关门请当心',param='{"isLoopPlay":False,"priority":1,"streamType":6,"zone":0}',timeout=10)
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_door_opener_cmd(3, 2)
        self.io.set_door(Drvr=Door.close,Pass=Door.close,LeRe=Door.close,RiRe=Door.close)
        self.bus_comm.set_door_opener_sts(lere_opener=DoorOpenerSts.FullClsd)
        self.bus_comm.dk.ck_four_door_lock_cmd(2)
        self.bus_comm.set_4_door_lock_status(Locksts.Lockd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock,exp_trigsrc=LockTrigerSource.IntrSwt)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("闭锁_DelayFail_INACTIVE+车内有人")
    @pytest.mark.full
    def test_caseid_1987333(self):
        self.mix.set_common_precontion()
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("闭锁_DelayFail_Convenience+车内有人")
    @pytest.mark.full
    def test_caseid_1987332(self):
        self.mix.set_common_precontion()
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("闭锁_DelayFail_ABANDONED+车内有人")
    @pytest.mark.full
    def test_caseid_1987331(self):
        self.mix.set_common_precontion()
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("闭锁_DelayFail_Convenience+车内无人")
    @pytest.mark.full
    def test_caseid_1987330(self):
        self.mix.set_common_precontion()
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(3)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("解锁_DelayFail_Abandoned")
    @pytest.mark.full
    def test_caseid_1987329(self):
        self.mix.set_common_precontion()
        self.mix.ctrl_lock(lock_type=LockCmd.LockCompleteArm,ctrl_type=LockSource.NFC)
        sleep(1)
        self.bus_comm.dk.send_rke_unlock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_four_door_lock_cmd(1)
        self.bus_comm.set_4_door_lock_status(Locksts.Unlckd)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock,exp_trigsrc=LockTrigerSource.KeyRem)
        sleep(1)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("联动关门_DelayFail_Convenience+车内有人")
    @pytest.mark.full
    def test_caseid_1987328(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(3)
        self.io.set_door(Drvr=Door.open,Pass=Door.open,LeRe=Door.open,RiRe=Door.open)
        self.bus_comm.dk.send_rke_close_door_and_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.io.set_five_door_sts(sts=Door.close)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("联动关门_DelayFail_Convenience+车内无人")
    @pytest.mark.full
    def test_caseid_1987327(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(3)
        self.io.set_door(Drvr=Door.open,Pass=Door.open,LeRe=Door.open,RiRe=Door.open)
        self.bus_comm.dk.send_rke_close_door_and_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.io.set_five_door_sts(sts=Door.close)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("联动关门_DelayFail_Inactive+车内有人")
    @pytest.mark.full
    def test_caseid_1987325(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.io.set_door(Drvr=Door.open,Pass=Door.open,LeRe=Door.open,RiRe=Door.open)
        self.bus_comm.dk.send_rke_close_door_and_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.io.set_five_door_sts(sts=Door.close)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("联动关门_DelayFail_ABANDONED+车内有人")
    @pytest.mark.full
    def test_caseid_1987324(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(3)
        self.io.set_door(Drvr=Door.open,Pass=Door.open,LeRe=Door.open,RiRe=Door.open)
        self.bus_comm.dk.send_rke_close_door_and_lock()
        self.bus_comm.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
        self.io.set_five_door_sts(sts=Door.close)
        self.bus_comm.dk.ck_rke_resp(1, 0, "Success", exec_type=3)

    @allure.title("联动关门_DoorCloseFail_右前门开+Convenience+车内无人")
    @pytest.mark.full
    def test_caseid_1987323(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["Pass"])

    @allure.title("联动关门_DoorCloseFail_右后门开+Convenience+车内有人")
    @pytest.mark.full
    def test_caseid_1987322(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["RR"])

    @allure.title("联动关门_DoorCloseFail_尾门开+Convenience+车内无人")
    @pytest.mark.full
    def test_caseid_1987321(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["Tailgate"])

    @allure.title("联动关门_DoorCloseFail_左前门开+Convenience+车内有人")
    @pytest.mark.full
    def test_caseid_1987320(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["Drv"])

    @allure.title("联动关门_DoorCloseFail_左后门开+Convenience+车内无人")
    @pytest.mark.full
    def test_caseid_1987319(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["RL"])

    @allure.title("联动关门_DoorCloseFail_右前门开+Abandoned+车内有人")
    @pytest.mark.full
    def test_caseid_1987318(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["Pass"])

    @allure.title("联动关门_DoorCloseFail_右后门开+Abandoned+车内无人")
    @pytest.mark.full
    def test_caseid_1987317(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.CONVENIENCE,door_open_pos = ["RR"])

    @allure.title("联动关门_DoorCloseFail_尾门开+Abandoned+车内有人")
    @pytest.mark.full
    def test_caseid_1987316(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["Tailgate"])

    @allure.title("联动关门_DoorCloseFail_左前门开+Abandoned+车内无人")
    @pytest.mark.full
    def test_caseid_1987315(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["Drv"])

    @allure.title("联动关门_DoorCloseFail_左后门开+Abandoned+车内有人")
    @pytest.mark.full
    def test_caseid_1987314(self):
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        self.check_lock_any_door_open_fail(usage = UsageMode.INACTIVE,door_open_pos = ["RL"])