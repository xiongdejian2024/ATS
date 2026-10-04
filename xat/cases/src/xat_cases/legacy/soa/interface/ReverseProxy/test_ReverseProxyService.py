#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_ReverseProxyService.py
@Time         :2023/04/08 17:20:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import allure
import pytest
import random
from time import sleep
from random import randint
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.digital_key_s2s import DigitalKeyPartner
from xat_cases.legacy.soa.case_helper.gnss_server import *
from xat_cases.legacy.soa.case_helper.utils import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *

def calc_buma(num, length):
    """计算补码"""
    if num < 0:
        inverse_code = abs(int(num)) ^ ((1 << (length - 1)) - 1) + (
                1 << (length - 1)
        )
        num = inverse_code + 1  # 负数返回 补码
    return num

RKECTRL_SERVICE_SERVER = "RKECtrlService_server"

@allure.feature("SOA服务接口")
@allure.story("反向代理/ReverseProxyService")
@pytest.mark.zjb
class TestReverseProxyService(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = DigitalKeyPartner([
            RPAAPA_SERVICE_SERVER,
            AVP_SERVICE_SERVER,
            ACC_SERVICE_SERVER,
            INTERACTIVE_SERVICE_SERVER
        ])
        self.partner.register_callback(RPAAPA_SERVICE_SERVER, self.partner.on_GetAPAStatus)
        self.ipdu.send_pdu('chassiscan1', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)
        self.ipdu.send_pdu('chassiscan2', 0x527, [0x27, 0x40, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], cycle_time=1)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEKeyPrsntStsZone7', 'Validity_NotValid')
        self.partner.empty_all(0.5)
        self.dk.empty_dk_data_queue()

    def after_each_func(self, ecu):
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr01, 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1', 0)
        if ecu.get("testresult") != "Pass":
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER,
                                           "NotifyPASetResponse", {"paSetResponse": 2})
            sleep(1)
        super().after_each_func(ecu, start=False)

    @allure.title("通知AVP相关控制按键显示状态_parkOutFrontLeft")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702883?projectId=46')
    @pytest.mark.full
    def test_caseid_105071(self):
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutFrontLeft': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts1', i,
                            timeout=1)  # 0.2

    @allure.title("通知AVP相关控制按键显示状态_parkOutFrontRight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702864?projectId=46')
    @pytest.mark.full
    def test_caseid_105086(self):
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutFrontRight': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts2', i,
                            timeout=1)  # 0.2

    @allure.title("通知AVP相关控制按键显示状态_parkOutRearLeft")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702849?projectId=46')
    @pytest.mark.full
    def test_caseid_105097(self):
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutRearLeft': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts3', i,
                            timeout=1)  # 0.2

    @allure.title("通知AVP相关控制按键显示状态_parkOutRearRight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702867?projectId=46')
    @pytest.mark.full
    def test_caseid_105084(self):
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutRearRight': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts4', i,
                            timeout=1)  # 0.2

    @allure.title("通知AVP相关控制按键显示状态_parkOutLeftFront")
    @pytest.mark.smoke
    def test_caseid_105115(self):
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutLeftFront': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts5', i,
                            timeout=1)  # 0.2

    @allure.title("通知AVP相关控制按键显示状态_parkOutRightFront")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702871?projectId=46')
    @pytest.mark.full
    def test_caseid_105080(self):
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutRightFront': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts6', i,
                            timeout=1)  # 0.2

    @allure.title("通知AVP相关控制按键显示状态_parkOutFront")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702820?projectId=46')
    @pytest.mark.full
    def test_caseid_105120(self):
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutFront': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts7', i,
                            timeout=1)  # 0.2

    @allure.title("通知AVP相关控制按键显示状态_parkOutRear")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702881?projectId=46')
    @pytest.mark.full
    def test_caseid_105072(self):
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutRear': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts8', i,
                            timeout=1)  # 0.2

    @allure.title("通知AVP相关控制按键显示状态_RPAFront")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702854?projectId=46')
    @pytest.mark.full
    def test_caseid_105092(self):
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'RPAFront': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr09, 'BleCtrlRPABtnStsFrnt', i, timeout=1)  # 0.2

    @allure.title("通知AVP相关控制按键显示状态_RPARear")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702842?projectId=46')
    @pytest.mark.full
    def test_caseid_105103(self):
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'RPARear': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr09, 'BleCtrlRPABtnStsRear', i, timeout=1)  # 0.2

    @allure.title("通知AVP相关控制按键显示状态_RPALeftTurn")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702888?projectId=46')
    @pytest.mark.full
    def test_caseid_105067(self):
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'RPALeftTurn': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr09, 'BleCtrlRPABtnStsLftTurn', i, timeout=1)  # 0.2

    @allure.title("通知AVP相关控制按键显示状态_RPARightTurn")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702890?projectId=46')
    @pytest.mark.full
    def test_caseid_105066(self):
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'RPARightTurn': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr09, 'BleCtrlRPABtnStsRgtTurn', i, timeout=1)  # 0.2

    @allure.title("通知AVP相关控制按键显示状态_button1")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702848?projectId=46')
    @pytest.mark.full
    def test_caseid_105098(self):
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'button1': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'HavpModBtnSts1', i, timeout=1)  # 0.2

    @allure.title("通知AVP相关控制按键显示状态_button2")
    @pytest.mark.smoke
    def test_caseid_105085(self):
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'button2': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'HavpModBtnSts2', i, timeout=1)  # 0.2

    @allure.title("通知AVP相关控制按键显示状态_button3")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702877?projectId=46')
    @pytest.mark.full
    def test_caseid_105075(self):
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'button3': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'HavpModBtnSts3', i, timeout=1)  # 0.2

    @allure.title("通知AVP相关控制按键显示状态_button4")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702813?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105126(self):
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'button4': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'HavpModBtnSts4', i, timeout=1)  # 0.2

    @allure.title("通知AVP相关控制按键显示状态_所有参数随机设置")
    @pytest.mark.smoke
    def test_caseid_105117(self):
        map = {'parkOutFrontLeft': [self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts1'],
               'parkOutFrontRight': [self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts2'],
               'parkOutRearLeft': [self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts3'],
               'parkOutRearRight': [self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts4'],
               'parkOutLeftFront': [self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts5'],
               'parkOutRightFront': [self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts6'],
               'parkOutFront': [self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts7'],
               'parkOutRear': [self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts8'],
               'RPAFront': [self.ipdu.connectivitycanfd.VgmConnFr09, 'BleCtrlRPABtnStsFrnt'],
               'RPARear': [self.ipdu.connectivitycanfd.VgmConnFr09, 'BleCtrlRPABtnStsRear'],
               'RPALeftTurn': [self.ipdu.connectivitycanfd.VgmConnFr09, 'BleCtrlRPABtnStsLftTurn'],
               'RPARightTurn': [self.ipdu.connectivitycanfd.VgmConnFr09, 'BleCtrlRPABtnStsRgtTurn'],
               'button1': [self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'HavpModBtnSts1'],
               'button2': [self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'HavpModBtnSts2'],
               'button3': [self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'HavpModBtnSts3'],
               'button4': [self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'HavpModBtnSts4'],
               }
        for _ in range(20):
            info = {x: randint(0, 3) for x in map.keys()}
            logger.info(info)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus', {"buttonSts": info})
            for key, value in info.items():
                self.ipdu.check(map[key][0], map[key][1], value, timeout=1)  # 0.2

    @allure.title("通知倒计时信息")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702855?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105091(self):
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyCountdown", {"timerCount": 0})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'RemCntDwn', 0, timeout=1)  # 0.03
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyCountdown", {"timerCount": 0x3FF})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'RemCntDwn', 0x3FF, timeout=1)  # 0.03
        for _ in range(10):
            count = randint(0, 0xFFFF)
            logger.info(count)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyCountdown", {"timerCount": count})
            self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'RemCntDwn', count & 0x3FF, timeout=1)  # 0.03

    @allure.title("通知倒计时信息_参数相同也需要触发pdu下行")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702835?projectId=46')
    @pytest.mark.full
    def test_caseid_105107(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for i in range(2):
            self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyCountdown", {"timerCount": 0})
            time.sleep(0.2)
        time.sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('RemCntDwn', [0, 0])

    @allure.title("通知AVP路线规划轨迹_targetLotLocation.parkLotForm")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702824?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105116(self):
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyPlanningPathTrack",
                                       {"pathTrack": {"targetLotLocation": {"parkLotForm": 0}}})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr09, 'AvpTargetpkgtpe', 0, timeout=1)  # 0.2
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyPlanningPathTrack",
                                       {"pathTrack": {"targetLotLocation": {"parkLotForm": 1}}})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr09, 'AvpTargetpkgtpe', 1, timeout=1)  # 0.2
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyPlanningPathTrack",
                                       {"pathTrack": {"targetLotLocation": {"parkLotForm": 2}}})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr09, 'AvpTargetpkgtpe', 2, timeout=1)  # 0.2

    @allure.title("通知AVP路线规划轨迹_参数相同也需要触发pdu下行")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702891?projectId=46')
    @pytest.mark.full
    def test_caseid_105065(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for i in range(2):
            self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyPlanningPathTrack",
                                           {"pathTrack": {"targetLotLocation": {"parkLotForm": 0}}})
            time.sleep(0.2)
        time.sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("AvpTargetpkgtpe", [0, 0])

    @allure.title("远程设置RPA及APA的状态_MobDevAVPReq=0")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702859?projectId=46')
    @pytest.mark.full
    def test_caseid_105088(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
        self.partner.empty_all(1)
        self.dk.send_apa_cmd(0, "0102030405060708")
        sleep(1)
        assert self.partner.partner_infos[RPAAPA_SERVICE_SERVER].req_queue.empty(), "不应该发送请求"

        self.partner.stop_single_partner(RPAAPA_SERVICE_SERVER)
        sleep(5)
        self.partner.start_single_partner("RPAAPAService", "server")
        self.partner.register_callback(RPAAPA_SERVICE_SERVER, self.partner.on_GetAPAStatus)
        sleep(5)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
        self.partner.ck_no_req(RPAAPA_SERVICE_SERVER, "SetPARemoteStatus", timeout=3)

    @allure.title("远程设置RPA及APA的状态_MobDevAVPReq遍历1-15")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702892?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105064(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
        self.partner.empty_all(1)
        for req in range(1, 16):
            logger.info(req)
            self.dk.send_apa_cmd(req, "0102030405060708")
            self.partner.ck_s2s_req(RPAAPA_SERVICE_SERVER, "SetPARemoteStatus",
                                    {"paReq": req, "handleUid": 0x0102030405060708})
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER,
                                           "NotifyPASetResponse", {"paSetResponse": 2})
            sleep(1)
            self.dk.ck_vehicle_control_resp(0, function_id=0xB)

    @allure.title("远程设置RPA及APA的状态_BLEAccountInfo=0")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702844?projectId=46')
    @pytest.mark.full
    def test_caseid_105101(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
        self.partner.empty_all(1)
        self.dk.send_apa_cmd(1, "0000000000000000")
        sleep(1)
        assert self.partner.partner_infos[RPAAPA_SERVICE_SERVER].req_queue.empty() == 0, "不应该发送请求"

        self.partner.stop_single_partner(RPAAPA_SERVICE_SERVER)
        sleep(5)
        self.partner.start_single_partner("RPAAPAService", "server")
        self.partner.register_callback(RPAAPA_SERVICE_SERVER, self.partner.on_GetAPAStatus)
        sleep(5)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
        self.partner.ck_no_req(RPAAPA_SERVICE_SERVER, "SetPARemoteStatus", timeout=3)

    @allure.title("远程设置RPA及APA的状态_服务连接但未接收到NotifyPARemoteStatus_缓存不发送_条件满足后发送缓存")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702844?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1919295(self):
        self.partner.stop_single_partner(RPAAPA_SERVICE_SERVER)
        sleep(5)
        self.partner.start_single_partner("RPAAPAService", "server")
        self.partner.register_callback(RPAAPA_SERVICE_SERVER, self.partner.on_GetAPAStatus)
        sleep(5)
        self.dk.send_apa_cmd(1, "0102030405060708")
        self.partner.ck_no_req(RPAAPA_SERVICE_SERVER, "SetPARemoteStatus", timeout=3)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
        self.partner.ck_s2s_req(RPAAPA_SERVICE_SERVER, "SetPARemoteStatus",
                                {"paReq": 1, "handleUid": 0x0102030405060708})

        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
        self.partner.ck_no_req(RPAAPA_SERVICE_SERVER, "SetPARemoteStatus", timeout=1)  # 不会再次触发

        self.partner.stop_single_partner(RPAAPA_SERVICE_SERVER)
        sleep(5)
        self.partner.start_single_partner("RPAAPAService", "server")
        self.partner.register_callback(RPAAPA_SERVICE_SERVER, self.partner.on_GetAPAStatus)
        sleep(2)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
        self.partner.ck_no_req(RPAAPA_SERVICE_SERVER, "SetPARemoteStatus", timeout=3)  # 服务下线再上线不会再次触发
        # 不给响应，mcu会等待45s超时，不会响应下一次的指令
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPASetResponse", {"paSetResponse": 2})
        sleep(1)

    @allure.title(
        "远程设置RPA及APA的状态_服务连接但未接收到NotifyPARemoteStatus_缓存不发送_服务下线在上线满足条件后会继续发送")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702844?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1919296(self):
        self.partner.stop_single_partner(RPAAPA_SERVICE_SERVER)
        sleep(5)
        self.partner.start_single_partner("RPAAPAService", "server")
        self.partner.register_callback(RPAAPA_SERVICE_SERVER, self.partner.on_GetAPAStatus)
        sleep(5)
        self.dk.send_apa_cmd(1, "0102030405060708")
        self.partner.ck_no_req(RPAAPA_SERVICE_SERVER, "SetPARemoteStatus", timeout=3)

        self.partner.stop_single_partner(RPAAPA_SERVICE_SERVER)
        sleep(5)
        self.partner.start_single_partner("RPAAPAService", "server")
        self.partner.register_callback(RPAAPA_SERVICE_SERVER, self.partner.on_GetAPAStatus)
        sleep(2)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
        self.partner.ck_s2s_req(RPAAPA_SERVICE_SERVER, "SetPARemoteStatus",
                                {"paReq": 1, "handleUid": 0x0102030405060708})
        # 不给响应，mcu会等待45s超时，不会响应下一次的指令
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPASetResponse", {"paSetResponse": 2})
        sleep(1)

    @allure.title("通知远程RPA及APA设置状态的反馈_0_NO_RESPONSE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702814?projectId=46')
    @pytest.mark.full
    def test_caseid_105125(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPASetResponse", {"paSetResponse": 0})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'MobDevRPAReqResp', 0)
        time.sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("MobDevRPAReqResp", [0])

    @allure.title("通知远程RPA及APA设置状态的反馈_1_FAILURE")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702875?projectId=46')
    @pytest.mark.full
    def test_caseid_105077(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.send_apa_cmd(1, "0102030405060708")
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPASetResponse", {"paSetResponse": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'MobDevRPAReqResp', 1)
        self.dk.ck_vehicle_control_resp(7, function_id=0xB)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("MobDevRPAReqResp", [1])

    @allure.title("通知远程RPA及APA设置状态的反馈_2_SUCCESS")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702853?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105093(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.send_apa_cmd(1, "0102030405060708")
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPASetResponse", {"paSetResponse": 2})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02, 'MobDevRPAReqResp', 2)
        self.dk.ck_vehicle_control_resp(0, function_id=0xB)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("MobDevRPAReqResp", [2])

    @allure.title("通知远程APA_RPA状态_paStatus")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702876?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105076(self):
        for x in range(15):
            logger.info(x)
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, 'NotifyPARemoteStatus',
                                           {"paRemoteStatus": {'paStatus': x}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr21, 'MobDevRPASts', x, timeout=1)

    @allure.title("通知远程APA_RPA状态_lastHandleType")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702887?projectId=46')
    @pytest.mark.full
    def test_caseid_105068(self):
        for x in range(5):
            logger.info(x)
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, 'NotifyPARemoteStatus',
                                           {"paRemoteStatus": {'lastHandleType': x}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr34, 'PALstHndlTyp', x, timeout=1)  # 0.06

    @allure.title("通知远程APA_RPA状态_参数相同也需要触发pdu下行")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702893?projectId=46')
    @pytest.mark.full
    def test_caseid_105063(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for i in range(2):
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, 'NotifyPARemoteStatus',
                                           {"paRemoteStatus": {'lastHandleType': 0,
                                                               'paStatus': 0}})
            time.sleep(0.2)
        time.sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("PALstHndlTyp", [0, 0])
        self.bgm_eth_inter.ck_signal_values("MobDevRPASts", [0, 0])

    @allure.title("通知目标车位方向_derection")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702843?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105102(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyParkingLotDirection", {"derection": 0})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr03, 'RemPATarpkgDir', 0, timeout=1)  # 0.2
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyParkingLotDirection", {"derection": 1})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr03, 'RemPATarpkgDir', 1, timeout=1)  # 0.2
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyParkingLotDirection", {"derection": 2})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr03, 'RemPATarpkgDir', 2, timeout=1)  # 0.2

    @allure.title("通知目标车位方向_参数相同也需要触发pdu下行")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702852?projectId=46')
    @pytest.mark.full
    def test_caseid_105094(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for i in range(2):
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyParkingLotDirection", {"derection": 0})
            time.sleep(0.2)
        time.sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("RemPATarpkgDir", [0, 0])

    @allure.title("通知驾驶模式状态_参数遍历")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702869?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105082(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for data in range(16):
            logger.info(data)
            self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "DriveModeStatus",
                                           {"values": [{"id": "DriveMode", "data": str(data)}]})
            sleep(0.4)
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'DrvModSet_1_BgmChas2SignalIPdu01', data, timeout=1)
            self.ipdu.check(self.ipdu.adcanfd.BgmADCANFDFr02, 'DrvModSet', data, timeout=0.4)
        sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("DrvModSet", list(range(16)))
        self.bgm_eth_inter.ck_signal_values("DrvModReqETH", [2, 2, 2, 3, 2, 2, 2, 7, 2, 2, 2, 11, 2, 2, 2, 2])

    @allure.title("通知驾驶模式状态_参数相同也需要触发pdu下行")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702822?projectId=46')
    @pytest.mark.full
    def test_caseid_105118(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for i in range(2):
            self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "DriveModeStatus",
                                           {"values": [{"id": "DriveMode", "data": "0"}]})
            time.sleep(0.2)
        time.sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("DrvModSet", [0, 0])
        self.bgm_eth_inter.ck_signal_values("DrvModReqETH", [2, 2])

    @allure.title("通知驾驶模式状态_id异常")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702815?projectId=46')
    @pytest.mark.full
    def test_caseid_105124(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "DriveModeStatus",
                                       {"values": [{"id": "SceneMode", "data": "0"}]})
        time.sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("DrvModSet", [])
        self.bgm_eth_inter.ck_signal_values("DrvModReqETH", [])

    @allure.title("通知驾驶模式状态_data异常")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702817?projectId=46')
    @pytest.mark.full
    def test_caseid_105122(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "DriveModeStatus",
                                       {"values": [{"id": "SceneMode", "data": "16"}]})
        time.sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("DrvModSet", [])
        self.bgm_eth_inter.ck_signal_values("DrvModReqETH", [])

    @allure.title("通知场景模式状态")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702880?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105073(self):
        for data in range(14):
            logger.info(data)
            self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "SceneModeStatus",
                                           {"values": [{"id": "SceneMode", "data": str(data)}]})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr78, 'SceneModSeld', data, timeout=1)  # 0.05

    @allure.title("通知场景模式状态_参数相同也需要触发pdu下行")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702847?projectId=46')
    @pytest.mark.full
    def test_caseid_105099(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for i in range(2):
            self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "SceneModeStatus",
                                           {"values": [{"id": "SceneMode", "data": "0"}]})
            time.sleep(0.2)
        time.sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SceneModSeld", [0, 0])

    @allure.title("通知场景模式状态_id异常")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702840?projectId=46')
    @pytest.mark.full
    def test_caseid_105104(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "SceneModeStatus",
                                       {"values": [{"id": "DriveMode", "data": "0"}]})
        time.sleep(1)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SceneModSeld", [])

    @allure.title("通知场景模式状态_data异常")
    @pytest.mark.sanity
    def test_caseid_105106(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "SceneModeStatus",
                                       {"values": [{"id": "SceneMode", "data": "14"}]})
        time.sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SceneModSeld", [])

    @allure.title("通知APA事件类型提醒")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702831?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105110(self):
        for last_handle_type in range(4):
            logger.info(last_handle_type)
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                           {"reminder": {"lastHandleType": last_handle_type}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr34, 'PALstHndlTyp', last_handle_type, timeout=1)  # 0.06

    @allure.title("通知APA周期类型提醒")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702873?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105078(self):
        for last_handle_type in range(4):
            logger.info(last_handle_type)
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderCycle",
                                           {"reminder": {"lastHandleType": last_handle_type}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr34, 'PALstHndlTyp', last_handle_type, timeout=1)  # 0.06

    @allure.title("通知APA车外提醒")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1702870?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105081(self):
        for last_handle_type in range(4):
            logger.info(last_handle_type)
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                           {"reminder": {"lastHandleType": last_handle_type}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr34, 'PALstHndlTyp', last_handle_type, timeout=1)  # 0.06


@allure.feature("SOA服务接口")
@allure.story("反向代理/ReverseProxyService")
@pytest.mark.zjb
class TestReverseProxyGNSSService(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.nucapp.tcam_power_off()
        time.sleep(30)
        self.partner = GNSSServiceServer([
            ("GNSSService", "server", "GNSSService_HD"),
            REMOTECTRL_SERVICE_SERVER
        ])
        self.partner.register_callback("GNSSService_server_GNSSService_HD", self.partner.on_GetGNSSInformation)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.partner.stop_operators()
        self.nucapp.tcam_power_on()
        sleep(120)
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.partner.GNSSStatus = 1
        self.partner.empty_all()

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)
    
    @allure.title("通知远程授权启动状态_启动后未收到notify不触发下行pdu")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_105087(self):  # s2s重启后会注册event，且并要求历史数据，因为服务仍在线，所以会获取到历史数据，故该case放在最开始
        self.kill_bgm_process()
        sleep(3)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("TelmRemoteAuthStartSts", [])

    @allure.title("通知远程授权启动状态_状态值遍历")
    @pytest.mark.sanity
    def test_caseid_1985585(self):
        for sts in [0, 3, 1, 4, 2, 3, 5, 4]:
            self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts",
                                        {"info": {"sts": sts, "time": 0xFFFFFFFF}})
            signal_value = 1 if sts in [3, 4] else 0
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21, 'TelmRemoteAuthStartSts', signal_value, timeout=3) 

    @allure.title("通知远程授权启动状态_下行报文周期校验")
    @pytest.mark.smoke
    def test_caseid_1985586(self):
        dict={0:random.choice([0, 1, 2, 5]), 1:random.choice([3, 4])}
        for key, value in dict.items():
            self.bgm_eth_inter.start_bgm_tcpdump()
            sleep(2)            
            self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts",
                                            {"info": {"sts": value, "time": 0xFFFFFFFF}})
            sleep(5)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_ordered_array("TelmRemoteAuthStartSts", [key])
            self.bgm_eth_inter.ck_period_time("TelmRemoteAuthStartSts", 1)        

    @allure.title("PosnFromSatltCntr从0到7翻转为0")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720501?projectId=46')
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_104997(self):
        self.nucapp.bgm_power_off()
        sleep(5)
        self.nucapp.bgm_power_on()
        self.partner.empty_all()
        self.partner.wait_for_service_reconnect("GNSSService_server_GNSSService_HD")
        for i in range(15):
            # 服务连上后等了4s才请求GetGNSSInformation
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltCntr', i % 8, timeout=6)

    @allure.title("通知非融合GNSS信息_PosnFromSatltPosnAlti")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720476?projectId=46')
    @pytest.mark.full
    def test_caseid_105022(self):
        for ellipsoid in [-101.1, -100, -99.85, 0, 6000, 6000.1]:
            self.partner.ellipsoid = ellipsoid
            y = int((ellipsoid + 100) / 0.1) if -100 <= ellipsoid <= 6000 else 0
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltPosnAlti', y, timeout=2)

    @allure.title("通知非融合GNSS信息_PosnAltitude")
    @pytest.mark.smoke
    def test_caseid_1988963(self): # Venus-T
        for ellipsoid in [-101.1, -100, -99.85, 0, 6000, 6000.1]:
            self.partner.ellipsoid = ellipsoid
            y = int((ellipsoid + 100) / 0.1) if -100 <= ellipsoid <= 6000 else 0
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr05, 'PosnAltitude', y, timeout=2)
            
    @allure.title("通知非融合GNSS信息_PosnFromSatltPosnDir")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720497?projectId=46')
    @pytest.mark.full
    def test_caseid_105001(self):
        for heading in [-0.1, 0, 0.015, 100.01, 359.99, 359.995] + [random.uniform(0, 359.99) for _ in range(10)]:
            logger.info(heading)
            self.partner.heading = heading
            y = int(heading / 0.01) if 0 <= heading <= 359.99 else 0
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltPosnDir', y, timeout=2)

    @allure.title("通知非融合GNSS信息_PosnFromSatltPosnLat")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720484?projectId=46')
    @pytest.mark.full
    def test_caseid_105014(self):
        for latitude in [-90.1, -90, 1, 90, 90.1] + [random.uniform(-90, 90) for _ in range(10)]:
            logger.info(latitude)
            self.partner.latitude = latitude
            y = calc_buma(int(latitude / 2.77777777777778E-07), 30) if -90 <= latitude <= 90 else 90
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltPosnLat', y, timeout=2)

    @allure.title("通知非融合GNSS信息_PosnFromSatltPosnLgt")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720477?projectId=46')
    @pytest.mark.full
    def test_caseid_105021(self):
        for longitude in [-180.1, -180, 1, 180, 180.1] + [random.uniform(-180, 180) for _ in range(10)]:
            logger.info(longitude)
            self.partner.longitude = longitude
            y = calc_buma(int(longitude / 2.77777777777778E-07), 31) if -180 <= longitude <= 180 else 180
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltPosnLgt', y, timeout=2)

    @allure.title("通知非融合GNSS信息_PosnFromSatltPosnSpd")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720481?projectId=46')
    @pytest.mark.full
    def test_caseid_105017(self):
        self.partner.velocityOverGround, self.partner.downVelocity = 0, 100
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltPosnSpd', 100000, timeout=2)
        self.partner.velocityOverGround, self.partner.downVelocity = 0, 101
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltPosnSpd', 0, timeout=2)
        self.partner.velocityOverGround, self.partner.downVelocity = 100, 0
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltPosnSpd', 100000, timeout=2)
        self.partner.velocityOverGround, self.partner.downVelocity = 100, -1
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltPosnSpd', 0, timeout=2)
        self.partner.velocityOverGround, self.partner.downVelocity = 30, 40
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltPosnSpd', 50000, timeout=2)
        self.partner.velocityOverGround, self.partner.downVelocity = 44, 55.55
        self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltPosnSpd', 70864, timeout=2)

    @allure.title("通知非融合GNSS信息_PosnFromSatltPosnVHozl")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720491?projectId=46')
    @pytest.mark.full
    def test_caseid_105007(self):
        for velocityOverGround in [-0.1, 0, 1, 100, 100.1] + [random.uniform(0, 100) for _ in range(20)]:
            logger.info(velocityOverGround)
            self.partner.velocityOverGround = velocityOverGround
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltPosnVHozl',
                            int(velocityOverGround / 0.001) if 0 <= velocityOverGround <= 100 else 0,
                            timeout=2)

    @allure.title("通知非融合GNSS信息_PosnFromSatltPosnVVert")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720496?projectId=46')
    @pytest.mark.full
    def test_caseid_105002(self):
        for downVelocity in [-100.1, 1, 100, 100.1] + [random.uniform(-100, 100) for _ in range(10)]:
            logger.info(downVelocity)
            self.partner.downVelocity = downVelocity
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltPosnVVert',
                            calc_buma(int(downVelocity / 0.001), 18) if -100 <= downVelocity <= 100 else 0,
                            timeout=2)

    @allure.title("通知非融合GNSS信息_PosnFromSatltTiForMins")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720490?projectId=46')
    @pytest.mark.full
    def test_caseid_105008(self):
        for timestamp in [0, 0xFFFFFFFFFFFFFFFF] + [randint(0, 0xFFFFFFFFFFFFFFFF) for _ in range(20)]:
            logger.info(timestamp)
            self.partner.timestamp = timestamp
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltTiForMins',
                            int((int(timestamp / 1000000) / 60)) % 60,
                            timeout=2)

    @allure.title("通知非融合GNSS信息_PosnFromSatltTiForMsec")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720494?projectId=46')
    @pytest.mark.full
    def test_caseid_105004(self):
        for timestamp in [0, 0xFFFFFFFFFFFFFFFF] + [randint(0, 0xFFFFFFFFFFFFFFFF) for _ in range(20)]:
            logger.info(timestamp)
            self.partner.timestamp = timestamp
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltTiForMsec',
                            int(timestamp // 1000) % 1000,
                            timeout=2)

    @allure.title("通知非融合GNSS信息_PosnFromSatltTiForSec")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720492?projectId=46')
    @pytest.mark.full
    def test_caseid_105006(self):
        for timestamp in [0, 0xFFFFFFFFFFFFFFFF] + [randint(0, 0xFFFFFFFFFFFFFFFF) for _ in range(20)]:
            logger.info(timestamp)
            self.partner.timestamp = timestamp
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltTiForSec',
                            int(timestamp // 1000000) % 60,
                            timeout=2)

    @allure.title("通知非融合GNSS信息_PosnFromSatltUTCForDay")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720493?projectId=46')
    @pytest.mark.full
    def test_caseid_105005(self):
        for UTCDate in [0, 0xFFFFFFFF] + [randint(0, 0xFFFFFFFF) for _ in range(20)]:
            logger.info(UTCDate)
            self.partner.UTCDate = UTCDate
            day = int(UTCDate / 10000)
            if day > 31:
                day = 0
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltUTCForDay', day, timeout=2)

    @allure.title("通知非融合GNSS信息_PosnFromSatltUTCForHr")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720485?projectId=46')
    @pytest.mark.full
    def test_caseid_105013(self):
        for UTCTime in [0, 0xFFFFFFFFFFFFFFFF, 150000000, 160000000] + [randint(1, 23000000) for _ in range(20)]:
            logger.info(UTCTime)
            self.partner.UTCTime = UTCTime
            y = int(UTCTime / 10000000) + 8
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltUTCForHr', 0 if y > 23 else y,
                            timeout=2)

    @allure.title("通知非融合GNSS信息_PosnFromSatltUTCForMins")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720495?projectId=46')
    @pytest.mark.full
    def test_caseid_105003(self):
        for UTCTime in [0, 0xFFFFFFFFFFFFFFFF, 5900000, 6000000] + [randint(0, 0xFFFFFFFFFFFFFFFF) for _ in range(20)]:
            logger.info(UTCTime)
            self.partner.UTCTime = UTCTime
            y = int(UTCTime // 100000) % 100
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltUTCForMins', 0 if y > 59 else y,
                            timeout=2)

    @allure.title("通知非融合GNSS信息_PosnFromSatltUTCForMth")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720498?projectId=46')
    @pytest.mark.full
    def test_caseid_105000(self):
        for UTCDate in [0, 0xFFFFFFFF, 1200, 1300] + [randint(0, 0xFFFFFFFF) for _ in range(20)]:
            logger.info(UTCDate)
            self.partner.UTCDate = UTCDate
            y = int(UTCDate // 100) % 100
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltUTCForMth', 0 if y > 12 else y,
                            timeout=2)

    @allure.title("通知非融合GNSS信息_PosnFromSatltUTCForSec")
    @pytest.mark.smoke
    def test_caseid_105011(self):
        for UTCTime in [0, 0xFFFFFFFFFFFFFFFF, 59000, 60000] + [randint(0, 0xFFFFFFFFFFFFFFFF) for _ in range(20)]:
            logger.info(UTCTime)
            self.partner.UTCTime = UTCTime
            y = int(UTCTime // 1000) % 100
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltUTCForSec', 0 if y > 59 else y,
                            timeout=2)

    @allure.title("通知非融合GNSS信息_PosnFromSatltUTCForYr")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720486?projectId=46')
    @pytest.mark.full
    def test_caseid_105012(self):
        for UTCDate in [0, 0xFFFFFFFF] + [randint(0, 0xFFFFFFFF) for _ in range(20)]:
            logger.info(UTCDate)
            self.partner.UTCDate = UTCDate
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltUTCForYr', UTCDate % 100, timeout=2)

    @allure.title("通知非融合GNSS信息_PosnBriefPosnLat")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720489?projectId=46')
    @pytest.mark.full
    def test_caseid_105009(self):
        for latitude in [-90.1, -90, 1, 90, 90.1] + [random.uniform(-90, 90) for _ in range(10)]:
            logger.info(latitude)
            self.partner.latitude = latitude
            y = calc_buma(int(latitude / 2.77777777777778E-07), 30) if -90 <= latitude <= 90 else 90
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr09, 'PosnBriefPosnLat', y, timeout=2)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr44, 'PosnBriefPosnLat', y, timeout=2)

    @allure.title("通知非融合GNSS信息_PosnBriefPosnLgt")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720499?projectId=46')
    @pytest.mark.full
    def test_caseid_104999(self):
        for longitude in [-180.1, -180, 1, 180, 180.1] + [random.uniform(-180, 180) for _ in range(10)]:
            logger.info(longitude)
            self.partner.longitude = longitude
            y = calc_buma(int(longitude / 2.77777777777778E-07), 31) if -180 <= longitude <= 180 else 180
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr09, 'PosnBriefPosnLgt', y, timeout=2)
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr44, 'PosnBriefPosnLgt', y, timeout=2)

    @allure.title("通知非融合GNSS信息_GpsStatus")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720475?projectId=46')
    @pytest.mark.sanity
    def test_caseid_105023(self):
        for GNSSStatus in range(1, 9):
            self.partner.GNSSStatus = GNSSStatus
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, 'GpsStatus', 1, timeout=2)
            self.partner.GNSSStatus = 0
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, 'GpsStatus', 0, timeout=2)

    @allure.title("通知非融合GNSS信息_UTCTiFromEthDataValid")
    @pytest.mark.sanity
    def test_caseid_105018(self):
        for GNSSStatus in range(1, 9):
            self.partner.GNSSStatus = GNSSStatus
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, 'UTCTiFromEthDataValid', 1, timeout=2)
            self.partner.GNSSStatus = 0
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, 'UTCTiFromEthDataValid', 0, timeout=2)

    @allure.title("通知非融合GNSS信息_UTCTiFromEthDay")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720478?projectId=46')
    @pytest.mark.full
    def test_caseid_105020(self):
        for UTCDate in [0, 0xFFFFFFFF, 320000] + [randint(0, 320000) for _ in range(20)]:
            logger.info(UTCDate)
            self.partner.UTCDate = UTCDate
            day = int(UTCDate / 10000)
            if day > 31:
                day = 0
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, 'UTCTiFromEthDay', day, timeout=2)

    @allure.title("通知非融合GNSS信息_UTCTiFromEthHr1")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720482?projectId=46')
    @pytest.mark.full
    def test_caseid_105016(self):
        for UTCTime in [0, 0xFFFFFFFFFFFFFFFF, 150000000, 160000000] + [randint(1, 23000000) for _ in range(20)]:
            logger.info(UTCTime)
            self.partner.UTCTime = UTCTime
            y = int(UTCTime / 10000000) + 8
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, 'UTCTiFromEthHr1', 0 if y > 23 else y, timeout=3)

    @allure.title("通知非融合GNSS信息_UTCTiFromEthMins1")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720500?projectId=46')
    @pytest.mark.full
    def test_caseid_104998(self):
        for UTCTime in [0, 0xFFFFFFFFFFFFFFFF, 5900000, 6000000] + [randint(0, 0xFFFFFFFFFFFFFFFF) for _ in range(20)]:
            logger.info(UTCTime)
            self.partner.UTCTime = UTCTime
            #需向下取整
            y = int((UTCTime // 100000 * 100000) / 100000) % 100
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, 'UTCTiFromEthMins1', 0 if y > 59 else y, timeout=2)

    @allure.title("通知非融合GNSS信息_UTCTiFromEthMth1")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720479?projectId=46')
    @pytest.mark.full
    def test_caseid_105019(self):
        for UTCDate in [0, 0xFFFFFFFF, 1200, 1300] + [randint(0, 0xFFFFFFFF) for _ in range(20)]:
            logger.info(UTCDate)
            self.partner.UTCDate = UTCDate
            y = int(UTCDate / 100) % 100
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, 'UTCTiFromEthMth1', 0 if y > 12 else y, timeout=2)

    @allure.title("通知非融合GNSS信息_UTCTiFromEthSec1")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720488?projectId=46')
    @pytest.mark.full
    def test_caseid_105010(self):
        for UTCTime in [0, 0xFFFFFFFFFFFFFFFF, 59000, 60000] + [randint(0, 0xFFFFFFFFFFFFFFFF) for _ in range(20)]:
            logger.info(UTCTime)
            self.partner.UTCTime = UTCTime
            y = int(UTCTime // 1000) % 100
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, 'UTCTiFromEthSec1', 0 if y > 59 else y, timeout=2)

    @allure.title("通知非融合GNSS信息_UTCTiFromEthYr1")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1720483?projectId=46')
    @pytest.mark.full
    def test_caseid_105015(self):
        for UTCDate in [0, 0xFFFFFFFF] + [randint(0, 0xFFFFFFFF) for _ in range(20)]:
            logger.info(UTCDate)
            self.partner.UTCDate = UTCDate
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr15, 'UTCTiFromEthYr1', UTCDate % 100, timeout=2)

