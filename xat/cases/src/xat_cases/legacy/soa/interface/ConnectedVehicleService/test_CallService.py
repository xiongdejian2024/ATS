"""
@File        : test_CallService.py
@Author      : jingjing.wang
@Time        : 2024/01/05 18:00 PM
@Description : Test s2s interface about bonnet function
"""
from random import randint
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.soa_partner.src.partner_const import *
from xat_cases.legacy.bgm.case_helper.diag_case_helper.DiagTestBase import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH

USAGE_MODE_MAP = {
    0: "ABANDONED",
    1: "INACTIVE",
    2: "CONVENIENCE",
    11: "ACTIVE",
    13: "DRIVING",
}

CAR_MODE_MAP = {
    0: "NORMAL",
    1: "TRANSPORT",
    2: "FACTORY",
    3: "CRASH",
    5: "DYNO",
}


@allure.feature("SOA服务接口")
@allure.story("互联服务/CallService")
@pytest.mark.tcam
class TestCallService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("CallService", "client"),("VehicleModeService", "client")])
        self.partner.method_default_timeout = 0.1
        sleep(5)
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        # 检查上位机上是否有其它未关闭的soa_partner进程在运行，如果有，则杀死进程

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkNotEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set_vehspd(0)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)

    def after_each_func(self, ecu):
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待5s让环境恢复")
            sleep(5)
        else:
            sleep(3)  # 避免防玩
        self.ipdu.resume_all_bus_send()
        sleep(1)
        self.partner.send_method_request(CALL_SERVICE_CLIENT, "SetECallMode",{"Cmd": 4,"Src":0})
        self.partner.send_method_request(CALL_SERVICE_CLIENT, "SendBCallCmd",{"Cmd": 3})
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)


    @allure.title("eCall通话控制/获取eCall状态/通知eCall状态_主动拨打6123挂断5")#ecall紧急通话
    @pytest.mark.smoke
    def test_caseid_1983643(self):
        self.partner.send_method_request(CALL_SERVICE_CLIENT, "SetECallMode",{"Cmd": 0,"Src":0})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CALL_SERVICE_CLIENT, "SetECallMode",{"Cmd": 1,"Src":0})
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyECallStatus",
                                       {"Sts":{"Type":1,"Status":6}},method_name="GetECallWorkSts",timeout=5)
        # sleep(7.5)#7.5s内属于倒计时等待确认中
        # self.partner.send_method_request(CALL_SERVICE_CLIENT, "SetECallMode",{"Cmd": 5,"Src":0})#可设置可不设置只要没有挂断就会直接进入正式通话中
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyECallStatus",
                                       {"Sts":{"Type":1,"Status":1}},method_name="GetECallWorkSts",timeout=10)
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyECallStatus",
                                       {"Sts":{"Type":1,"Status":2}},method_name="GetECallWorkSts",timeout=5)
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyECallStatus",
                                       {"Sts":{"Type":1,"Status":3}},method_name="GetECallWorkSts",timeout=5)
        self.partner.send_method_request(CALL_SERVICE_CLIENT, "SetECallMode",{"Cmd": 4,"Src":0})
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyECallStatus",
                                       {"Sts":{"Type":1,"Status":5}},method_name="GetECallWorkSts")

    @allure.title("eCall通话控制/获取eCall状态/通知eCall状态_主动拨打6不等待7.5s调用确认拨打挂断5")
    @pytest.mark.full
    def test_caseid_1983644(self):
        self.partner.send_method_request(CALL_SERVICE_CLIENT, "SetECallMode",{"Cmd": 0,"Src":0})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CALL_SERVICE_CLIENT, "SetECallMode",{"Cmd": 1,"Src":0})
        sleep(2.5)#7.5s内属于倒计时等待确认中
        self.partner.send_method_request(CALL_SERVICE_CLIENT, "SetECallMode",{"Cmd": 5,"Src":0})#可设置可不设置只要没有挂断就会直接进入正式通话中
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyECallStatus",
                                       {"Sts":{"Type":1,"Status":1}},method_name="GetECallWorkSts",timeout=10)
        self.partner.send_method_request(CALL_SERVICE_CLIENT, "SetECallMode",{"Cmd": 4,"Src":0})
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyECallStatus",
                                       {"Sts":{"Type":1,"Status":5}},method_name="GetECallWorkSts",timeout=5)

    @allure.title("eCall通话控制/获取eCall状态/通知eCall状态_被动拨打123挂断5")
    @pytest.mark.full
    def test_caseid_1984163(self):
        self.partner.send_method_request(CALL_SERVICE_CLIENT, "SetECallMode",{"Cmd": 0,"Src":0})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CALL_SERVICE_CLIENT, "SetECallMode",{"Cmd": 1,"Src":1})
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyECallStatus",
                                       {"Sts":{"Type":2,"Status":1}},method_name="GetECallWorkSts",timeout=5)
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyECallStatus",
                                       {"Sts":{"Type":2,"Status":2}},method_name="GetECallWorkSts",timeout=5)
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyECallStatus",
                                       {"Sts":{"Type":2,"Status":3}},method_name="GetECallWorkSts",timeout=5)
        self.partner.send_method_request(CALL_SERVICE_CLIENT, "SetECallMode",{"Cmd": 4,"Src":1})
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyECallStatus",
                                       {"Sts":{"Type":2,"Status":5}},method_name="GetECallWorkSts",timeout=5)
        
    @allure.title("eCall通话控制/获取eCall状态/通知eCall状态_被动呼叫carmode为crash123挂断5")
    @pytest.mark.sanity
    def test_caseid_1983646(self):
        self.sd_tester.change_usage_mode(2)
        self.sd_tester.change_car_mode(3)
        sleep(0.5)
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyECallStatus",
                                       {"Sts":{"Type":2,"Status":1}},method_name="GetECallWorkSts",timeout=5)
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyECallStatus",
                                       {"Sts":{"Type":2,"Status":2}},method_name="GetECallWorkSts",timeout=5)
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyECallStatus",
                                       {"Sts":{"Type":2,"Status":3}},method_name="GetECallWorkSts",timeout=5)
        self.partner.send_method_request(CALL_SERVICE_CLIENT, "SetECallMode",{"Cmd": 4,"Src":1})
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyECallStatus",
                                       {"Sts":{"Type":2,"Status":5}},method_name="GetECallWorkSts",timeout=5)

    @allure.title("BCall通话控制/获取BCall状态/通知BCall状态_开始拨打1正在拨号1正在响铃2挂断5")#bcall道路救援
    @pytest.mark.smoke
    def test_caseid_1984154(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.send_method_request(CALL_SERVICE_CLIENT, "SendBCallCmd",{"Cmd": 0})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(CALL_SERVICE_CLIENT, "SendBCallCmd",{"Cmd": 1})
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyBCallStatus",
                                       {"Sts":{"Status":1}},method_name="GetBCallWorkSts",timeout=5)
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyBCallStatus",
                                       {"Sts":{"Status":2}},method_name="GetBCallWorkSts",timeout=10)
        self.partner.send_method_request(CALL_SERVICE_CLIENT, "SendBCallCmd",{"Cmd": 3})
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyBCallStatus",
                                       {"Sts":{"Status":5}},method_name="GetBCallWorkSts",timeout=5)

    @allure.title("eCall通话控制/获取eCall状态/通知eCall状态_严重故障")
    @pytest.mark.full
    def test_caseid_1984168(self):
        TCAM_SSH().type_commands('cat /dev/smd8 & echo -en "at+cfun=0\\r\\n" > /dev/smd8',timeout=3)
        TCAM_SSH().type_commands("\x03")#ctrl c
        self.partner.ck_event_and_resp(CALL_SERVICE_CLIENT, "NotifyECallStatus",
                                       {"Sts":{"FunctionSts":2}},method_name="GetECallWorkSts")
        TCAM_SSH().type_commands('cat /dev/smd8 & echo -en "at+cfun=1\\r\\n" > /dev/smd8',timeout=3)
        TCAM_SSH().type_commands("\x03")#ctrl c
        sts = self.partner.ck_s2s_event(CALL_SERVICE_CLIENT, "NotifyECallStatus", {"Sts":{}})['Sts']["FunctionSts"]
        assert sts in [0,1]
        self.partner.send_request_and_ck_resp(CALL_SERVICE_CLIENT, "GetECallWorkSts", {},
                                              {"out": {"FunctionSts":sts}})