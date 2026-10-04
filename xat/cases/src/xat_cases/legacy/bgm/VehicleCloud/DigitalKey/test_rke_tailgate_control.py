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
import time

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ""))
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass import *


@allure.feature("互联服务")
@allure.story("数字钥匙和账号/RKE/尾门控制")
class TestDigitalKeyRkeTailgateConTrol(TestDigitalKey):
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

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.io.set_four_door_close()
        self.io.trunk_door_close()
        self.dk.empty_dk_data_queue()
        sleep(3)
        self.partner.empty_all()
    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)
    

    @allure.title("打开尾门_UsageModeFail_CONVENIENCE+主驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111906?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111906(self):
        self.set_usage_mode(0x2)
        self.dk.set_drvr_seat_present()
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)

    @allure.title("尾门翘起_UsageModeFail_CONVENIENCE+副驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111919?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111919(self):
        self.set_usage_mode(0x2)
        self.dk.set_pass_seat_present()
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)

    @allure.title("关闭尾门_UsageModeFail_CONVENIENCE+后左占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111894?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111894(self):
        self.set_usage_mode(0x2)
        self.dk.set_secle_seat_present()
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)

    @allure.title("打开尾门_UsageModeFail_CONVENIENCE+后中占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111922?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111922(self):
        self.set_usage_mode(0x2)
        self.dk.set_secmid_seat_present()
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)

    @allure.title("尾门翘起_UsageModeFail_CONVENIENCE+后右占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111905?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111905(self):
        self.set_usage_mode(0x2)
        self.dk.set_secri_seat_present()
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)

    @allure.title("关闭尾门_UsageModeFail_ACTIVE+主驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111914?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111914(self):
        self.set_usage_mode(0xB)
        self.dk.set_drvr_seat_present()
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)

    @allure.title("打开尾门_UsageModeFail_ACTIVE+副驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111901?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111901(self):
        self.set_usage_mode(0xB)
        self.dk.set_pass_seat_present()
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)

    @allure.title("尾门翘起_UsageModeFail_ACTIVE+后左占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111899?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111899(self):
        self.set_usage_mode(0xB)
        self.dk.set_secle_seat_present()
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)

    @allure.title("关闭尾门_UsageModeFail_ACTIVE+后中占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111909?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111909(self):
        self.set_usage_mode(0xB)
        self.dk.set_secmid_seat_present()
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)
        assert False

    @allure.title("打开尾门_UsageModeFail_ACTIVE+后右占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111908?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111908(self):
        self.set_usage_mode(0xB)
        self.dk.set_secri_seat_present()
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)

    @allure.title("打开尾门_UsageModeFail_DRIVING")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483927?projectId=46')
    @pytest.mark.full
    def test_caseid_111910(self):
        self.set_usage_mode(0xD)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)

    @allure.title("尾门翘起_UsageModeFail_DRIVING")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111902?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111902(self):
        self.set_usage_mode(0xD)
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)

    @allure.title("打开尾门_CtrlTimeout_ABANDONED+后左占座_Status=kOpening")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483908?projectId=46')
    @pytest.mark.full
    def test_caseid_111929(self):
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_secle_seat_present()
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(10)
        self.dk.ck_rke_resp(4, 1, "DelayFail", exec_type=3)

    @allure.title("打开尾门_DelayFail_Abandoned_Status=kHover")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483910?projectId=46')
    @pytest.mark.full
    def test_caseid_111927(self):
        self.set_usage_mode(0x0)
        self.set_gear_pos(Gear.Park)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 4)
        sleep(10)
        self.dk.ck_rke_resp(4, 1, "DelayFail", exec_type=3)

    @allure.title("打开尾门_DelayFail_Inactive_Status=kClosing")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483926?projectId=46')
    @pytest.mark.full
    def test_caseid_111911(self):
        self.set_usage_mode(0x1)
        self.set_gear_pos(Gear.Park)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(10)
        self.dk.ck_rke_resp(4, 1, "DelayFail", exec_type=3)

    @allure.title("尾门异常开启对应用例")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/19835336?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_1983533(self):
        self.set_usage_mode(0x1)
        self.set_gear_pos(Gear.Park)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(10)
        self.dk.ck_rke_resp(4, 1, "DelayFail", exec_type=3)

    @allure.title("打开尾门_DelayFail_Convenience_Status=kClosed")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111893?projectId=46')
    @pytest.mark.sanity
    def test_caseid_111893(self):
        self.set_usage_mode(0x2)
        self.set_gear_pos(Gear.Park)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        sleep(10)
        self.dk.ck_rke_resp(4, 1, "DelayFail", exec_type=3)
    

    @allure.title("关闭尾门_CtrlTimeout_CONVENIENCE_Status=kClosing")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483911?projectId=46')
    @pytest.mark.full
    def test_caseid_111926(self):
        self.set_usage_mode(0x2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(10)
        self.dk.ck_rke_resp(4, 1, "DelayFail", exec_type=3)

    @allure.title("关闭尾门_CtrlTimeout_CONVENIENCE_Status=kHover")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483945?projectId=46')
    @pytest.mark.full
    def test_caseid_111892(self):
        self.set_usage_mode(0x2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 7)
        sleep(10)
        self.dk.ck_rke_resp(4, 1, "DelayFail", exec_type=3)

    @allure.title("关闭尾门_CtrlTimeout_CONVENIENCE_Status=kOpened")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483914?projectId=46')
    @pytest.mark.full
    def test_caseid_111923(self):
        self.set_usage_mode(0x2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        sleep(10)
        self.dk.ck_rke_resp(4, 1, "DelayFail", exec_type=3)

    @allure.title("关闭尾门_CtrlTimeout_CONVENIENCE_Status= kOpening")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483934?projectId=46')
    @pytest.mark.full
    def test_caseid_111903(self):
        self.set_gear_pos(Gear.Park)
        self.set_usage_mode(0x2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(10)
        self.dk.ck_rke_resp(4, 1, "DelayFail", exec_type=3)


    @allure.title("打开尾门_ResultOK_ABANDONED+主驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483930?projectId=46')
    @pytest.mark.smoke
    @pytest.mark.s2s_prebuild
    def test_caseid_111907(self):
        # self.dk.set_cenlock_sts(1)
        self.set_usage_mode(0x0)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_drvr_seat_present()
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.set_four_door_unlock()
        self.dk.set_cenlock_sts(1)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(6)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)
    
    
    @allure.title("打开尾门_ResultOK_INACTIVE+副驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111900?projectId=46')
    @pytest.mark.sanity
    def test_caseid_111900(self):
        self.set_usage_mode(0x1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_pass_seat_present()
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(6)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)
    

    @allure.title("打开尾门_Success_CONVENIENCE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483912?projectId=46')
    @pytest.mark.smoke
    @pytest.mark.v140only
    def test_caseid_111925(self):
        self.set_usage_mode(0x2)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(3)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    @allure.title("打开尾门_UsageModeFail_ACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111921?projectId=46')
    @pytest.mark.sanity
    @pytest.mark.v140only
    def test_caseid_111921(self):
        self.set_usage_mode(0xB)
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)

    @allure.title("翘起尾门_ResultOK_ABANDONED_开度10%")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483921?projectId=46')
    @pytest.mark.full
    @pytest.mark.s2s_prebuild
    def test_caseid_111916(self):
        #for value in [4,8,10]:
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 4)
        self.io.trunk_door_open()
        self.dk.ck_tropen_pos_req_from_hmi(10)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)


    @allure.title("翘起尾门_CtrlTimeout_INACTIVE+后中占座_Status=kHover")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111904?projectId=46')
    @pytest.mark.full
    def test_caseid_111904(self):
        self.set_usage_mode(0x1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_secmid_seat_present()
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 8)
        self.io.trunk_door_open()
        self.dk.ck_tropen_pos_req_from_hmi(10)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)


    @allure.title("翘起尾门_ResultOK_INACTIVE_开度15%")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483920?projectId=46')
    @pytest.mark.sanity
    def test_caseid_111917(self):
        self.set_usage_mode(0x1)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 15)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        sleep(1)
        self.io.trunk_door_open()
        self.dk.ck_tropen_pos_req_from_hmi(15)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    @allure.title("翘起尾门_ResultOK_CONVENIENCE_开度20%")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111912?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111912(self):
        self.set_usage_mode(0x2)
        self.io.trunk_door_close()
        self.dk.set_drvr_seat_notpresent()
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 20)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.io.trunk_door_open()
        self.dk.ck_tropen_pos_req_from_hmi(20)
        sleep(6)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    @allure.title("翘起尾门_ResultOK_ACTIVE_开度10%")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111898?projectId=46')
    @pytest.mark.sanity
    @pytest.mark.v140only
    def test_caseid_111898(self):
        self.set_usage_mode(0xB)
        sleep(1)
        self.dk.send_rke_tailgate_control(2)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)

    @allure.title("关闭尾门_ResultOK_ABANDONED+主驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483924?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111913(self):
        self.set_usage_mode(0x0)
        self.dk.set_drvr_seat_present()
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(6)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    @allure.title("关闭尾门_ResultOK_INACTIVE+副驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111895?projectId=46')
    @pytest.mark.sanity
    def test_caseid_111895(self):
        self.set_usage_mode(0x1)
        self.dk.set_pass_seat_present()
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(6)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    @allure.title("RKE关尾门+RKE解锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/109784?projectId=46')
    @pytest.mark.smoke
    def test_caseid_109784(self):
        self.dk.set_cenlock_sts(3)
        self.set_usage_mode(0x1)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.send_rke_unlock(slot_index=2)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2, slot_index=2)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3, slot_index=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(3)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    @allure.title("RKE解锁+RKE开尾门")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/109750?projectId=46')
    @pytest.mark.smoke
    def test_caseid_109750(self):
        self.dk.set_cenlock_sts(3)
        self.set_usage_mode(0x1)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(3)
        self.dk.send_rke_tailgate_control(1)
        self.dk.send_rke_unlock(slot_index=2)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2, slot_index=2)
        self.dk.set_four_door_unlock()
        self.dk.ck_cenlock_sts(1)
        self.dk.ck_rke_resp(1, 0, "Success", exec_type=3, slot_index=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(3)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    @allure.title("关闭尾门_ResultOK_CONVENIENCE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111897?projectId=46')
    @pytest.mark.sanity
    @pytest.mark.v140only
    def test_caseid_111897(self):
        self.set_usage_mode(0x2)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(6)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)
	

    @allure.title("关闭尾门_UsageModeFail_ACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483913?projectId=46')
    @pytest.mark.sanity
    @pytest.mark.v140only
    def test_caseid_111924(self):
        self.set_usage_mode(0xB)
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)

    @allure.title("打开尾门_BUSY_ACTIVE_关闭尾门执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483909?projectId=46')
    @pytest.mark.full
    def test_caseid_111928(self):
        self.set_usage_mode(0x1)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1, slot_index=1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2, slot_index=1)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        sleep(1)
        self.dk.send_rke_tailgate_control(1, slot_index=2)
        self.dk.ck_rke_resp(4, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(3)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    @allure.title("翘起尾门_BUSY_ACTIVE_关闭尾门执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483907?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111930(self):
        self.set_usage_mode(0xB)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1, slot_index=1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2, slot_index=1)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10, slot_index=2)
        self.dk.ck_rke_resp(4, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(3)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    @allure.title("关闭尾门_BUSY_CONVENIENCE_打开尾门执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111896?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111896(self):
        self.set_usage_mode(0x2)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_rke_tailgate_control(1, slot_index=1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2, slot_index=1)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        sleep(0.1)
        sleep(1)
        self.dk.send_rke_tailgate_control(-1, slot_index=2)
        self.dk.ck_rke_resp(4, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(3)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    @allure.title("翘起尾门_BUSY_CONVENIENCE_打开尾门执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483922?projectId=46')
    @pytest.mark.full
    def test_caseid_111915(self):
        self.set_usage_mode(0x2)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_rke_tailgate_control(1, slot_index=1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2, slot_index=1)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10, slot_index=2)
        self.dk.ck_rke_resp(4, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(3)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    @allure.title("关闭尾门_BUSY_ABANDONED_翘起尾门执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483919?projectId=46')
    @pytest.mark.full
    def test_caseid_111918(self):
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10, slot_index=1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2, slot_index=1)
        sleep(1)
        self.dk.send_rke_tailgate_control(-1, slot_index=2)
        self.dk.ck_rke_resp(4, 1, "SysBusy", exec_type=3, slot_index=2)
        self.io.trunk_door_open()
        sleep(2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 4)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    @allure.title("打开尾门_BUSY_ABANDONED_翘起尾门执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483917?projectId=46')
    @pytest.mark.full
    def test_caseid_111920(self):
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10, slot_index=1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2, slot_index=1)
        sleep(1)
        self.dk.send_rke_tailgate_control(1, slot_index=2)
        self.dk.ck_rke_resp(4, 1, "SysBusy", exec_type=3, slot_index=2)
    


    # --------------------------------------------------New----------------------------------------------------------------
    @allure.title("关闭尾门_Success_ABANDONED+副驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483924?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987365(self):
        self.set_usage_mode(0x0)
        self.dk.set_pass_seat_present()
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(6)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)
    
    @allure.title("关闭尾门_Success_ABANDONED+左后占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483924?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987364(self):
        self.set_usage_mode(0x0)
        self.dk.set_secle_seat_present()
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(6)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)
    
    @allure.title("关闭尾门_Success_ABANDONED+车内无人")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483924?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987361(self):
        self.set_usage_mode(0x0)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(6)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)
    
    @allure.title("关闭尾门_Success_Convenience+车内无人")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483924?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987363(self):
        self.set_usage_mode(0x2)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(6)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    
    @allure.title("关闭尾门_Success_Inactive+车内无人")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483924?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987362(self):
        self.set_usage_mode(0x1)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(6)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    

    @allure.title("打开尾门_Success_Abandoned+主驾占座 +  FullOpend")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483916?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987368(self):
        self.set_usage_mode(0x0)
        self.dk.set_drvr_seat_present()
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(6)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    @allure.title("打开尾门_Success_Abandoned+车内无人 +  FullOpend")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483916?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987371(self):
        self.set_usage_mode(0)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(6)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)
    
    @allure.title("打开尾门_Success_Convenience+右后占座 + Hover")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483916?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_111907(self):
        self.set_usage_mode(0x2)
        self.io.trunk_door_close()
        self.dk.set_secri_seat_present()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(6)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 8)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)
    
    @allure.title("打开尾门_Success_Convenience+左后占座 + FullOpend")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483916?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987367(self):
        self.set_usage_mode(0x2)
        self.io.trunk_door_close()
        self.dk.set_secle_seat_present()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(6)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)
    
    @allure.title("打开尾门_Success_Convenience+车内无人 + Hover")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483916?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987370(self):
        self.set_usage_mode(0x2)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)

        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(6)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 4)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)
    
    @allure.title("打开尾门_Success_Inactive+副驾占座 + Hover")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483916?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987366(self):
        self.set_usage_mode(0x1)
        self.dk.set_pass_seat_present()
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(6)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 4)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)
    
    @allure.title("打开尾门_Success_Inactive+车内无人 + Hover")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483916?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987369(self):
        self.set_usage_mode(0x1)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(6)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 10)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    
    @allure.title("翘起尾门_Success_ABANDONED_开度10% +车内有人 + 主驾占座 + FullOpend")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483921?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987375(self):
        self.set_usage_mode(0x0)
        self.dk.set_drvr_seat_present()
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.io.trunk_door_open()
        self.dk.ck_tropen_pos_req_from_hmi(10)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    
    @allure.title("翘起尾门_Success_ABANDONED_开度10%+车内无人 + FullOpend")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483921?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987372(self):
        self.set_usage_mode(0x0)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.io.trunk_door_open()
        self.dk.ck_tropen_pos_req_from_hmi(10)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)
    
    @allure.title("翘起尾门_Success_ABANDONED_开度20% +车内有人 + 右后占座 + Hover")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483921?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987378(self):
        self.set_usage_mode(0x0)
        self.dk.set_secri_seat_present()
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 20)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 4)
        self.io.trunk_door_open()
        self.dk.ck_tropen_pos_req_from_hmi(20)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    
    @allure.title("翘起尾门_Success_Convenience_开度10% +车内有人 + 左后占座 + FullOpend")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483921?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987377(self):
        self.set_usage_mode(0x2)
        self.dk.set_secle_seat_present()
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.io.trunk_door_open()
        self.dk.ck_tropen_pos_req_from_hmi(10)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    
    @allure.title("翘起尾门_Success_Convenience_开度10%+车内无人 + FullOpend")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483921?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987374(self):
        self.set_usage_mode(0x2)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.io.trunk_door_open()
        self.dk.ck_tropen_pos_req_from_hmi(10)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)
    
    @allure.title("翘起尾门_Success_Inactive_开度20% +车内有人 + 副驾占座 + Hover")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483921?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987376(self):
        self.set_usage_mode(0x1)
        self.dk.set_pass_seat_present()
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 8)
        self.io.trunk_door_open()
        self.dk.ck_tropen_pos_req_from_hmi(10)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    @allure.title("翘起尾门_Success_Inactive_开度20%+车内无人 + Hover")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483921?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987373(self):
        self.set_usage_mode(0x1)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 10)
        self.io.trunk_door_open()
        self.dk.ck_tropen_pos_req_from_hmi(10)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    
    @allure.title("关闭尾门_UsageModeFail_Abandoned+D挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483931?projectId=46')
    @pytest.mark.full
    def test_caseid_1987537(self):
        self.set_usage_mode(0xB)
        self.set_gear_pos(gear=Gear.Drv)
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)
    
    @allure.title("关闭尾门_UsageModeFail_ACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483931?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987351(self):
        self.set_usage_mode(11)
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)
    
    @allure.title("关闭尾门_UsageModeFail_Convenience+挡位非P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483931?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987353(self):
        self.set_usage_mode(0x2)
        self.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)
    
    @allure.title("关闭尾门_UsageModeFail_Driving")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483931?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987352(self):
        self.set_usage_mode(13)
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)
    
    @allure.title("关闭尾门_UsageModeFail_Inactive+R挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483931?projectId=46')
    @pytest.mark.full
    def test_caseid_1987536(self):
        self.set_usage_mode(0x1)
        self.set_usage_mode(0xB)
        self.set_gear_pos(gear=Gear.Rvs)
        sleep(1)
        self.dk.send_rke_tailgate_control(-1)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)
    
    @allure.title("尾门翘起_UsageModeFail_Active")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483931?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987349(self):
        self.set_usage_mode(11)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=10)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)

    @allure.title("尾门翘起_UsageModeFail_Convenience+非P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987350?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987350(self):
        self.set_usage_mode(11)
        self.set_gear_pos(gear=Gear.Rvs)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=20)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)
    
    @allure.title("打开尾门_UsageModeFail_Abandoned+D挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483931?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987539(self):
        self.set_usage_mode(13)
        self.set_gear_pos(gear=Gear.Drv)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)
    
    @allure.title("打开尾门_UsageModeFail_Active")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483931?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987354(self):
        self.set_usage_mode(11)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)

    @allure.title("打开尾门_UsageModeFail_Convenience+非P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483931?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987355(self):
        self.set_usage_mode(0x2)
        self.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)
    
    @allure.title("打开尾门_UsageModeFail_active+R挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483931?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987538(self):
        self.set_usage_mode(11)
        self.set_gear_pos(gear=Gear.Rvs)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)
    
    @allure.title("翘起尾门_UsageModeFail_Driving+R挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483931?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987535(self):
        self.set_usage_mode(13)
        self.set_gear_pos(gear=Gear.Rvs)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=20)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)
    
    @allure.title("翘起尾门_UsageModeFail_Driving+D挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483931?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987534(self):
        self.set_usage_mode(13)
        self.set_gear_pos(gear=Gear.Drv)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=10)
        self.dk.ck_rke_resp(4, 1, "UsageModeFail", exec_type=3)
        sleep(5)


    @allure.title("关闭尾门_BUSY_ABANDONED_关闭尾门执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483941?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987348(self):
        self.set_usage_mode(0x0)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1, slot_index=1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2, slot_index=1)
        sleep(0.1)
        sleep(1)
        self.dk.send_rke_tailgate_control(-1, slot_index=2)
        self.dk.ck_rke_resp(4, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(3)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    
    @allure.title("关闭尾门_BUSY_ABANDONED_打开尾门执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483941?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987347(self):
        self.set_usage_mode(0x0)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_rke_tailgate_control(1, slot_index=1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2, slot_index=1)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        sleep(0.1)
        sleep(1)
        self.dk.send_rke_tailgate_control(-1, slot_index=2)
        self.dk.ck_rke_resp(4, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(3)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    
    @allure.title("打开尾门_BUSY_ABANDONED_关闭尾门执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483909?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987346(self):
        self.set_usage_mode(0x0)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1, slot_index=1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2, slot_index=1)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        sleep(1)
        self.dk.send_rke_tailgate_control(1, slot_index=2)
        self.dk.ck_rke_resp(4, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(3)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    
    @allure.title("打开尾门_BUSY_ABANDONED_打开尾门执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483917?projectId=46')
    @pytest.mark.full
    def test_caseid_1987345(self):
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_rke_tailgate_control(1, slot_index=1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2, slot_index=1)
        sleep(1)
        self.dk.send_rke_tailgate_control(1, slot_index=2)
        self.dk.ck_rke_resp(4, 1, "SysBusy", exec_type=3, slot_index=2)

    
    @allure.title("翘起尾门_BUSY_ABANDONED_关闭尾门执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483907?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987344(self):
        self.set_usage_mode(0x0)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        sleep(1)
        self.dk.send_rke_tailgate_control(-1, slot_index=1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2, slot_index=1)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10, slot_index=2)
        self.dk.ck_rke_resp(4, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 6)
        sleep(3)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    
    @allure.title("翘起尾门_BUSY_ABANDONED_翘起尾门执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483922?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987343(self):
        self.set_usage_mode(0x0)
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_rke_tailgate_control(1,10, slot_index=1)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2, slot_index=1)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        sleep(1)
        self.dk.send_rke_tailgate_control(1, 10, slot_index=2)
        self.dk.ck_rke_resp(4, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(3)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    
    @allure.title("打开尾门_DelayFail+Convenience+Status=kOpening")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483908?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987358(self):
        self.set_usage_mode(0x2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(10)
        self.dk.ck_rke_resp(4, 1, "DelayFail", exec_type=3)
    
    @allure.title("打开尾门_DelayFail_Inactive+Status=kOpening")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483908?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987357(self):
        self.set_usage_mode(0x1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(10)
        self.dk.ck_rke_resp(4, 1, "DelayFail", exec_type=3)
        
    
    @allure.title("翘起尾门_DelayFail_Abandoned+后中占座_Status=kHover")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483908?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987359(self):
        self.set_usage_mode(0x1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=10)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 4)
        sleep(10)
        self.dk.ck_rke_resp(4, 1, "DelayFail", exec_type=3)
    
    @allure.title("翘起尾门_DelayFail_Convenience+后中占座_Status=kHover")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483908?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987360(self):
        self.set_usage_mode(0x2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 8)
        sleep(10)
        self.dk.ck_rke_resp(4, 1, "DelayFail", exec_type=3)

    
    @allure.title("掉电之后RKE开关尾门")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1483916?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987543(self):
        logger.info("------------------>复位BGM")
        self.nucapp.bgm_power_off()
        time.sleep(2)
        self.nucapp.bgm_power_on()
        time.sleep(15)
        logger.info("------------------>复位BGM结束")

        self.set_usage_mode(0x0)
        self.dk.set_drvr_seat_present()
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(6)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)

    @allure.title("休眠之后RKE开关尾门")
    @pytest.mark.full
    def test_caseid_1987550(self):
        self.bgm_power_off_and_on(timeout=15)#重启BGM代替休眠唤醒
        self.set_usage_mode(0x0)
        self.dk.set_drvr_seat_present()
        self.io.trunk_door_close()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        sleep(1)
        self.dk.send_rke_tailgate_control(op=1,position=0)
        self.dk.ck_rke_resp(4, 0, "PreConditionOK", exec_type=2)
        # self.dk.ck_door_opener_cmd(5, 1, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 2)
        sleep(6)
        self.io.trunk_door_open()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        sleep(2)
        self.dk.ck_rke_resp(4, 0, "Success", exec_type=3)













































