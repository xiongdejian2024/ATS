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

@allure.feature("性能稳定性")
@allure.story("业务稳定性/事件注册压测/反向代理事件注册")
@pytest.mark.soa
class TestWTIAutodrivePressure(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("LCAService", "server"),
                                     ("WTIAutoDriveService", "client"),
                                     ("ANPWTIService", "server"),
                                     ("RPAAPAService", "server"),
                                     ("AVPService", "server"),
                                     ("BACUService", "server"),
                                     ("FCTAService", "server"),
                                     ("RCWService", "server"),
                                     ("AEBRService", "server"),
                                     ("RCTAService", "server"),
                                     ("DOWService", "server"),
                                     ("LKAService", "server"),
                                     ("TLAService", "server"),
                                     ("SensorSelfCleanService", "server"),
                                     ("ACUFaultInfoService", "server"),
                                     ("FrontBackupCamera", "server"),
                                     ("CMSFService", "server"),
                                     ("SASService", "server"),
                                     ("AutoHighBeamControlService", "server"),
                                     ("AEBService", "server"),
                                     ("FCWService", "server"),
                                     ("AutoGearShiftService", "server"),
                                     ("APIService", "server"),
                                     ("ANPMRCService", "server"),
                                     ("AutoTurnLampCtrlService", "server"),
                                     ("ACCService", "server"),
                                     ("ELKService", "server"),
                                     ])
        self.sd_tester.tester_present()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.AutoDriverStatus_response = False
        self.ANP_response = False

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.partner.empty_all()
        logger.info(f"case开始运行***************************************************")

    def after_each_func(self, ecu):
        logger.info(f"case结束运行***************************************************")
        super().after_each_func(ecu, start=False)
                
    @allure.title("压测-客户端重启，服务端保持在线")
    @pytest.mark.sanity
    @pytest.mark.v200
    @pytest.mark.repeat(50)  # 50次
    def test_caseid_1985973(self):
        self.restart_bgm_and_connect_service(WTIAUTODRIVE_SERVICE_CLIENT)
        sleep(3)
        self.inner_test()

    @allure.title("压测-服务端重启，客户端保持在线")
    @pytest.mark.v200
    @pytest.mark.sanity
    @pytest.mark.repeat(50)  # 50次
    def test_caseid_1985974(self):
        #只需停止一个服务，其他服务也会下线
        self.partner.stop_single_partner(AVP_SERVICE_SERVER)
        self.partner.empty_all(2)
        self.partner.start_single_partner("AVPService", "server")
        sleep(3)
        self.partner.wait_for_service_reconnect(AVP_SERVICE_SERVER)
        self.inner_test()
  
    @allure.title("压测-卡bgm启动后第一个服务连接制造服务端上下线")
    @pytest.mark.v200
    @pytest.mark.sanity
    @pytest.mark.repeat(50)  # 100次
    def test_caseid_1985975(self):
        self.restart_bgm_and_connect_service(AVP_SERVICE_SERVER)
        self.partner.stop_single_partner(AVP_SERVICE_SERVER)
        self.partner.empty_all(1)
        self.partner.start_single_partner("AVPService", "server")
        self.partner.wait_for_service_reconnect(AVP_SERVICE_SERVER)
        self.partner.empty_all(3)
        self.inner_test()

    def inner_test(self):
        #LCAService
        self.partner.empty_all()  # 压测过程中bgm重启，但是服务端的历史数据会在连接并注册后再次发给bgm，也就会触发event，需要先清除避免影响后面的case
        self.partner.send_event_notify(LCA_SERVICE_SERVER, "NotifyLCAStatus",
                                           {"lcaStatus": {"leftWarning": 0}})
        sleep(0.5)
        self.partner.send_event_notify(LCA_SERVICE_SERVER, "NotifyLCAStatus",
                                           {"lcaStatus": {"leftWarning": 3}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'LCA Left Warning', 'info': '1'}]})
        
        #ANPWTI_SERVICE
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPLaneChangeReminder",
                                           {"anpLaneChangeReminder": {"reminder": 0, "openSource": 0}})
        sleep(0.5)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPLaneChangeReminder",
                                           {"anpLaneChangeReminder": {"reminder": 3, "openSource": 2}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'ANP Lane Change Remind1', 'info': '3'}]})
        
        #RPAAPA_SERVICE
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderCycle",
                                           {"reminder": {"type": 0, "lastHandleType": 0}})
        sleep(0.5)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderCycle",
                                           {"reminder": {"type": 1, "lastHandleType": 4}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'APA Working Status Both', 'info': '1'}]})
             
        #AVP_SERVICE
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyAVPReminderCycle",
                                       {"avpReminder": {"type": 0, "source": 0}})
        sleep(0.5)
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyAVPReminderCycle",
                                       {"avpReminder": {"type": 6, "source": 1}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'HAVP Cycle Warn Both', 'info': '1'}]})
        
        #BACU_SERVICE and ACUFaultInfo
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyIMUStatus",
                                       {"imuStatus": {"isCalibrationed": False}})
        sleep(0.5)
        self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyBIMUStatus",
                                        {"status": {"isCalibrationed": True}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'AD IMU Cali Warning', 'info': '0'}]})
        
        # #RCW_SERVICE
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus",
                                       {"rcwStatus": {"warning": 0}})
        sleep(0.5)
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus",
                                       {"rcwStatus": {"warning": 3}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'RCW Warning', 'info': '1'}]})  
        
        # #AEBR_SERVICE
        self.partner.send_event_notify(AEBR_SERVICE_SERVER, "NotifyAEBRStatus",
                                       {"aebRStatus": {"activeSts": 0}})
        sleep(0.5)
        self.partner.send_event_notify(AEBR_SERVICE_SERVER, "NotifyAEBRStatus",
                                       {"aebRStatus": {"activeSts": 3}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'AEBR Warning', 'info': '3'}]})  
        
        # #RCTA_SERVICE
        self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
                                       {"rctaFunctionStatus": {"leftWarning": 0, "rightWarning": 0}})
        sleep(0.5)
        self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
                                       {"rctaFunctionStatus": {"leftWarning": 1, "rightWarning": 0}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'RCTA Warning', 'info': '1'}]})  
        
        # #DOW_SERVICE
        self.partner.send_event_notify(DOW_SERVICE_SERVER, "NotifyDOWStatus",
                                       {"dowStatus": {"leftWarning": 0}})
        sleep(0.5)
        self.partner.send_event_notify(DOW_SERVICE_SERVER, "NotifyDOWStatus",
                                       {"dowStatus": {"leftWarning": 3}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'DOW Left Warning', 'info': '1'}]})  
        # #LKA_SERVICE
        self.partner.send_event_notify(LKA_SERVICE_SERVER, "NotifyLKAFunctionStatus",
                                      {"lasFunctionStatus": {"activeSts": 0}})
        sleep(0.5)
        self.partner.send_event_notify(LKA_SERVICE_SERVER, "NotifyLKAFunctionStatus",
                                      {"lasFunctionStatus": {"activeSts": 1}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'LDW Left Warning', 'info': '1'}]}) 
        
        # #SensorSelfClean_SERVICE
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, 'NotifySensorSelfCleanUsageScenario',
                                           {"occludedScenes": 1})
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                           {"cameraCleanSts": {"narrowAngleCamera": {"isDirty": False}}})
        sleep(0.5)
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                           {"cameraCleanSts": {"narrowAngleCamera": {"isDirty": True}}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'Front View Camera Clean Failed Remind', 'info': '1'}]})
        
        #ACUFaultInfo_SERVICE        
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                       {"cameraSts": {"leftAVMCamera": {"isFault": False}}})
        sleep(0.5)
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                           {"cameraSts": {"leftAVMCamera": {"isFault": True}}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'Left AVM Camera Fault Warning', 'info': '1'}]}) 
        
        #FrontBackupCamera_SERVICE
        self.partner.send_event_notify(FrontBackupCamera_SERVICE_SERVER, 'NotifyFrontCameraSts',
                                           {"frontCameraPrm": {"isCalibrated": True}})
        sleep(0.5)
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                                   {"cameraSts": {"frontAVMCamera": {"isCalibrated": False}}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'Camera Not Calibrated Warning', 'info': '1'}]})
        
        #CMSF_SERVICE 
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, 'NotifyCMSFStatus',
                                           {"cmsfStatus": {"faultSts": 0}})
        sleep(0.5)
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus",
                                            {"cmsfStatus": {"faultSts": 2}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'FCW_AEB Failed Warning', 'info': '1'}]})
        
        #AEB_SERVICE
        self.partner.send_event_notify(AEB_SERVICE_SERVER, "NotifyAEBStatus",
                                       {"aebStatus": {"functionActiveSts": 0}})
        sleep(0.5)
        self.partner.send_event_notify(AEB_SERVICE_SERVER, "NotifyAEBStatus",
                                           {"aebStatus": {"functionActiveSts": 1}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'AEB Warning', 'info': '1'}]})
        
        # FCW_SERVICE
        self.partner.send_event_notify(FCW_SERVICE_SERVER, "NotifyFCWStatus",
                                       {"fcwStatus": {"warningSts": 0}})
        sleep(0.5)
        self.partner.send_event_notify(FCW_SERVICE_SERVER, "NotifyFCWStatus",
                                           {"fcwStatus": {"warningSts": 1}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'FCW Warning', 'info': '1'}]})
        
        # AutoGearShift_SERVICE
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                       {"autoGearShiftSts": {"driverReminder": 0}})
        sleep(0.5)
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                           {"autoGearShiftSts": {"driverReminder": 1}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'Auto Gear Remind', 'info': '1'}]})
        
        #ANPMRC_SERVICE    
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyANPDegraedFault",
                                            {"fault": 0})
        sleep(0.5)
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyANPDegraedFault",
                                            {"fault": 2})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                    {"list":[{'name': 'ANP Degraed Fault Remind', 'info': '2'}]})
        
        #ACC_SERVICE
        self.partner.send_event_notify(ACC_SERVICE_SERVER, "NotifyACCSpeed", {"accSpeed":{"enableAdjustSpeedReason": 0}})
        sleep(0.5)
        self.partner.send_event_notify(ACC_SERVICE_SERVER, "NotifyACCSpeed", {"accSpeed":{"enableAdjustSpeedReason": 6}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                    {"list":[{'name': 'ACC Speed Remind', 'info': '6'}]})
        
        