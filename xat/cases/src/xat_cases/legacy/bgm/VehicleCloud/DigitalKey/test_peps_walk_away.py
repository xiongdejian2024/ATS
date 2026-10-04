# -*- coding: utf-8 -*-
"""
@File        : test_rke.py
@Author      : jiabin.zhu@jiduatuo.com
@Time        : 2022/10/23 18:00 PM
@Description : description about this file
@Examples    : example of how to use it
"""
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass import *

handle_ti = 0.5  # todo: 当前车控指令的时间也满足不了，可能是寻钥匙引起的，而且上锁的时间还不确定


@allure.feature("互联服务")
@allure.story("数字钥匙和账号/PEPS/离车侧门尾门自动关闭落锁")
class TestDigitalKeyWalkAway(TestDigitalKey):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        logger.info("------------------>复位BGM")
        self.nucapp.bgm_power_off()
        time.sleep(2)
        self.nucapp.bgm_power_on()
        time.sleep(15)
        logger.info("------------------>复位BGM结束")
    
    def after_class(self, ecu):
        super().after_class(self, ecu)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门全开_关门闭锁失败_ACTIVE+主驾占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112304?projectId=46')
    @pytest.mark.full
    def test_caseid_112304(self):
        self.set_usage_mode(0xB)
        self.set_config_info(0, 3)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_drvr_seat_present()
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        time.sleep(2)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeave_OnWithDriverDoorClose_原LockUnlckd+右后门开_闭锁失败_ABANDONED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112302?projectId=46')
    @pytest.mark.full
    def test_caseid_112302(self):
        self.set_config_info(0, 2)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        time.sleep(2)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门关闭_闭锁成功_ABANDONED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112301?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112301(self):
        self.set_usage_mode(0)
        self.set_car_mode(0)
        self.dk.set_drvr_seat_notpresent()
        self.set_config_info(0, 3)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        time.sleep(5)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_four_door_lock_cmd(2)
        time.sleep(1)
        self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(3, 9)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门全开_关门闭锁成功_CONVENIENCE+未主驾占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112228?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112228(self):
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_notpresent()
        self.set_config_info(0, 3)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_door_sts([1, 1, 1, 1, 0])
        time.sleep(2)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(0.5)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        time.sleep(0.5)
        self.dk.ck_cenlock_sts(3, 9)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门全开_关门闭锁成功_CONVENIENCE+未主驾占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112300?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112300(self):
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_notpresent()
        self.set_config_info(0, 3)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_door_sts([1, 1, 1, 1, 0])
        time.sleep(2)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(0.5)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        time.sleep(0.5)
        self.dk.ck_cenlock_sts(3, 9)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+左后门开_关门闭锁成功_CONVENIENCE+未主驾占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112296?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112296(self):
        self.set_usage_mode(2)
        self.set_car_mode(0)
        self.dk.set_drvr_seat_notpresent()
        self.set_config_info(0, 3)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_door_sts([0, 0, 1, 0, 0])
        self.dk.set_door_opener_sts(1, 1, 5, 1, 1)
        time.sleep(2)
        self.dk.send_walk_away_lock_cmd()
        # self.dk.ck_door_opener_cmd(3, 2)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        time.sleep(1)
        # self.dk.ck_four_door_lock_cmd(2)
        # time.sleep(1)
        # self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(3, 9)

    @allure.title("AutoLockOnLeave_OnWithDriverDoorClose_原LockUnlckd+尾门开_关门闭锁失败_CONVENIENCE+主驾未占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112292?projectId=46')
    @pytest.mark.full
    def test_caseid_112292(self):
        self.set_config_info(0, 2)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_drvr_seat_present()
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        time.sleep(2)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_door_opener_cmd(5, 0)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeaveOff_原LockUnlckd+五门关闭_CONVENIENCE+主驾未占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112287?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112287(self):
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_notpresent()
        self.set_config_info(0, 0)
        self.dk.set_cenlock_sts(0x1)
        time.sleep(3)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(1)
        self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeave_OnWithDriverDoorClose_原LockUnlckd+五门关闭_闭锁成功_INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112286?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112286(self):
        self.set_usage_mode(0x1)
        self.dk.set_drvr_seat_notpresent()
        self.set_config_info(0, 2)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        time.sleep(1)
        self.dk.send_walk_away_lock_cmd()
        self.dk.ck_four_door_lock_cmd(2)
        time.sleep(1)
        self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(3, 9)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门关闭_闭锁失败_ccp#94=0x2")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112285?projectId=46')
    @pytest.mark.full
    def test_caseid_112285(self):
        self.set_config_info(0, 3)
        self.dk.set_cenlock_sts(0x1)
        self.write_ccp({94: 0x02, 98: 0x2, 10: 0x2})
        time.sleep(3)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeave_OnWithDriverDoorClose_原LockUnlckd+五门关闭_闭锁成功_ACTIVE+主驾未占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112284?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112284(self):
        self.dk.set_cenlock_sts(0x3)
        self.set_config_info(0, 2)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        self.set_usage_mode(0xB)
        time.sleep(3)
        self.dk.send_walk_away_lock_cmd()
        self.dk.ck_four_door_lock_cmd(2, 3)  # 执行闭锁时间不固定
        time.sleep(1)
        self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(3, 9)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门关闭_闭锁成功_ACTIVE+主驾未占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112281?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112281(self):
        self.set_usage_mode(0xB)
        self.set_config_info(0, 3)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        time.sleep(3)
        self.dk.send_walk_away_lock_cmd()
        self.dk.ck_four_door_lock_cmd(2)
        time.sleep(1)
        self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(3, 9)
        with allure.step("校验usage下切至inactive"):
            self.doip.information_check_dd0a()
            curr_mode = self.doip.return_udsdata_and_check_and_print_response_result("Send dd0a to get result")[3:][0]
            assert curr_mode == 0x1, f'切换Usage Mode至inactive失败, 当前为{curr_mode}'

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+右后门开_关门闭锁成功_ACTIVE+未主驾占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112272?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112272(self):
        self.set_usage_mode(0xB)
        self.set_config_info(0, 3)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        self.dk.set_door_opener_sts(1, 5, 1, 1, 1)
        time.sleep(13)
        self.dk.send_walk_away_lock_cmd()
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.ck_cenlock_sts(3, 9)


    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+副驾门开_关门闭锁成功_INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112269?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112269(self):
        self.set_usage_mode(0x1)
        self.set_config_info(0, 3)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        self.dk.set_door_opener_sts(1, 5, 1, 1, 1)
        time.sleep(13)
        self.dk.send_walk_away_lock_cmd()
        # self.dk.ck_door_opener_cmd(2, 2)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        # self.dk.ck_four_door_lock_cmd(2)
        # time.sleep(1)
        # self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(3, 9)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门关闭_闭锁失败_CarModSubtyp=Factory Driving")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112268?projectId=46')
    @pytest.mark.full  # todo   Factory Driving
    def test_caseid_112268(self):
        self.set_config_info(0, 3)
        self.dk.set_cenlock_sts(0x1)
        self.write_ccp({94: 0x01, 98: 0x2, 10: 0x2})
        self.set_car_mode(0x2)
        time.sleep(1)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门关闭_闭锁失败_DRIVING")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112267?projectId=46')
    @pytest.mark.full
    def test_caseid_112267(self):
        self.set_config_info(0, 3)
        self.dk.set_cenlock_sts(0x1)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.set_usage_mode(0xD)
        time.sleep(3)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门关闭_闭锁失败_CarModSubtyp=Transport Driving")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112266?projectId=46')
    @pytest.mark.full  # todo CarModSubtyp=Transport Driving
    def test_caseid_112266(self):
        self.set_config_info(0, 3)
        self.dk.set_cenlock_sts(0x1)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.set_car_mode(0x2)
        time.sleep(3)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门关闭_闭锁成功_INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112262?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112262(self):
        self.set_usage_mode(0x1)
        self.set_config_info(0, 3)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        time.sleep(3)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_cenlock_sts(3, 9)
        self.dk.ck_four_door_lock_cmd(2)
        time.sleep(1)
        self.dk.ck_four_door_lock_cmd(0)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门关闭_闭锁失败_CarModSubtyp=Factory Paused")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112260?projectId=46')
    @pytest.mark.full  # todo CarModSubtyp=Factory Paused
    def test_caseid_112260(self):
        self.set_config_info(0, 3)
        self.dk.set_cenlock_sts(0x1)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.set_car_mode(0x2)
        time.sleep(3)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_cenlock_sts(1)


    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门关闭_闭锁失败_CarMode=Factory")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112255?projectId=46')
    @pytest.mark.full
    def test_caseid_112255(self):
        self.set_config_info(0, 3)
        self.dk.set_cenlock_sts(0x1)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.set_car_mode(0x2)
        time.sleep(3)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门关闭_闭锁失败_CarMode=Transport")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112251?projectId=46')
    @pytest.mark.full
    def test_caseid_112251(self):
        self.set_config_info(0, 3)
        self.dk.set_cenlock_sts(0x1)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.set_car_mode(0x1)
        time.sleep(3)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_door_opener_cmd(5, 0)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门关闭_闭锁成功_ccp#10=0x1")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112242?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112242(self):
        self.set_config_info(0, 3)
        self.dk.set_cenlock_sts(0x1)
        time.sleep(1)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x1})
        time.sleep(3)
        self.dk.send_walk_away_lock_cmd()
        self.dk.ck_four_door_lock_cmd(2)
        time.sleep(1)
        self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(3, 9)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门关闭_闭锁失败_ccp#10=0x2+TrsmParkLockd！=0x1[ParkEngd]+EpbLampReq=[OFF]")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112241?projectId=46')
    @pytest.mark.full
    def test_caseid_112241(self):
        self.ipdu.backbonefr_bbmbackbonefr04_epblampreqsecepblampreq_epblampreqtype1_off()
        self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_undefd()
        self.set_config_info(0, 3)
        self.dk.set_cenlock_sts(0x1)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.set_car_mode(0x1)
        time.sleep(3)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门关闭_闭锁失败_ACTIVE+主驾占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112239?projectId=46')
    @pytest.mark.full
    def test_caseid_112239(self):
        self.set_config_info(0, 3)
        self.dk.set_cenlock_sts(0x1)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_present()
        time.sleep(2)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeave_OnWithDriverDoorClose_原LockUnlckd+副驾门开_闭锁失败_CONVENIENCE+主驾未占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112238?projectId=46')
    @pytest.mark.full
    def test_caseid_112238(self):
        self.set_usage_mode(0x2)
        self.set_config_info(0, 2)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_drvr_seat_notpresent()
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        time.sleep(2)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_door_opener_cmd(2, 0)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeave_OnWithDriverDoorClose_原LockUnlckd+左后门开_闭锁失败_INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112237?projectId=46')
    @pytest.mark.full
    def test_caseid_112237(self):
        self.set_usage_mode(0x1)
        self.set_config_info(0, 2)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_drvr_seat_notpresent()
        self.dk.set_door_sts([0, 0, 1, 0, 0])
        time.sleep(2)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_door_opener_cmd(3, 0)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeave_OnWithDriverDoorClose_原LockUnlckd+五门关闭_闭锁成功_CONVENIENCE+未主驾占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112234?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112234(self):
        with allure.step("设置CONVENIENCE，主驾未占座, 设置仅主驾车门为开情况下关门且落锁，配置ccp# 94=0x80, ccp#98=0x2, \
        配置ccp#10=0x2，FR报文48-0-4中TrsmParkLockd=0x1[ParkEngd]或者57-23-64中EpbLampReq=[On]"):
            self.set_usage_mode(2)
            self.set_car_mode(0)
            self.dk.set_drvr_seat_notpresent()
            self.set_config_info(0, 2)
            self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
            self.dk.set_cenlock_sts(0x1)
            time.sleep(4)
            self.dk.send_walk_away_lock_cmd()
            self.dk.ck_four_door_lock_cmd(2)
            time.sleep(1)
            self.dk.ck_four_door_lock_cmd(0)
            self.dk.ck_cenlock_sts(3, 9)
        with allure.step("校验usage下切至inactive"):
            self.doip.information_check_dd0a()
            curr_mode = self.doip.return_udsdata_and_check_and_print_response_result("Send dd0a to get result")[3:][0]
            assert curr_mode == 0x1, f'切换Usage Mode至inactive失败, 当前为{curr_mode}'

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门关闭_闭锁成功_CONVENIENCE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112231?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112231(self):
        self.set_usage_mode(0x2)
        self.set_config_info(0, 3)
        self.dk.set_cenlock_sts(0x1)
        time.sleep(4)
        self.dk.send_walk_away_lock_cmd()
        self.dk.ck_four_door_lock_cmd(2)
        time.sleep(1)
        self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(3, 9)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门关闭_闭锁失败_CONVENIENCE+主驾占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112226?projectId=46')
    @pytest.mark.full
    def test_caseid_112226(self):
        self.set_config_info(0, 3)
        self.dk.set_cenlock_sts(0x1)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_present()
        time.sleep(3)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+主驾门开_关门闭锁成功_ABANDONED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112217?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112217(self):
        self.dk.set_drvr_seat_notpresent()
        self.set_config_info(0, 3)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.dk.set_door_opener_sts(5, 1, 1, 1, 1)
        time.sleep(2)
        self.dk.send_walk_away_lock_cmd()
        # self.dk.ck_door_opener_cmd(1, 2)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        time.sleep(1)
        # self.dk.ck_four_door_lock_cmd(2)
        # time.sleep(1)
        # self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(3, 9)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+五门关闭_闭锁失败_ccp#94=0x1")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112215?projectId=46')
    @pytest.mark.full
    def test_caseid_112215(self):
        self.set_config_info(0, 3)
        self.dk.set_cenlock_sts(0x1)
        self.write_ccp({94: 0x01, 98: 0x2, 10: 0x2})
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_present()
        time.sleep(3)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeave_OnWithDriverDoorClose_原LockUnlckd+主驾门开_闭锁成功_ACTIVE+主驾未占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112209?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112209(self):
        self.dk.set_drvr_seat_notpresent()
        self.set_config_info(0, 3)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.dk.set_door_opener_sts(5, 1, 1, 1, 1)
        time.sleep(2)
        self.dk.send_walk_away_lock_cmd()
        # self.dk.ck_door_opener_cmd(1, 2)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        time.sleep(1)
        # self.dk.ck_four_door_lock_cmd(2)
        # time.sleep(1)
        # self.dk.ck_four_door_lock_cmd(0)
        self.dk.ck_cenlock_sts(3, 9)

            


    @allure.title("AutoLockOnLeaveOff_原LockUnlckd+尾门开_关门闭锁失败_CONVENIENCE+主驾未占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112206?projectId=46')
    @pytest.mark.full
    def test_caseid_112206(self):
        self.dk.set_drvr_seat_notpresent()
        self.set_config_info(0, 2)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        time.sleep(2)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_cenlock_sts(1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        time.sleep(3)
        self.dk.ck_cenlock_sts(1)

    @allure.title("AutoLockOnLeave_OnWithAllDoorClose_原LockUnlckd+尾门开_关门闭锁失败_CONVENIENCE+未主驾占位")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112205?projectId=46')
    @pytest.mark.smoke
    def test_caseid_112205(self):
        self.set_usage_mode(2)
        self.dk.set_drvr_seat_notpresent()
        self.set_config_info(0, 3)
        self.write_ccp({94: 0x80, 98: 0x2, 10: 0x2})
        self.dk.set_cenlock_sts(0x1)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        time.sleep(2)
        self.dk.send_walk_away_lock_cmd()
        time.sleep(handle_ti)
        self.dk.ck_cenlock_sts(1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        time.sleep(3)
        self.dk.ck_cenlock_sts(1)