@allure.feature("SOA服务接口")
@allure.story("反向代理/ReverseProxyService")
@pytest.mark.lg11
class TestReverseBLECtrlService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu, enable_inter_service=True)
        for process_name in ["monitor_em2.sh", "em2", "rke", "service_monitor"]:
            res = command_send(
                device_name="BGM",
                cmd=f"ps -ef |grep app |grep {process_name} |grep -v grep",
                timeout=60,
            )[1]
            pid = res.split()[1]
            command_send(device_name="BGM", cmd=f"kill -9 {pid}")
        sleep(2)
        command_send(device_name="BGM", cmd='su - service_monitor -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/service_monitor  -c /data/app/etc/service_monitor.json &"', timeout=15)
        self.partner = S2sBaseClass([("RKECtrlService", "server")])
        self.partner.method_default_timeout = 0.1

        self.partner.wait_for_service_reconnect(RKECTRL_SERVICE_SERVER)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1) # MPU侧档位
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)  
        self.partner.empty_all(0.5)
        self.dk.empty_dk_data_queue()

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)
           
    def kill_process(self, progressName):
        for process_name in ["monitor_em2.sh", "em2", progressName]:
            res = command_send(
                device_name="BGM",
                cmd=f"ps -ef |grep app |grep {process_name} |grep -v grep",
                timeout=60,
            )[1]
            pid = res.split()[1]
            command_send(device_name="BGM", cmd=f"kill -9 {pid}")
        sleep(5)
        
    def rke_lock_data(self):
        #uuid是随机生成的，这里需要固定
        self.set_nopeople_incar()
        execid = "b3419551-e045-11ee-940d-67196dbea9c3".replace("-", "")
        # execid = str(uuid.uuid1()).replace("-", "")
        logger.info(f"execid={execid}")
        self.dk.send_rke_lock(exec_id=execid)
        real_cmd = RealtimeCmdReq()
        logger.info(f"real_cmd={real_cmd}")
        real_cmd.execId = execid
        real_cmd.vid = f'{1:032}'
        real_cmd.vehicleModel = 61
        real_cmd.cmdCode = 1
        real_cmd.timestamp = 1000000012345678
        cd = CmdDetail()
        logger.info(f"cd={cd}")
        lc = LockControl()
        lc.op = 2
        lc.keyId = f'{1:032}'
        lc.userId = ''
        cd.lock_control.MergeFrom(lc)
        real_cmd.cmdDetail.MergeFrom(cd)
        ble_payload = real_cmd.SerializeToString().hex()
        logger.info(f"ble_payload={ble_payload}")
        ck_data = DataTypeHanding.hexstr_to_inlist(f'21{1 + len(ble_payload) // 2:04X}{1:02X}{ble_payload}')
        logger.info(f"ck_data={ck_data}")
        return ck_data
         
    @allure.title("BLECtrlService_设置数字钥匙RKE的请求指令信息_透传")
    @pytest.mark.sanity
    def test_caseid_1984561(self):
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyServiceSts",
                                       {"state": False}) 
        ck_data = self.rke_lock_data()
        self.partner.ck_no_req(RKECTRL_SERVICE_SERVER, "SetDigitalKeyDataUp", timeout=3)
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyServiceSts",
                                       {"state": True}) 
        sleep(1)
        self.partner.ck_s2s_req(RKECTRL_SERVICE_SERVER, "SetDigitalKeyDataUp",
                                    {"data": ck_data})
        #保证第一次流程走完
        sleep(60)
        self.partner.empty_all(0.5)
        ck_data = self.rke_lock_data()
        sleep(3)
        self.partner.ck_s2s_req(RKECTRL_SERVICE_SERVER, "SetDigitalKeyDataUp",
                                    {"data": ck_data})
        
    @allure.title("BLECtrlService_下行数字钥匙处理数据能力状态_透传")
    @pytest.mark.smoke
    def test_caseid_1984560(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(2)
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyServiceSts",
                                              {"state": True})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21, "DKServiceSts", 1)
        sleep(1)
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyServiceSts",
                                              {"state": False}) 
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21, "DKServiceSts", 0)
        sleep(1)
        self.partner.send_event_notify(RKECTRL_SERVICE_SERVER, "DigitalKeyServiceSts",
                                              {"state": False}) 
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("DKServiceSts", [1,0,0])

