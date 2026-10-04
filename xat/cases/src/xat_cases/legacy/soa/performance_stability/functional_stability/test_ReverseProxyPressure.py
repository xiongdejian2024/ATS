import allure
import pytest
from time import sleep
from random import randint
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_cases.legacy.bgm.VehicleCloud.DigitalKey.case_helper.digital_key_s2s import DigitalKeyPartner
from xat_cases.legacy.soa.case_helper.gnss_server import *
from xat_cases.legacy.soa.case_helper.utils import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *

globalvar=0

@allure.feature("性能稳定性")
@allure.story("业务稳定性/事件注册压测/反向代理事件注册")
@pytest.mark.soa
class TestReverseProxyPressure(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.nucapp.tcam_power_off()
        time.sleep(30)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner_members = [
            RPAAPA_SERVICE_SERVER,
            AVP_SERVICE_SERVER,
            ACC_SERVICE_SERVER,
            INTERACTIVE_SERVICE_SERVER,
            ("GNSSService", "server", "GNSSService_HD"),
            REMOTECTRL_SERVICE_SERVER
        ]
        self.partner = GNSSServiceServer(self.partner_members)
        self.partner.register_callback("GNSSService_server_GNSSService_HD", self.partner.on_GetGNSSInformation)
        # self.partner.register_callback(RPAAPA_SERVICE_SERVER, self.partner.on_GetAPAStatus)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
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
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEKeyPrsntStsZone7', 'Validity_NotValid')
        self.partner.GNSSStatus = 1
        self.partner.empty_all(0.5)
        self.dk.empty_dk_data_queue()

    def after_each_func(self, ecu):
        if ecu.get("testresult") != "Pass":
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER,
                                           "NotifyPASetResponse", {"paSetResponse": 2})
            sleep(1)
        super().after_each_func(ecu, start=False)

    @allure.title("压测-客户端重启，服务端保持在线")
    @pytest.mark.repeat(50)  # 50次
    def test_caseid_1985850(self):
        self.restart_bgm_and_connect_service(AVP_SERVICE_SERVER)
        sleep(3)
        self.inner_test()

    @allure.title("压测-服务端重启，客户端保持在线")
    @pytest.mark.repeat(50)  # 50次
    def test_caseid_1985852(self):
        self.partner.stop_single_partner(AVP_SERVICE_SERVER)
        self.partner.empty_all(2)
        self.partner.start_single_partner("AVPService", "server")
        sleep(3)
        self.partner.wait_for_service_reconnect(AVP_SERVICE_SERVER)
        self.inner_test()
    
    @allure.title("压测-卡bgm启动后第一个服务连接制造服务端上下线")
    @pytest.mark.repeat(100)  # 100次
    def test_caseid_1985853(self):
        self.restart_bgm_and_connect_service(AVP_SERVICE_SERVER)
        self.partner.stop_single_partner(AVP_SERVICE_SERVER)
        self.partner.empty_all(1)
        self.partner.start_single_partner("AVPService", "server")
        self.partner.wait_for_service_reconnect(AVP_SERVICE_SERVER)
        self.partner.empty_all(3)
        self.inner_test()

    def inner_test(self):
        global globalvar
        globalvar+=1
        logger.info(f"打印全局变量当前值globalvar={globalvar}")
        # AVP相关控制按键显示状态
        for i in range(4):
            logger.info(i)
            self.partner.send_event_notify(AVP_SERVICE_SERVER, 'NotifyAVPButtonStatus',
                                           {"buttonSts": {'parkOutRearLeft': i, 'parkOutFrontLeft': i}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts3', i,
                            timeout=2)  # 0.2
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr30, 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts1', i,
                            timeout=2)  # 0.2
        # 通知倒计时信息
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyCountdown", {"timerCount": 0})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'RemCntDwn', 0, timeout=2)  # 0.03
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyCountdown", {"timerCount": 0x3FF})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr06, 'RemCntDwn', 0x3FF, timeout=2) 

        # 通知AVP路线规划轨迹
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyPlanningPathTrack",
                                       {"pathTrack": {"targetLotLocation": {"parkLotForm": 0}}})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr09, 'AvpTargetpkgtpe', 0, timeout=2)  # 0.2
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyPlanningPathTrack",
                                       {"pathTrack": {"targetLotLocation": {"parkLotForm": 1}}})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr09, 'AvpTargetpkgtpe', 1, timeout=2)  # 0.2

        # 远程设置RPA及APA的状态
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
        self.partner.empty_all(1)
        for req in range(1, 2):
            logger.info(req)
            self.dk.send_apa_cmd(req, "0102030405060708")
            self.partner.ck_s2s_req(RPAAPA_SERVICE_SERVER, "SetPARemoteStatus",
                                    {"paReq": req, "handleUid": 0x0102030405060708})
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER,
                                           "NotifyPASetResponse", {"paSetResponse": 2})
            sleep(1)
            self.dk.ck_vehicle_control_resp(0, function_id=0xB)

        # 知目标车位方向_derection
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyParkingLotDirection", {"derection": 0})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr03, 'RemPATarpkgDir', 0, timeout=2)  # 0.2
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyParkingLotDirection", {"derection": 1})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr03, 'RemPATarpkgDir', 1, timeout=2)  # 0.2
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyParkingLotDirection", {"derection": 2})
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr03, 'RemPATarpkgDir', 2, timeout=2)  # 0.2

        # 通知驾驶模式状态
        for data in range(3):
            logger.info(data)
            self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "DriveModeStatus",
                                           {"values": [{"id": "DriveMode", "data": str(data)}]})
            sleep(0.4)
            self.ipdu.check(self.ipdu.chassiscan2.BgmChas2Fr01, 'DrvModSet', data, timeout=21)
            self.ipdu.check(self.ipdu.adcanfd.BgmADCANFDFr02, 'DrvModSet', data, timeout=2)
            # self.ipdu.check(self.ipdu.backbonefr.IHUBackBoneFr03, 'DrvModReq', data, timeout=1)
        sleep(1)

        # 通知场景模式状态
        for data in range(3):
            logger.info(data)
            self.partner.send_event_notify(INTERACTIVE_SERVICE_SERVER, "SceneModeStatus",
                                           {"values": [{"id": "SceneMode", "data": str(data)}]})
            self.ipdu.check(self.ipdu.bodycan.CemBodyFr78, 'SceneModSeld', data, timeout=2)  # 0.05
        
        # 通知APA事件类型提醒
        for last_handle_type in range(3):
            logger.info(last_handle_type)
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                           {"reminder": {"lastHandleType": last_handle_type}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr34, 'PALstHndlTyp', last_handle_type, timeout=2)

        # 通知APA周期类型提醒
        for last_handle_type in range(3):
            logger.info(last_handle_type)
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderCycle",
                                           {"reminder": {"lastHandleType": last_handle_type}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr34, 'PALstHndlTyp', last_handle_type, timeout=2)  # 0.06
        
        # 通知APA车外提醒
        for last_handle_type in range(3):
            logger.info(last_handle_type)
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                           {"reminder": {"lastHandleType": last_handle_type}})
            self.ipdu.check(self.ipdu.connectivitycanfd.VgmConnFr34, 'PALstHndlTyp', last_handle_type, timeout=3)  # 0.06
        
        # 通知远程授权启动状态 globalvar为全局变量
        for sts in [0, 3]:
            self.partner.send_event_notify(REMOTECTRL_SERVICE_SERVER, "RemoteAuthStartModeSts",
                                        {"info": {"sts": sts, "time": globalvar}})
            signal_value = 1 if sts in [3, 4] else 0
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21, 'TelmRemoteAuthStartSts', signal_value, timeout=3) 

        # 通知非融合GNSS信息
        for ellipsoid in [-101.1, -100, ]:
            self.partner.ellipsoid = ellipsoid
            y = int((ellipsoid + 100) / 0.1) if -100 <= ellipsoid <= 6000 else 0
            self.ipdu.check(self.ipdu.backbonefr.VgmBackBoneFr02, 'PosnFromSatltPosnAlti', y, timeout=2)
