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
import threading 

PRECHECKTI = 1  # mcu接收再上行到mpu很慢，约1s左右

times_light = 0
times_horn = 0

@allure.feature("互联服务")
@allure.story("数字钥匙和账号/RKE/寻车控制")
class TestDigitalKeyRkeCarLocator(TestDigitalKeyBase):
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        times_light = 0
        times_horn = 0
        self.soa.hmi_set_car_location_req(req=CarLocalTraceReq.kLiReq)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=2)
        self.bus_comm.dk.empty_dk_data_queue()
        sleep(2)

    def after_each_func(self, ecu):
        sleep(5)
        super().after_each_func(ecu)

    def start_thread_check_lamp(self):
        global times_light
        times_light = self.bus_comm.ipdu.check_event(self.bus_comm.ipdu.bodyexposedcanfd.CemBodyExpoFr51,'ActvnOfIndcrIndcrOut', 0,3)

    def start_thread_check_horn(self):
        global times_horn
        times_horn = self.bus_comm.ipdu.check_event(self.bus_comm.ipdu.backbonefr.CemBackBoneFr18,'ActvOfHorn', 0,1)


    def check_car_location_sts(self,sts:CarLocalTraceReq,last_time:int = 1):
        global times_light,times_horn
        promt_info = f"---------------->检查总线寻车的状态是否为{sts.name},检测的持续时间为{last_time})"
        with allure.step(promt_info):
            logger.info(promt_info)

        thread_lamp = threading.Thread(target=self.start_thread_check_lamp, args=())
        thread_lamp.setDaemon(True)
        thread_horn = threading.Thread(target=self.start_thread_check_horn, args=())
        thread_horn.setDaemon(True)
        thread_lamp.start()
        thread_horn.start()
        sleep(6)
          
        if sts.name == "kLiReq":
            if times_light != 0 and times_horn ==0:
                logger.info("检测到有闪灯,没有鸣笛")
                assert True
            else:
                logger.info("没有检测到闪灯")
                assert False
        elif sts.name == "kHornLiReq":
            if times_light != 0 and times_horn !=0:
                logger.info("检测到有闪灯鸣笛")
                assert True
            else:
                logger.info("没有检测到闪灯和鸣笛")
                assert False



    @allure.title("寻车控制_ResultOK_INACTIVE+主驾占座_仅闪灯PvOnlyLight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111839?projectId=46')
    @pytest.mark.smoke
    @pytest.mark.v140only
    def test_caseid_111839(self):
        self.mix.set_common_precontion()
        self.io.driver_seat_present()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kLiReq)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.All,sts=PosnLampSts.On)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)

    
    @allure.title("寻车控制_ResultOK_INACTIVE+副驾占座_鸣笛闪灯PvHornLight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111842?projectId=46')
    @pytest.mark.smoke
    @pytest.mark.v140only
    def test_caseid_111842(self):
        self.mix.set_common_precontion()
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kHornLiReq)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)



    @allure.title("寻车控制_ResultOK_CONVENIENCE+所有座椅不占座_仅闪灯PvOnlyLight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111831?projectId=46')
    @pytest.mark.smoke
    @pytest.mark.v140only
    def test_caseid_111831(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kLiReq)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.All,sts=PosnLampSts.On)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)

    
    @allure.title("寻车控制_ResultOK_ACTIVE+所有座椅不占座_仅闪灯PvOnlyLight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111829?projectId=46')
    @pytest.mark.smoke
    @pytest.mark.v140only
    def test_caseid_111829(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kLiReq)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.All,sts=PosnLampSts.On)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)



    @allure.title("寻车控制_ResultOK_ACTIVE+所有座椅不占座_鸣笛闪灯PvHornLight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111853?projectId=46')
    @pytest.mark.smoke
    @pytest.mark.v140only
    def test_caseid_111853(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kHornLiReq)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)

    
    @allure.title("寻车控制_ReqPriorLowFail_INACTIVE+后左占座_原危险报警灯开启")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111854?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111854(self):
        self.mix.set_common_precontion()
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=2)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ReqPriorLowFail", exec_type=3)

    
    @allure.title("寻车控制_ResultOK_CONVENIENCE+所有座椅不占座_鸣笛闪灯PvHornLight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111852?projectId=46')
    @pytest.mark.sanity
    @pytest.mark.v140only
    def test_caseid_111852(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kHornLiReq)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)

    
    @allure.title("寻车控制_BUSY_寻车指令执行中_仅闪灯PvOnlyLight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111854?projectId=46')
    @pytest.mark.full
    def test_caseid_111851(self):
        self.mix.set_common_precontion()
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=2)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 1, "SysBusy", exec_type=3)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kStop,priority=2)

    
    @allure.title("寻车控制_UsageModeFail_CONVENIENCE+后左占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111850?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111850(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)

    @allure.title("寻车控制_ReqPriorLowFail_ABANDONED+后左占座_原危险报警灯开启")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111845?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111845(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=2)
        self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ReqPriorLowFail", exec_type=3)
    
    @allure.title("寻车控制_ResultFail_ABANDONED+左后占座_鸣笛闪灯PvHornLight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111844?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111844(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ResultFail", exec_type=3)

    @allure.title("寻车控制_ResultFaill_INACTIVE+左后占座_Carmode=FACTORY")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111849?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111849(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ResultFail", exec_type=3)

    @allure.title("寻车控制_UsageModeFail_CONVENIENCE+后右占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111840?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111840(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)

    @allure.title("寻车控制_ResultFail_ACTIVE+所有座椅不占座_Carmode=FACTORY")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111830?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111830(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        # self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ResultFail", exec_type=3)

    @allure.title("寻车控制_UsageModeFail_CONVENIENCE+后中占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111838?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111838(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.set_seats_present_sts(sec_mid=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)

    @allure.title("寻车控制_UsageModeFail_CONVENIENCE+副驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111836?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111836(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)

    @allure.title("寻车控制_ResultFail_INACTIVE+后中占座_Carmode=TRANSPORT")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111832?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111832(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.mix.set_seats_present_sts(sec_mid=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(9)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ResultFail", exec_type=3)

    @allure.title("寻车控制_ReqPriorLowFail_InActive+所有座椅不占座_原左转向灯开启")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111828?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111828(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=2)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ReqPriorLowFail", exec_type=3)

    @allure.title("寻车控制_ReqPriorLowFail_ACTIVE+所有座椅不占座_原右转向灯开启")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111833?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111833(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kLeft,priority=3)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ReqPriorLowFail", exec_type=3)

    @allure.title("寻车控制_UsageModeFail_ACTIVE+后右占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111827?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111827(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.mix.set_seats_present_sts(sec_right=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)

    
    @allure.title("寻车控制_UsageModeFail_ACTIVE+主驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111826?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111826(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)

    @allure.title("寻车控制_ReqFail_panicVehicle.op=0 PvUnknown")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111835?projectId=46')
    @pytest.mark.full
    def test_caseid_111835(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(0)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ReqFail", exec_type=3)
        
    
    @allure.title("寻车控制_ReqFail_panicVehicle.op=-1 PvClose")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111834?projectId=46')
    @pytest.mark.full
    def test_caseid_111834(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(-1)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ReqFail", exec_type=3)
        

    @allure.title("寻车控制_ResultFail_ABANDONED+后中占座_仅闪灯PvOnlyLight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111846?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111846(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.mix.set_seats_present_sts(sec_mid=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(9)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ResultFail", exec_type=3)

    
    @allure.title("寻车控制_UsageModeFail_CONVENIENCE+主驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111843?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111843(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)

    @allure.title("寻车控制_UsageModeFail_ACTIVE+副驾占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111825?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111825(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)

    @allure.title("寻车控制_UsageModeFail_ACTIVE+后左占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111841?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111841(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)

    @allure.title("寻车控制_UsageModeFail_ACTIVE+后中占座")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111847?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111847(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.mix.set_seats_present_sts(sec_mid=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)

    @allure.title("寻车控制_UsageModeFail_DRIVING_仅闪灯PvOnlyLight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111848?projectId=46')
    @pytest.mark.full
    def test_caseid_111848(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)

    @allure.title("寻车控制_UsageModeFail_DRIVING_鸣笛闪灯PvHornLight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111837?projectId=46')
    @pytest.mark.full
    def test_caseid_111837(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)

    @allure.title("寻车控制_Success_Abandoned+主驾占位_仅闪灯PvOnlyLight+P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987273?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987273(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.empty_dk_data_queue()
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kLiReq)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.All,sts=PosnLampSts.On)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)

    
    @allure.title("寻车控制_Success_Abandoned+所有座椅不占座_仅闪灯PvOnlyLight+P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987269?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987269(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.dk.empty_dk_data_queue()
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kLiReq)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.All,sts=PosnLampSts.On)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)

    
    @allure.title("寻车控制_Success_Abandoned+所有座椅不占座_闪灯鸣笛HornLight+P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987270?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987270(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.dk.empty_dk_data_queue()
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kHornLiReq)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)

    @allure.title("寻车控制_Success_CONVENIENCE+副驾占位_仅闪灯PvOnlyLight+P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987274?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987274(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(pass_seat=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kLiReq)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.All,sts=PosnLampSts.On)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)

    
    @allure.title("寻车控制_Success_CONVENIENCE+所有座椅不占座_仅闪灯PvOnlyLight+P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987267?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987267(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kLiReq)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.All,sts=PosnLampSts.On)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)

    
    @allure.title("寻车控制_Success_CONVENIENCE+所有座椅不占座_闪灯鸣笛HornLight+P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987271?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987271(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kHornLiReq)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)

    
    @allure.title("寻车控制_Success_Inactive+主驾占位_闪灯鸣笛HornLight+P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987275?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987275(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.mix.set_seats_present_sts(drv_seat=SeatPresSts.Pres)
        sleep(1)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kHornLiReq)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)

    
    @allure.title("寻车控制_Success_Inactive+所有座椅不占座_仅闪灯PvOnlyLight+P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987268?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987268(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kLiReq)
        self.bus_comm.set_turn_indcr_lamp_sts(pos=LampPos.All,sts=PosnLampSts.On)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)

    
    @allure.title("寻车控制_Success_Inactive+所有座椅不占座_闪灯鸣笛HornLight+P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987272?projectId=46')
    @pytest.mark.smoke
    
    def test_caseid_1987272(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kHornLiReq)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)

    
    @allure.title("寻车控制_UsageModeFail_Abandoned + HornLight + D挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987522?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987522(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)

    
    @allure.title("寻车控制_UsageModeFail_Abandoned + OnlyLight + R挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987520?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987520(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        sleep(1)
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)
    
    @allure.title("寻车控制_UsageModeFail_ACTIVE + HornLight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987252?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987252(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)
    
    @allure.title("寻车控制_UsageModeFail_ACTIVE + OnlyLight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987251?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987251(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)
    
    @allure.title("寻车控制_UsageModeFail_CONVENIENCE + HornLight + 非P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987253?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987253(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)
    
    @allure.title("寻车控制_UsageModeFail_CONVENIENCE + OnlyLight + 非P挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987254?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987254(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)
    
    @allure.title("寻车控制_UsageModeFail_Inactive + HornLight + R挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987521?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987521(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)

    @allure.title("寻车控制_UsageModeFail_Inactive + OnlyLight + D挡")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1987519?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987519(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        sleep(1)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "UsageModeFail", exec_type=3)


    @allure.title("寻车控制-HornLight_ReqPriorLowFail_Abandoned+P挡_原危险报警灯开启")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111854?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987256(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=2)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ReqPriorLowFail", exec_type=3)

    
    @allure.title("寻车控制-HornLight_ReqPriorLowFail_Convenience+P挡_原危险报警灯开启")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111854?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987257(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=2)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ReqPriorLowFail", exec_type=3)


    @allure.title("寻车控制-OnlyLight_ReqPriorLowFail_Abandoned+P挡_原危险报警灯开启")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111854?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987259(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=2)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ReqPriorLowFail", exec_type=3)

    
    @allure.title("寻车控制-OnlyLight_ReqPriorLowFail_Convenience+P挡_原危险报警灯开启")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111854?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987260(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=2)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ReqPriorLowFail", exec_type=3)

    
    @allure.title("寻车控制+HornLight_ReqPriorLowFail_INACTIVE+P挡_原危险报警灯开启")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111854?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987255(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=2)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ReqPriorLowFail", exec_type=3)
    
    @allure.title("寻车控制+OnlyLight_ReqPriorLowFail_INACTIVE+P挡_原危险报警灯开启")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111854?projectId=46')
    @pytest.mark.full
    
    def test_caseid_1987258(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=2)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ReqPriorLowFail", exec_type=3)

    
    @allure.title("寻车控制+HornLight _ResultFail_Abandoned+Carmode=FACTORY")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111854?projectId=46')
    @pytest.mark.full
    def test_caseid_1987264(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=2)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ResultFail", exec_type=3,timeout=10)

    @allure.title("寻车控制+HornLight_ResultFail_Convenience+Carmode=Dyno")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111854?projectId=46')
    @pytest.mark.full
    def test_caseid_1987265(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.DYNO)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=2)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ResultFail", exec_type=3,timeout=10)
    
    @allure.title("寻车控制+HornLight_ResultFail_Inactive+Carmode=Transport")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111854?projectId=46')
    @pytest.mark.full
    def test_caseid_1987266(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=2)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ResultFail", exec_type=3,timeout=10)

    
    @allure.title("寻车控制+OnlyLight _ResultFail_Abandoned+Carmode=FACTORY")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111854?projectId=46')
    @pytest.mark.full
    def test_caseid_1987261(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.FACTORY)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=2)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ResultFail", exec_type=3,timeout=10)

    @allure.title("寻车控制+OnlyLight_ResultFail_Convenience+Carmode=Dyno")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111854?projectId=46')
    @pytest.mark.full
    def test_caseid_1987262(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.DYNO)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=2)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ResultFail", exec_type=3,timeout=10)
    
    @allure.title("寻车控制+OnlyLight_ResultFail_Inactive+Carmode=Transport")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111854?projectId=46')
    @pytest.mark.full
    def test_caseid_1987263(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,car_mode=CarMode.TRANSPORT)
        self.soa.hmi_set_turn_lamp_mode_and_priority(mode=TurnLampMode.kHazard,priority=2)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(2)
        self.bus_comm.dk.ck_rke_resp(3, 1, "ResultFail", exec_type=3,timeout=10)

    @allure.title("掉电之后RKE寻车")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/112297?projectId=46')
    @pytest.mark.full
    def test_caseid_1987544(self):
        logger.info("------------------>复位BGM")
        self.io.io_reset_bgm()
        logger.info("------------------>复位BGM结束")
        sleep(15)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kHornLiReq)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)

    @allure.title("休眠之后RKE寻车")
    @pytest.mark.full
    def test_caseid_1987551(self):
        self.sd_tester.reset_bgm()#重启BGM代替休眠唤醒
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.dk.empty_dk_data_queue()
        self.bus_comm.dk.send_rke_car_locator(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        self.check_car_location_sts(sts=CarLocalTraceReq.kHornLiReq)
        self.bus_comm.dk.ck_rke_resp(3, 0, "StartOK", exec_type=2)
        self.bus_comm.dk.ck_rke_resp(3, 0, "Success", exec_type=3)

    # @allure.title("寻车控制_DelayFail_ABANDONED+后中占座_仅闪灯PvOnlyLight")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1488978?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1488978(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
    #     self.mix.set_seats_present_sts(sec_mid=SeatPresSts.Pres)
    #     sleep(2)
    #     self.bus_comm.dk.send_rke_car_locator(2)
    #     sleep(1)
    #     self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
    #     sleep(10)
    #     self.bus_comm.dk.ck_rke_resp(3, 1, "DelayFail", exec_type=3)


    # @allure.title("寻车控制_DelayFail_ABANDONED+左后占座_鸣笛闪灯PvHornLight")
    # @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1488980?projectId=46')
    # @pytest.mark.full
    # def test_caseid_1488980(self):
    #     self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED)
    #     self.mix.set_seats_present_sts(sec_left=SeatPresSts.Pres)
    #     sleep(2)
    #     self.bus_comm.dk.send_rke_car_locator(1)
    #     sleep(1)
    #     self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
    #     sleep(10)
    #     self.bus_comm.dk.ck_rke_resp(3, 1, "DelayFail", exec_type=3)

    
    
    @allure.title("寻车控制_DelayFail_CONVENIENCE+所有座椅不占座_Carmode=TRANSPORT")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/111855?projectId=46')
    @pytest.mark.full
    @pytest.mark.v140only
    def test_caseid_111855(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        sleep(2)
        self.bus_comm.dk.send_rke_car_locator(1)
        sleep(1)
        self.bus_comm.dk.ck_rke_resp(3, 0, "PreConditionOK", exec_type=2)
        sleep(10)
        self.bus_comm.dk.ck_rke_resp(3, 1, "DelayFail", exec_type=3)