def is_sublist(main_list, sublist):
    if len(main_list) < len(sublist):
        return False
    for i in range(len(main_list) - len(sublist) + 1):
        if main_list[i:i+len(sublist)] == sublist:
            return True
    return False
     
@allure.feature("SOA服务接口")
@allure.story("反向代理/ReverseProxyService")
@pytest.mark.lg
class TestReverseBLECtrlService2(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.dk.empty_dk_data_queue()

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)
        self.bgm_power_off_and_on(timeout=3)
        sleep(15)
        
    def kill_em2(self):
        for process_name in ["monitor_em2.sh", "em2"]:
            res = command_send(
                device_name="BGM",
                cmd=f"ps -ef |grep app |grep {process_name} |grep -v grep",
                timeout=60,
            )[1]
            pid = res.split()[1]
            command_send(device_name="BGM", cmd=f"kill -9 {pid}")
        sleep(5)
              
    @allure.title("BLECtrlService_下行数字钥匙处理数据能力状态_rke重启场景")
    @pytest.mark.sanity
    def test_caseid_1984559(self): 
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_bgm_process("rke")
        sleep(10)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("DKServiceSts", [1])
        
    @allure.title("BLECtrlService_下行数字钥匙处理数据能力状态_反向代理启动场景")
    @pytest.mark.smoke
    def test_caseid_1984558(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(2)
        self.kill_em2()
        self.kill_bgm_process("s2s_service")
        self.kill_bgm_process("rke")
        sleep(5)
        command_send(device_name="BGM", cmd='su - s2s_service -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/s2s_service"', timeout=5)
        sleep(5)
        command_send(device_name="BGM", cmd='su - rke -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/rke"', timeout=5) 
        sleep(10)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()  
        value = self.bgm_eth_inter.get_signal_values("DKServiceSts")
        if is_sublist(value,[0,1]) or is_sublist(value,[0]) or is_sublist(value,[1]):
            pass
        else:
            assert False