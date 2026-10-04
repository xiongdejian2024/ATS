#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_charge_pile_open_charge_lid.py
@Time         :2023/1/31 17:54:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.test_digital_key_baseclass import *

PRECHECKTI = 0.3


@allure.feature("互联服务")
@allure.story("数字钥匙和账号/RKE/APA五门全关控制")
class TestDigitalKeyApaCloseDoor(TestDigitalKey):
    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 0)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassAntiPnch', 0) 
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReAntiPnch', 0) 
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReAntiPnch', 0) 
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "RoadInclnQly", 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "RoadInclnRoadIncln", 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr13, "RollAgGlbQf", 1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr13, "RollAgGlbVal", 0)
        sleep(3)
        self.partner.send_event_notify("RPAAPAService_server", "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
        self.partner.empty_all()
    
    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    

    @allure.title("APA五门全关_Success_CONVENIENCE+无占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111879?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111879(self):
        self.set_usage_mode(0x2)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.dk.send_rke_apa_close_door()
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2, timeout=5)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_rke_resp(10, 0, "Success", exec_type=3, timeout=5)

    @allure.title("APA五门全关_Success_CONVENIENCE+后左占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111870?projectId=46')
    @pytest.mark.full
    def test_caseid_111870(self):
        self.set_usage_mode(0x2)
        self.ipdu.backbonefr_srsbackbonefr04_seatoccptatrowsecle_0_srsbackbonesignalipdu04_passseatsts1_occptlrg()
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.dk.send_rke_apa_close_door()
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_rke_resp(10, 0, "Success", exec_type=3, timeout=5)

    @allure.title("APA五门全关_Success_ACTIVE+无占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111888?projectId=46')
    @pytest.mark.full
    def test_caseid_111888(self):
        self.set_usage_mode(0xB)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.dk.send_rke_apa_close_door()
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_rke_resp(10, 0, "Success", exec_type=3, timeout=5)

    @allure.title("APA五门全关_Success_ACTIVE+后中占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111881?projectId=46')
    @pytest.mark.sanity
    def test_caseid_111881(self):
        self.set_usage_mode(0xB)
        self.ipdu.backbonefr_srsbackbonefr04_seatoccptatrowsecmid_0_srsbackbonesignalipdu04_passseatsts1_occptlrg()
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.dk.send_rke_apa_close_door()
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_rke_resp(10, 0, "Success", exec_type=3, timeout=5)

    @allure.title("APA五门全关_Success_INACTIVE+无占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111868?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111868(self):
        self.set_usage_mode(0x1)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.dk.send_rke_apa_close_door()
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_rke_resp(10, 0, "Success", exec_type=3, timeout=5)

    @allure.title("APA五门全关_Success_INACTIVE+后右占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111871?projectId=46')
    @pytest.mark.sanity
    def test_caseid_111871(self):
        self.set_usage_mode(0x1)
        self.dk.set_secri_seat_present()
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.dk.send_rke_apa_close_door()
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_rke_resp(10, 0, "Success", exec_type=3, timeout=5)

    @allure.title("APA五门全关_Success_ABANDONED+无占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111878?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111878(self):   # todo: 四门关门信号没发，内部开关禁用，要看下是不是触发relocking或是详细的内部开关禁用逻辑
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.dk.send_rke_apa_close_door()
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_rke_resp(10, 0, "Success", exec_type=3, timeout=5)

    @allure.title("APA五门全关_Success_ABANDONED+后排全占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111891?projectId=46')
    @pytest.mark.full
    def test_caseid_111891(self):
        self.dk.set_secle_seat_present()
        self.dk.set_secmid_seat_present()
        self.dk.set_secri_seat_present()
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.dk.send_rke_apa_close_door()
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_rke_resp(10, 0, "Success", exec_type=3, timeout=5)

    @allure.title("APA五门全关_Success_DRIVING+无占座+paStatus==PAUSING")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111886?projectId=46')
    @pytest.mark.full
    @pytest.mark.s2s_prebuild
    def test_caseid_111886(self):
        self.partner.send_event_notify("RPAAPAService_server", "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 4}})
        self.partner.update_apa_sts(4, 4)
        self.set_usage_mode(11)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_rke_resp(10, 0, "Success", exec_type=3, timeout=5)

    @allure.title("APA五门全关_Success_ACTIVE+无占座+paStatus==RELATED_SYSTEM_ERROR")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111890?projectId=46')
    @pytest.mark.full
    def test_caseid_111890(self):
        self.partner.update_apa_sts(8, 4)
        self.set_usage_mode(0xB)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)

        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_rke_resp(10, 0, "Success", exec_type=3, timeout=5)

    @allure.title("APA五门全关_Success_CONVENIENCE+无占座+paStatus==ACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111860?projectId=46')
    @pytest.mark.full
    def test_caseid_111860(self):
        self.partner.update_apa_sts(3, 4)
        self.set_usage_mode(0x2)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_rke_resp(10, 0, "Success", exec_type=3, timeout=5)

    @allure.title("APA五门全关_Success_Abandoned+无占座+paStatus==COMPLETED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111884?projectId=46')
    @pytest.mark.full
    def test_caseid_111884(self):
        self.partner.update_apa_sts(8, 4)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_rke_resp(10, 0, "Success", exec_type=3, timeout=5)

    @allure.title("APA五门全关_Success_Inactive+无占座+paStatus==TERMINATED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111866?projectId=46')
    @pytest.mark.full
    def test_caseid_111866(self):
        self.partner.update_apa_sts(5, 4)
        self.set_usage_mode(0x1)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_rke_resp(10, 0, "Success", exec_type=3, timeout=5)

    @allure.title("APA五门全关_Success_ACTIVE+无占座+paStatus==SYSTEM_ERROR")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111880?projectId=46')
    @pytest.mark.full
    def test_caseid_111880(self):
        self.partner.update_apa_sts(7, 4)
        self.set_usage_mode(0xB)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_rke_resp(10, 0, "Success", exec_type=3, timeout=5)

    @allure.title("APA五门全关_DrvrSeatOccupied_ABANDONED+主驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111861?projectId=46')
    @pytest.mark.full
    def test_caseid_111861(self):
        self.dk.set_drvr_seat_present()
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        sleep(1)
        self.dk.ck_rke_resp(10, 1, "DrvrSeatOccupied", exec_type=3)

    @allure.title("APA五门全关_DrvrSeatOccupied_CONVENIENCE+主驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111859?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111859(self):
        self.dk.set_drvr_seat_present()
        self.set_usage_mode(0x2)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        sleep(1)
        self.dk.ck_rke_resp(10, 1, "DrvrSeatOccupied", exec_type=3)

    @allure.title("APA五门全关_DrvrSeatOccupied_INACTIVE+主驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111887?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111887(self):
        self.dk.set_drvr_seat_present()
        self.set_usage_mode(0x1)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        sleep(1)
        self.dk.ck_rke_resp(10, 1, "DrvrSeatOccupied", exec_type=3)

    @allure.title("APA五门全关_DrvrSeatOccupied_ACTIVE+主驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111865?projectId=46')
    @pytest.mark.sanity
    def test_caseid_111865(self):
        self.dk.set_drvr_seat_present()
        self.set_usage_mode(0xB)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        sleep(1)
        self.dk.ck_rke_resp(10, 1, "DrvrSeatOccupied", exec_type=3)

    @allure.title("APA五门全关_DrvrSeatOccupied_ABANDONED+副驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111883?projectId=46')
    @pytest.mark.smoke
    def test_caseid_111883(self):
        self.ipdu.backbonefr_srsbackbonefr04_passseatsts_0_srsbackbonesignalipdu04_passseatsts1_occptlrg()
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        sleep(1)
        self.dk.ck_rke_resp(10, 1, "DrvrSeatOccupied", exec_type=3)

    @allure.title("APA五门全关_DrvrSeatOccupied_CONVENIENCE+副驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111873?projectId=46')
    @pytest.mark.full
    def test_caseid_111873(self):
        self.ipdu.backbonefr_srsbackbonefr04_passseatsts_0_srsbackbonesignalipdu04_passseatsts1_occptlrg()
        self.set_usage_mode(0x2)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        sleep(1)
        self.dk.ck_rke_resp(10, 1, "DrvrSeatOccupied", exec_type=3)

    @allure.title("APA五门全关_DrvrSeatOccupied_INACTIVE+副驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111889?projectId=46')
    @pytest.mark.full
    def test_caseid_111889(self):
        self.ipdu.backbonefr_srsbackbonefr04_passseatsts_0_srsbackbonesignalipdu04_passseatsts1_occptlrg()
        self.set_usage_mode(0x1)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        sleep(1)
        self.dk.ck_rke_resp(10, 1, "DrvrSeatOccupied", exec_type=3)

    @allure.title("APA五门全关_DrvrSeatOccupied_ACTIVE+副驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111877?projectId=46')
    @pytest.mark.full
    def test_caseid_111877(self):
        self.ipdu.backbonefr_srsbackbonefr04_passseatsts_0_srsbackbonesignalipdu04_passseatsts1_occptlrg()
        self.set_usage_mode(0xB)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        sleep(1)
        self.dk.ck_rke_resp(10, 1, "DrvrSeatOccupied", exec_type=3)

    @allure.title("APA五门全关_DrvrSeatOccupied_DRIVING+主驾占座+paStatus==ENABLE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111867?projectId=46')
    @pytest.mark.full
    def test_caseid_111867(self):
        self.dk.set_drvr_seat_present()
        self.set_usage_mode(0xD)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.partner.update_apa_sts(1, 4)
        sleep(1)
        self.dk.send_rke_apa_close_door()
        sleep(1)
        self.dk.ck_rke_resp(10, 1, "DrvrSeatOccupied", exec_type=3)

    @allure.title("APA五门全关_DrvrSeatOccupied_DRIVING+副驾占座+paStatus==ENABLE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111882?projectId=46')
    @pytest.mark.sanity
    def test_caseid_111882(self):
        self.ipdu.backbonefr_srsbackbonefr04_passseatsts_0_srsbackbonesignalipdu04_passseatsts1_occptlrg()
        self.set_usage_mode(0xD)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.partner.update_apa_sts(1, 4)
        sleep(1)
        self.dk.send_rke_apa_close_door()
        sleep(1)
        self.dk.ck_rke_resp(10, 1, "DrvrSeatOccupied", exec_type=3)

    @allure.title("APA五门全关_UsageModeFail_DRIVING+无占座+paStatus==SEARCHING")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111876?projectId=46')
    @pytest.mark.full
    def test_caseid_111876(self):
        self.set_usage_mode(0xD)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.partner.update_apa_sts(2, 4)
        sleep(1)
        self.dk.send_rke_apa_close_door()
        sleep(1)
        self.dk.ck_rke_resp(10, 1, "UsageModeFail", exec_type=3)

    @allure.title("APA五门全关_UsageModeFail_DRIVING+无占座+paStatus==ACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111863?projectId=46')
    @pytest.mark.full
    def test_caseid_111863(self):
        self.set_usage_mode(0xD)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.partner.update_apa_sts(3, 4)
        sleep(1)
        self.dk.send_rke_apa_close_door()
        self.dk.ck_rke_resp(10, 1, "UsageModeFail", exec_type=3)

    @allure.title("APA五门全关_UsageModeFail_DRIVING+无占座+paStatus==COMPLETED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111874?projectId=46')
    @pytest.mark.full
    def test_caseid_111874(self):
        self.set_usage_mode(0xD)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.partner.update_apa_sts(8, 4)
        sleep(1)
        self.dk.send_rke_apa_close_door()
        self.dk.ck_rke_resp(10, 1, "UsageModeFail", exec_type=3)

    @allure.title("APA五门全关_UsageModeFail_DRIVING+无占座+paStatus==TERMINATED")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111885?projectId=46')
    @pytest.mark.full
    def test_caseid_111885(self):
        self.set_usage_mode(0xD)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.partner.update_apa_sts(5, 4)
        sleep(1)
        self.dk.send_rke_apa_close_door()
        self.dk.ck_rke_resp(10, 1, "UsageModeFail", exec_type=3)

    @allure.title("APA五门全关_UsageModeFail_DRIVING+无占座+paStatus==SYSTEM_ERROR")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111864?projectId=46')
    @pytest.mark.full
    def test_caseid_111864(self):
        self.set_usage_mode(0xD)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.partner.update_apa_sts(7, 4)
        sleep(1)
        self.dk.send_rke_apa_close_door()
        self.dk.ck_rke_resp(10, 1, "UsageModeFail", exec_type=3)

    @allure.title("APA五门全关_DelayFail_CONVENIENCE+无占座_尾门未关闭")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111856?projectId=46')
    @pytest.mark.full
    def test_caseid_111856(self):
        self.set_usage_mode(0x2)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 5)
        sleep(8)
        self.dk.ck_rke_resp(10, 1, "DelayFail", exec_type=3, timeout=5)

    @allure.title("APA五门全关_DelayFail_ACTIVE+无占座_左前门未关闭")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111857?projectId=46')
    @pytest.mark.full
    def test_caseid_111857(self):
        self.set_usage_mode(0xB)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(5, 1, 1, 1, 1)
        sleep(8)
        self.dk.ck_rke_resp(10, 1, "DelayFail", exec_type=3, timeout=5)

    @allure.title("APA五门全关_DelayFail_INACTIVE+无占座_右前门未关闭")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111862?projectId=46')
    @pytest.mark.full
    def test_caseid_111862(self):
        self.set_usage_mode(0x1)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 5, 1, 1, 1)
        sleep(8)
        self.dk.ck_rke_resp(10, 1, "DelayFail", exec_type=3, timeout=5)

    @allure.title("APA五门全关_DelayFail_ABANDONED+无占座_左后门未关闭")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111875?projectId=46')
    @pytest.mark.full
    def test_caseid_111875(self):
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 5, 1, 1)
        sleep(8)
        self.dk.ck_rke_resp(10, 1, "DelayFail", exec_type=3, timeout=5)

    @allure.title("APA五门全关_DelayFail_DRIVING+无占座+paStatus==PAUSING_右后门未关闭")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111858?projectId=46')
    @pytest.mark.full
    def test_caseid_111858(self):
        self.partner.update_apa_sts(4, 4)
        self.set_usage_mode(11)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.set_door_opener_sts(1, 1, 1, 5, 1)
        sleep(8)
        self.dk.ck_rke_resp(10, 1, "DelayFail", exec_type=3, timeout=5)

    @allure.title("APA五门全关_BUSY_相同指令执行中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111869?projectId=46')
    @pytest.mark.full
    def test_caseid_111869(self):
        self.set_usage_mode(0x2)
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        sleep(1)
        self.dk.send_rke_apa_close_door(slot_index=1)
        self.dk.ck_door_opener_cmd(1, 2, 2, timeout=5)
        self.dk.ck_door_opener_cmd(2, 2, 2)
        self.dk.ck_door_opener_cmd(3, 2, 2)
        self.dk.ck_door_opener_cmd(4, 2, 2)
        self.dk.ck_door_opener_cmd(5, 2, 6)
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2, slot_index=1)
        self.dk.send_rke_apa_close_door(slot_index=2)
        sleep(1)
        self.dk.ck_rke_resp(10, 1, "SysBusy", exec_type=3, slot_index=2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.ck_rke_resp(10, 0, "Success", exec_type=3, timeout=5)

    @allure.title("APA五门全关_Success_原五门关闭_INACTIVE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111872?projectId=46')
    @pytest.mark.full
    def test_caseid_111872(self):
        self.set_usage_mode(0x1)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        sleep(1)
        self.dk.send_rke_apa_close_door()
        self.dk.ck_rke_resp(10, 0, "PreConditionOK", exec_type=2)
        self.dk.ck_rke_resp(10, 0, "Success", exec_type=3)

