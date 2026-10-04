#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :VehicleModeService.py
@Time         :2024/11/05 14:00
@Author       :jingjing.wang@jiduauto.com
@Description  :
"""
import pytest
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.nuc_app import partner_process_check
from xat_ecu.legacy.soa_partner.src.partner_const_dp2 import *
from xat_ecu.legacy.sdk.Internal_ETH.tools.mock_udp_tcp_server_dp2 import MockUdp, MockTcp
from xat_ecu.legacy.soa_partner.src.partner_const_dp2 import VEHICLE_MODE_SERVICE_CLIENT
from xat_ecu.legacy.sdk.Internal_ETH.tools.common_dp2 import TcpChannel, UdpChannel
from xat_ecu.api.interfaces.dp2.cd_service.soa import Soa
from xat_cases.dp2.cd_service.case_helper.test_sil_abc_base import *
from xat_ecu.legacy.common.logger import logger


class TestVehicleModeService(TestSILAbcBase):
    def before_class(self, ecu: EcuInfo):
        super().before_class(self, ecu)
        logger.info("before_class")
        self.ssh.service_sil_test_preparation()
        self.soa.update([VEHICLE_MODE_SERVICE_CLIENT])#
        self.mock.update_channel({
                                    UdpChannel.CCUMCUCD_Multicast: None,
                                    #  UdpChannel.LcuL_Multicast: None,
                                    #  UdpChannel.LcuR_Multicast: None,
                                    #  UdpChannel.CCUMCUAD_CCUSOCCD: None,
                                    #  UdpChannel.CCUMCUCD_CCUSOCCD: None,
                                    #  UdpChannel.LcuL_CCUSOCCD: None,
                                    #  UdpChannel.LcuR_CCUSOCCD: None,
                                     TcpChannel.CdMcuTCPServer_CdSocTCPClient1: None,
                                    #  TcpChannel.LcuLTCPServer_CdSocTCPClient3: None,
                                    #  TcpChannel.LcuRTCPServer_CdSocTCPClient4: None,
                                    #  TcpChannel.AdMcuTCPServer_CdSocTCPClient2: None,
                                     })

    def before_each_func(self, ecu: EcuInfo):
        super().before_each_func(ecu)
        self.mock.resume_send_all_cycle_pdu()
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": 0}})
        self.mock.empty()
        self.soa.soa_partner.empty_all(0.5)
        logger.info("before_each_func")
        

    def after_each_func(self, ecu: EcuInfo):
        self.mock.resume_send_all_cycle_pdu()
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu: EcuInfo):
        super().after_class(self, ecu)
        logger.info("after_class")

    @allure.title("SetCarModeCtrl_OK")
    @pytest.mark.somke
    def test_caseid_100002(self):
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": 1}})
        self.soa.soa_partner.empty_all(0.5)
        for carmode in range(3):
            self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": carmode}},{"out":0})
            sleep(0.2)
            
    @allure.title("SetCarModeCtrl_RequestOutOfRange不会下行_mode")
    @pytest.mark.sanity
    def test_caseid_100202(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": 4}},{"out":1})
        sleep(0.5)
        self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'SetCarModProxyReq',[0])
        
        
    @allure.title("SetCarModeCtrl_RequestOutOfRange_mode")
    @pytest.mark.full
    def test_caseid_100205(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": 4}},{"out":1})
        
    @allure.title("SetCarModeCtrl_打断_三帧mode间打断")
    @pytest.mark.sanity
    def test_caseid_100207(self):
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": 0}})
        sleep(0.2)
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": 1}})
        sleep(0.2)
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": 3}})
        sleep(2)
        self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'SetCarModProxyReq',[1, 1, 2, 2, 4, 4, 4])
        
    @allure.title("SetCarModeCtrl_打断_复位idle间打断")
    @pytest.mark.sanity
    def test_caseid_100206(self):
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": 2}})
        sleep(0.3)
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": 1}})
        sleep(1)
        self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'SetCarModProxyReq',[3, 3, 3, 2, 2, 2,])
        
    @allure.title("SetCarModeCtrl_打断_100ms内多次调用下发最新值")
    @pytest.mark.sanity
    def test_caseid_100203(self):
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": 2}})
        sleep(0.11)
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": 1}})
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": 0}})
        sleep(1)
        self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'SetCarModProxyReq',[3,1,1,1])
        
    @allure.title("SetCarModeCtrl_下行pdu校验")
    @pytest.mark.sanity
    def test_caseid_100208(self):
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": 1}})
        self.soa.soa_partner.empty_all(0.5)
        for carmode in range(4):
            logger.info({f'当前carmode为{carmode}'})
            self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": carmode}},{"out":0})
            sleep(1)
        a = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'SetCarModProxyReq')
        assert a == [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            # self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'SetCarModProxyReq',[carmode+1,carmode+1,carmode+1])
            
    @allure.title("SetCarModeCtrl_打断_RequestOutOfRange不会打断有效值")
    @pytest.mark.full
    def test_caseid_100204(self):
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": 1}})
        self.soa.soa_partner.empty_all(0.5)
        for carmode in range(3):
            self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": carmode}},{"out":0})
            sleep(1)
            
    @allure.title("SetStartInhibitCtrl_OK")
    @pytest.mark.smoke
    def test_caseid_100201(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": True}},{"out":0})
        self.soa.soa_partner.empty_all(2)
        for isInhibitReq in [False,True]:
            self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": isInhibitReq}},{"out":0})
            sleep(2)
            
    @allure.title("SetStartInhibitCtrl_超时释放")
    @pytest.mark.smoke
    def test_caseid_100200(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": True}},{"out":0})
        self.soa.soa_partner.empty_all(2)
        self.mock.empty()
        for isInhibitReq in [False,True]:
            logger.info({f'当前禁用模式为{isInhibitReq}'})
            self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl",{"startInhibitCtrlCmd":{"isInhibitReq": isInhibitReq}},{"out":0})
            sleep(2)
            self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'StrtInhbProxyReq',[0])
            
    @allure.title("SetStartInhibitCtrl_周期维持请求, 主动释放")
    @pytest.mark.sanity
    def test_caseid_100199(self):
        self.mock.empty()
        sleep(0.1)
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": True}})
        sleep(0.1)
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": False}})
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": True}})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": False}},{"out":9})
        sleep(0.4)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": False}},{"out":0})
        sleep(1.1)
        self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'StrtInhbProxyReq',[1, 1, 1, 1, 1, 1, 0,0,0,0,0,0,0,0,0,0])
        
    @allure.title("SetStartInhibitCtrl_周期维持请求, 主动释放")
    @pytest.mark.sanity
    def test_caseid_100198(self):
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": True}})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": False}},{"out":9})
        
    @allure.title("SetStartInhibitCtrl_周期维持请求, 超时释放")
    @pytest.mark.sanity
    def test_caseid_100197(self):#todo 1.true200ms内false未发送成功无errorcode
        self.mock.empty()
        sleep(0.1)
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": True}})
        sleep(0.1)
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": False}})
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": True}})
        sleep(1.1)
        self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'StrtInhbProxyReq',[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        
    @allure.title("SetStartInhibitCtrl_调用True计时器重置")
    @pytest.mark.sanity
    def test_caseid_100196(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": True}},{"out":0})
        sleep(0.3)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": True}},{"out":0})
        self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'StrtInhbProxyReq')
        
    @allure.title("SetStartInhibitCtrl_100ms多次调用接口响应最新值")
    @pytest.mark.full
    def test_caseid_100195(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": True}},{"out":0})
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": False}},{"out":9})
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": True}},{"out":0})
        self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'StrtInhbProxyReq')
        
    @allure.title("SetStartInhibitCtrl_200ms计时器")
    @pytest.mark.full
    def test_caseid_100194(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": True}},{"out":0})
        sleep(0.19)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": False}},{"out":9})
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": True}},{"out":0})
        sleep(0.21)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": False}},{"out":0})
        self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'StrtInhbProxyReq')
    
    @allure.title("SetStartInhibitCtrl_OK")
    @pytest.mark.smoke
    def test_caseid_100176(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": True}},{"out":0})
        sleep(0.19)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": False}},{"out":9})
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": True}},{"out":0})
        sleep(0.21)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetStartInhibitCtrl", {"startInhibitCtrlCmd":{"isInhibitReq": False}},{"out":0})
        result = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'StrtInhbProxyReq')
        assert result == [1]
        
    @allure.title("SetKeepUsageModeCtrl_OK")
    @pytest.mark.smoke
    def test_caseid_100181(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd":{"usageMode":1}},{"out":0})
        self.soa.soa_partner.empty_all(1)
        self.mock.empty()
        for keepUsageModeCmd in range(1,4):
            logger.info({f'当前保持为{keepUsageModeCmd}'})
            self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd": {"usageMode":keepUsageModeCmd}},{"out":0})
            sleep(1.5)
            if keepUsageModeCmd == 3:
                self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'KeepUsgModProxyReq',[13, 13, 13, 13, 13, 13, 13, 13, 13, 13])
            else:
                self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'KeepUsgModProxyReq',[keepUsageModeCmd, keepUsageModeCmd, keepUsageModeCmd,keepUsageModeCmd, keepUsageModeCmd, keepUsageModeCmd,
                                                                                                            keepUsageModeCmd, keepUsageModeCmd, keepUsageModeCmd])
    @allure.title("SetParkingComfortModeCtrl_OK")
    @pytest.mark.smoke
    def test_caseid_100180(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetParkingComfortModeCtrl", {"parkingComfortModeCtrlCmd":{"isOpenReq":True}},{"out":0})
        self.soa.soa_partner.empty_all(0.5)
        self.mock.empty()
        for CnvModProxyReq in [False,True]:
            logger.info({f'当前保持为{CnvModProxyReq}'})
            self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetParkingComfortModeCtrl", {"parkingComfortModeCtrlCmd":{"isOpenReq":CnvModProxyReq} },{"out":0})
            sleep(0.5)
        result = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'CnvModProxyReq')
        assert result == [1, 1, 1, 1, 0, 0, 2, 2, 2, 0, 0]
            
    @allure.title("SetDynoModeCtrl_OK")
    @pytest.mark.smoke
    def test_caseid_100176(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetDynoModeCtrl", {"dynoModeCtrlCmd":{"dynoMode":1}},{"out":0})
        self.soa.soa_partner.empty_all(0.5)
        for dynoMode in range(2):
            self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetDynoModeCtrl", {"dynoModeCtrlCmd":{"dynoMode":dynoMode} },{"out":0})
            sleep(1)
            
    @allure.title("SetDynoModeCtrl_下行pdu校验")
    @pytest.mark.smoke
    def test_caseid_100170(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetDynoModeCtrl", {"dynoModeCtrlCmd":{"dynoMode":1}},{"out":0})
        self.soa.soa_partner.empty_all(1)
        self.mock.empty()
        for dynoMode in range(2):
            logger.info({f'当前转毂模式为{dynoMode}'})
            self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetDynoModeCtrl", {"dynoModeCtrlCmd":{"dynoMode":dynoMode} },{"out":0})
            sleep(0.5)
        result = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'SetDynoModProxyReq')
        assert result == [1, 1, 1, 0, 0, 2, 2, 2, 0, 0]
            
    @allure.title("CarModeInfo_遍历carmode状态")
    @pytest.mark.smoke
    def test_caseid_100163(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast,"VMMGlbSigCarModSts", 2)
        self.soa.soa_partner.empty_all(0.5)
        for carmode in [1,2,3,8,0]:
            logger.info({f'当前carmode状态{carmode}'})
            self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigCarModSts", carmode)
            self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "CarModeInfo", {"carModeInfo":{"validity":0,"carModeSts":carmode}},timeout=2)
        sleep(0.5)
            
    @allure.title("UsageModeInfo_UsgModSts遍历")
    @pytest.mark.smoke
    def test_caseid_100148(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for usgmode in [0,1,2,13,1]:
            logger.info({f'当前usgmode是{usgmode}'})
            self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", usgmode)
            if usgmode ==13:
                self.soa.ck_s2s_event(VEHICLE_MODE_SERVICE_CLIENT, "UsageModeInfo", {"usageModeInfo":{"validity":0, "usageModeSts":3}})
            else:
                self.soa.ck_s2s_event(VEHICLE_MODE_SERVICE_CLIENT, "UsageModeInfo", {"usageModeInfo":{"validity":0, "usageModeSts":usgmode}})
        
    @allure.title("UsageModeInfo_InactiveSubSts遍历")
    @pytest.mark.smoke
    def test_caseid_100147(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigInactvSubSts1", 1)
        self.soa.soa_partner.empty_all(0.5)
        for usgmode1 in range(3):
            logger.info({f'当前InactiveSubSts是{usgmode1}'})
            self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigInactvSubSts1", usgmode1)
            self.soa.ck_s2s_event(VEHICLE_MODE_SERVICE_CLIENT, "UsageModeInfo", {"usageModeInfo":{"validity":1, "inactiveSubSts":usgmode1}})
            
    @allure.title("UsageModeInfo_ConvenienceSubSts遍历")
    @pytest.mark.smoke
    def test_caseid_100146(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 2)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigCnvincSubSts1", 1)
        self.soa.soa_partner.empty_all(0.5)
        for usgmode2 in range(3):
            logger.info({f'当前convenience状态{usgmode2}'})
            self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigCnvincSubSts1", usgmode2)
            self.soa.ck_s2s_event(VEHICLE_MODE_SERVICE_CLIENT, "UsageModeInfo", {"usageModeInfo":{"validity":1, "convenienceSubSts":usgmode2}})
            
    @allure.title("UsageModeInfo_validity有效")
    @pytest.mark.sanity
    def test_caseid_100344(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigDrvgSubSts1", 1)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigInactvSubSts1", 1)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigCnvincSubSts1",1)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigInactvSubSts1", 2)
        self.soa.ck_s2s_event(VEHICLE_MODE_SERVICE_CLIENT, "UsageModeInfo", {"usageModeInfo":{"validity":0,"usageModeSts":1,"inactiveSubSts":2,"convenienceSubSts":1,"drivingSubSts":1}})
    
    @allure.title("UsageModeInfo_DrivingSubSts遍历")
    @pytest.mark.smoke
    def test_caseid_100145(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 3)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigDrvgSubSts1", 1)
        self.soa.soa_partner.empty_all(0.5)
        for usgmode3 in range(4):
            logger.info({f'当前DrivingSubSts状态{usgmode3}'})
            self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigDrvgSubSts1", usgmode3)
            self.soa.ck_s2s_event(VEHICLE_MODE_SERVICE_CLIENT, "UsageModeInfo", {"usageModeInfo":{"validity":1, "drivingSubSts":usgmode3}})
            
    @allure.title("UsageModeInfo_KeepConvenienceSts遍历")
    @pytest.mark.smoke
    def test_caseid_100343(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "CnvKeepSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for keepmode in range(3):
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "CnvKeepSts", keepmode)
            self.soa.ck_s2s_event(VEHICLE_MODE_SERVICE_CLIENT, "UsageModeInfo", {"usageModeInfo":{"keepConvenienStsValidity":0, "keepConvenienceSts":keepmode}})
            sleep(0.5)
            
    @allure.title("SetKeepUsageModeCtrl_InterfaceOccupied")
    @pytest.mark.sanity
    def test_caseid_100343(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "CnvKeepSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for keepmode in range(3):
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "CnvKeepSts", keepmode)
            self.soa.ck_s2s_event(VEHICLE_MODE_SERVICE_CLIENT, "UsageModeInfo", {"usageModeInfo":{"keepConvenienStsValidity":0, "keepConvenienceSts":keepmode}})
            sleep(0.5)
            
    @allure.title("DynoModeInfo_从开始到关闭")
    @pytest.mark.sanity
    def test_caseid_100156(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "DynoModSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for dynoMode in range(2):
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "DynoModSts", dynoMode)
            self.soa.ck_s2s_event(VEHICLE_MODE_SERVICE_CLIENT, "DynoModeInfo", {"dynoModeInfo":{"validity":0, "dynoModeSts":dynoMode}})
            
    @allure.title("StartInhibitInfo_打开到关闭")
    @pytest.mark.sanity
    def test_caseid_100167(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "StrtInhbSts", False)
        sleep(1)
        for isInhibitSts in [True, False]:
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "StrtInhbSts", isInhibitSts)
            self.soa.ck_s2s_event(VEHICLE_MODE_SERVICE_CLIENT, "StartInhibitInfo", {"startInhibitInfo":{"validity":0, "isInhibitSts":isInhibitSts}})
            sleep(0.5)
            
    @allure.title("StartInhibitInfo_启动场景默认值获取&无通知")
    @pytest.mark.sanity
    def test_caseid_100169(self):#todo 信号停发了但是validity没有从0变成4所以没有event上报
        self.ssh.rerun_car_service()
        self.soa.empty_all(0.5) 
        self.soa.wait_for_service_reconnect(VEHICLE_MODE_SERVICE_CLIENT)
        sleep(1.5)
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "StrtInhbSts", True)
        sleep(1)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204005)
        logger.info({"停发0x204005"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "StartInhibitInfo", {"startInhibitInfo":{"validity":4, "isInhibitSts":True}},deviation=0.2, timeout=4)
        sleep(0.5)
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204005)
        logger.info({"恢复0x204005"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "StartInhibitInfo", {"startInhibitInfo":{"validity":0, "isInhibitSts":True}},deviation=0.2)
        
    @allure.title("SetKeepUsageModeCtrl_周期维持请求, 超时释放")
    @pytest.mark.sanity
    def test_caseid_100185(self):
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd":{"usageMode":3}})
        self.soa.soa_partner.empty_all(0.1)
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd":{"usageMode":0}})
        sleep(2)
        self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'KeepUsgModProxyReq',[13, 13, 13, 13, 13, 13, 13, 13, 13, 13])
        
    @allure.title("SetKeepUsageModeCtrl_InterfaceOccupied")
    @pytest.mark.sanity
    def test_caseid_100186(self):
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd":{"usageMode":3}})
        self.soa.soa_partner.empty_all(0.1)
        for usageMode in [2, 1]:
            logger.info({f'当前usageMode是{usageMode}'})
            self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd":{"usageMode":usageMode}},{"out":9})
            
    @allure.title("SetKeepUsageModeCtrl_200ms窗口可以被高取值调用打断")
    @pytest.mark.sanity
    def test_caseid_100183(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd":{"usageMode":1}},{"out":0})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd":{"usageMode":2}},{"out":0})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd":{"usageMode":3}},{"out":0})
        sleep(1.1)
        self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'KeepUsgModProxyReq',[1,1,2,2,3, 3, 3, 3, 3, 3, 3, 3, 3])
        
    @allure.title("SetDynoModeCtrl_打断响应最新接口调用值1被2打断")
    @pytest.mark.sanity
    def test_caseid_100175(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetDynoModeCtrl", {"dynoModeCtrlCmd":{"dynoMode":0}},{"out":0})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetDynoModeCtrl", {"dynoModeCtrlCmd":{"dynoMode":1}},{"out":0})
        sleep(1.1)
        self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'SetDynoModProxyReq',[ 1, 2, 2, 2,])
        
    @allure.title("SetDynoModeCtrl_RequestOutOfRange不会下行_dynoMode")
    @pytest.mark.sanity
    def test_caseid_100171(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetDynoModeCtrl", {"dynoModeCtrlCmd":{"dynoMode":0} },{"out":0})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetDynoModeCtrl", {"dynoModeCtrlCmd":{"dynoMode":2} },{"out":1})
        sleep(1.1)
        self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'SetDynoModProxyReq',[1,1,1])
        
    @allure.title("SetParkingComfortModeCtrl_打断_相同值")
    @pytest.mark.sanity
    def test_caseid_100178(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetParkingComfortModeCtrl", {"parkingComfortModeCtrlCmd":{"isOpenReq":False} },{"out":0})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetParkingComfortModeCtrl", {"parkingComfortModeCtrlCmd":{"isOpenReq":False} },{"out":0})
        sleep(1.1)
        self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'CnvModProxyReq',[1, 1, 1, 1])
        
    @allure.title("SetParkingComfortModeCtrl_打断_不同值")
    @pytest.mark.sanity
    def test_caseid_100179(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetParkingComfortModeCtrl", {"parkingComfortModeCtrlCmd":{"isOpenReq":True} },{"out":0})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetParkingComfortModeCtrl", {"parkingComfortModeCtrlCmd":{"isOpenReq":False} },{"out":0})
        sleep(1.1)
        self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'CnvModProxyReq',[2, 2, 1, 1,1])
        
    @allure.title("OccupyInfo_userInCarSts_driverInCarSts遍历")
    @pytest.mark.sanity
    def test_caseid_100141(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "UsrInCarSts", 0)
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "DrvrInCarSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        logger.info({"设置信号"})
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "UsrInCarSts", 1)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"userInCarStsValidity":0,"userInCarSts":1,"driverInCarStsValidity":0,"driverInCarSts":0}})
        self.soa.soa_partner.empty_all(0.5)
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "DrvrInCarSts", 1)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"userInCarStsValidity":0,"userInCarSts":1,"driverInCarStsValidity":0,"driverInCarSts":1}})
        
    @allure.title("OccupyInfo_thirdRightOccupySts_seatOccpyActionFusionSts_seatOccpyFaultSts_遍历")
    @pytest.mark.sanity
    def test_caseid_100102(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsThrdRowRiSeatSts", 1)
        self.mock.set_signal(UdpChannel.LcuR_Multicast, "ThrdRowRiOccpSnsrOKSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号ActFusnSeatStsThrdRowRiSeatSts{mcu_soc}"})
            logger.info({f"设置信号ThrdRowRiOccpSnsrOKSts{mcu_soc}"})
            self.mock.set_signal(UdpChannel.LcuR_Multicast, "ThrdRowRiOccpSnsrOKSts", mcu_soc)
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsThrdRowRiSeatSts", mcu_soc)
            self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdRightOccupySts":{"validity":0,"seatOccpyActionFusionSts":mcu_soc,"seatOccpyFaultSts":mcu_soc}}})
            
    @allure.title("OccupyInfo_thirdRightOccupySts_seatOccpyRawSts遍历")
    @pytest.mark.sanity
    def test_caseid_100101(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsThrdRowRiSeatSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号SeatOccpStsThrdRowRiSeatSts{mcu_soc}"})
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsThrdRowRiSeatSts", mcu_soc)
            if mcu_soc == 1:
                self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdRightOccupySts":{"validity":0,"seatOccpyRawSts":5}}})
            else:
                self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdRightOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
            
    @allure.title("OccupyInfo_thirdMiddleOccupySts_seatOccpyActionFusionSts_seatOccpyFaultSts_遍历")
    @pytest.mark.sanity
    def test_caseid_100107(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsThrdRowMidSeatSts", 1)
        self.mock.set_signal(UdpChannel.LcuL_Multicast, "ThrdRowMidOccpSnsrOKSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号ActFusnSeatStsThrdRowMidSeatSts{mcu_soc}"})
            logger.info({f"设置信号ThrdRowMidOccpSnsrOKSts{mcu_soc}"})
            self.mock.set_signal(UdpChannel.LcuL_Multicast, "ThrdRowMidOccpSnsrOKSts", mcu_soc)
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsThrdRowMidSeatSts", mcu_soc)
            self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdMiddleOccupySts":{"validity":0,"seatOccpyActionFusionSts":mcu_soc,"seatOccpyFaultSts":mcu_soc}}})
            
            
    @allure.title("OccupyInfo_thirdMiddleOccupySts_seatOccpyRawSts遍历")
    @pytest.mark.sanity
    def test_caseid_100106(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsThrdRowMidSeatSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号SeatOccpStsThrdRowMidSeatSts{mcu_soc}"})
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsThrdRowMidSeatSts", mcu_soc)
            if mcu_soc == 1:
                self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdMiddleOccupySts":{"validity":0,"seatOccpyRawSts":5}}})
            else:
                self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdMiddleOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
        
        
    @allure.title("OccupyInfo_thirdLeftOccupySts_seatOccpyActionFusionSts_seatOccpyFaultSts_遍历")
    @pytest.mark.sanity
    def test_caseid_100112(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsThrdRowLeSeatSts", 1)
        self.mock.set_signal(UdpChannel.LcuL_Multicast, "ThrdRowLeOccpSnsrOKSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号ActFusnSeatStsThrdRowLeSeatSts{mcu_soc}"})
            logger.info({f"设置信号ThrdRowLeOccpSnsrOKSts{mcu_soc}"})
            self.mock.set_signal(UdpChannel.LcuL_Multicast, "ThrdRowLeOccpSnsrOKSts", mcu_soc)
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsThrdRowLeSeatSts", mcu_soc)
            self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdLeftOccupySts":{"validity":0,"seatOccpyActionFusionSts":mcu_soc,"seatOccpyFaultSts":mcu_soc}}})
            
    @allure.title("OccupyInfo_thirdLeftOccupySts_seatOccpyRawSts遍历")
    @pytest.mark.sanity
    def test_caseid_100111(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsThrdRowLeSeatSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号SeatOccpStsThrdRowLeSeatSts{mcu_soc}"})
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsThrdRowLeSeatSts", mcu_soc)
            if mcu_soc == 1:
                self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdLeftOccupySts":{"validity":0,"seatOccpyRawSts":5}}})
            else:
                self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdLeftOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
                
    @allure.title("OccupyInfo_secondRightOccupySts_seatOccpyActionFusionSts_seatOccpyFaultSts_遍历")
    @pytest.mark.sanity
    def test_caseid_100117(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsSecRowRiSeatSts", 1)
        self.mock.set_signal(UdpChannel.LcuR_Multicast, "SecRowRiOccpSnsrOKSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号ActFusnSeatStsSecRowRiSeatSts{mcu_soc}"})
            logger.info({f"设置信号SecRowRiOccpSnsrOKSts{mcu_soc}"})
            self.mock.set_signal(UdpChannel.LcuR_Multicast, "SecRowRiOccpSnsrOKSts", mcu_soc)
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsSecRowRiSeatSts", mcu_soc)
            self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondRightOccupySts":{"validity":0,"seatOccpyActionFusionSts":mcu_soc,"seatOccpyFaultSts":mcu_soc}}})
            
    @allure.title("OccupyInfo_secondRightOccupySts_seatOccpyRawSts遍历")
    @pytest.mark.sanity
    def test_caseid_100116(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsSecRowRiSeatSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号SeatOccpStsSecRowRiSeatSts{mcu_soc}"})
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsSecRowRiSeatSts", mcu_soc)
            if mcu_soc == 1:
                self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondRightOccupySts":{"validity":0,"seatOccpyRawSts":5}}})
            else:
                self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondRightOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
        
    @allure.title("OccupyInfo_secondMiddleOccupySts_seatOccpyActionFusionSts_seatOccpyFaultSts_遍历")
    @pytest.mark.sanity
    def test_caseid_100122(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsSecRowMidSeatSts", 1)
        self.mock.set_signal(UdpChannel.LcuL_Multicast, "SecRowMidOccpSnsrOKSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号ActFusnSeatStsSecRowRiSeatSts{mcu_soc}"})
            logger.info({f"设置信号SecRowMidOccpSnsrOKSts{mcu_soc}"})
            self.mock.set_signal(UdpChannel.LcuL_Multicast, "SecRowMidOccpSnsrOKSts", mcu_soc)
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsSecRowMidSeatSts", mcu_soc)
            self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondMiddleOccupySts":{"validity":0,"seatOccpyActionFusionSts":mcu_soc,"seatOccpyFaultSts":mcu_soc}}})
            
    @allure.title("OccupyInfo_secondMiddleOccupySts_seatOccpyRawSts遍历")
    @pytest.mark.sanity
    def test_caseid_100121(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsSecRowMidSeatSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号SeatOccpStsSecRowMidSeatSts{mcu_soc}"})
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsSecRowMidSeatSts", mcu_soc)
            if mcu_soc == 1:
                self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondMiddleOccupySts":{"validity":0,"seatOccpyRawSts":5}}})
            else:
                self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondMiddleOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
                
    @allure.title("OccupyInfo_secondLeftOccupySts_seatOccpyActionFusionSts_seatOccpyFaultSts_遍历")
    @pytest.mark.sanity
    def test_caseid_100127(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsSecRowLeSeatSts", 1)
        self.mock.set_signal(UdpChannel.LcuL_Multicast, "SecRowLeOccpSnsrOKSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号ActFusnSeatStsSecRowLeSeatSts{mcu_soc}"})
            logger.info({f"设置信号SecRowLeOccpSnsrOKSts{mcu_soc}"})
            self.mock.set_signal(UdpChannel.LcuL_Multicast, "SecRowLeOccpSnsrOKSts", mcu_soc)
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsSecRowLeSeatSts", mcu_soc)
            self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondLeftOccupySts":{"validity":0,"seatOccpyActionFusionSts":mcu_soc,"seatOccpyFaultSts":mcu_soc}}})
            
    @allure.title("OccupyInfo_secondLeftOccupySts_seatOccpyRawSts遍历")
    @pytest.mark.sanity
    def test_caseid_100126(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsSecRowLeSeatSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号SeatOccpStsSecRowLeSeatSts{mcu_soc}"})
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsSecRowLeSeatSts", mcu_soc)
            if mcu_soc == 1:
                self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondLeftOccupySts":{"validity":0,"seatOccpyRawSts":5}}})
            else:
                self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondLeftOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
                
    @allure.title("OccupyInfo_passengerOccupySts_seatOccpyActionFusionSts_seatOccpyFaultSts_遍历")
    @pytest.mark.sanity
    def test_caseid_100132(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsPassSeatSts", 1)
        self.mock.set_signal(UdpChannel.LcuR_Multicast, "PassSeatOccpSnsrOKSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号ActFusnSeatStsPassSeatSts{mcu_soc}"})
            logger.info({f"设置信号PassSeatOccpSnsrOKSts{mcu_soc}"})
            self.mock.set_signal(UdpChannel.LcuR_Multicast, "PassSeatOccpSnsrOKSts", mcu_soc)
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsPassSeatSts", mcu_soc)
            self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"passengerOccupySts":{"validity":0,"seatOccpyActionFusionSts":mcu_soc,"seatOccpyFaultSts":mcu_soc}}})
            
    @allure.title("OccupyInfo_passengerOccupySts_seatOccpyRawSts遍历")
    @pytest.mark.sanity
    def test_caseid_100131(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsPassSeatSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号SeatOccpStsPassSeatSts{mcu_soc}"})
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsPassSeatSts", mcu_soc)
            if mcu_soc == 1:
                self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"passengerOccupySts":{"validity":0,"seatOccpyRawSts":5}}})
            else:
                self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"passengerOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
                
    @allure.title("OccupyInfo_driverOccupySts_seatOccpyActionFusionSts_seatOccpyFaultSts_遍历")
    @pytest.mark.sanity
    def test_caseid_100139(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsDrvrSeatSts", 1)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "DrvrSeatOccpSnsrOKSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号ActFusnSeatStsDrvrSeatSts{mcu_soc}"})
            logger.info({f"设置信号DrvrSeatOccpSnsrOKSts{mcu_soc}"})
            self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "DrvrSeatOccpSnsrOKSts", mcu_soc)
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsDrvrSeatSts", mcu_soc)
            self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"driverOccupySts":{"validity":0,"seatOccpyActionFusionSts":mcu_soc,"seatOccpyFaultSts":mcu_soc}}})
            
    @allure.title("OccupyInfo_driverOccupySts_seatOccpyRawSts遍历")
    @pytest.mark.sanity
    def test_caseid_100138(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsDrvrSeatSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号SeatOccpStsDrvrSeatSts{mcu_soc}"})
            self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsDrvrSeatSts", mcu_soc)
            if mcu_soc == 1:
                self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"driverOccupySts":{"validity":0,"seatOccpyRawSts":5}}})
            else:
                self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"driverOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
                
    @allure.title("UsageModeInfo_Validity4")
    @pytest.mark.full
    def test_caseid_100144(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 2)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigCnvincSubSts1", 2)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "UsageModeInfo", {"usageModeInfo":{"validity": 0, "usageModeSts": 2, "inactiveSubSts": 0, "convenienceSubSts": 2, "drivingSubSts": 0}})
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_Multicast, 0x20FF04)
        sleep(2)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "UsageModeInfo", {"usageModeInfo":{"validity": 4, "usageModeSts": 2, "inactiveSubSts": 0, "convenienceSubSts": 2, "drivingSubSts": 0}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_Multicast, 0x20FF04)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "UsageModeInfo", {"usageModeInfo":{"validity": 0, "usageModeSts": 2, "inactiveSubSts": 0, "convenienceSubSts": 2, "drivingSubSts": 0}})
        
    @allure.title("UsageModeInfo_Validity从1到4")
    @pytest.mark.full
    def test_caseid_100149(self):
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_Multicast, 0x20FF04)
        self.ssh.rerun_car_service()
        self.soa.empty_all(2) 
        self.soa.wait_for_service_reconnect(VEHICLE_MODE_SERVICE_CLIENT)
        sleep(1.5)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "GetUsageModeInfoAsync",{},{"out":{"validity": 1, "usageModeSts": 255, "inactiveSubSts": 255, "convenienceSubSts": 255, "drivingSubSts": 255}})
        self.soa.ck_s2s_event(VEHICLE_MODE_SERVICE_CLIENT, "UsageModeInfo", {"usageModeInfo":{"validity":4,"usageModeSts":255,"inactiveSubSts":255,"convenienceSubSts":255,"drivingSubSts":255}})
                                                                        
    @allure.title("UsageModeInfo_启动场景默认值获取&无通知")
    @pytest.mark.full
    def test_caseid_100150(self):
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_Multicast, 0x20FF04)
        self.ssh.rerun_car_service()
        self.soa.empty_all(0.5) 
        self.soa.wait_for_service_reconnect(VEHICLE_MODE_SERVICE_CLIENT)
        sleep(1.5)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "GetUsageModeInfoAsync",{},{"out":{"validity": 1, "usageModeSts": 255, "inactiveSubSts": 255, "convenienceSubSts": 255, "drivingSubSts": 255}})
        
    @allure.title("UsageModeInfo_降频_100ms内发布多次")
    @pytest.mark.full
    def test_caseid_100143(self):
        self.soa.empty_all(0.5)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        sleep(0.02)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 3)
        sleep(0.02)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 2)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "UsageModeInfo", {"usageModeInfo":{"validity": 0, "usageModeSts": 2}})
        
    @allure.title("StartInhibitInfo_Validity4")
    @pytest.mark.full
    def test_caseid_100165(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "StrtInhbSts", 0)
        sleep(1)
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "StrtInhbSts", 1)
        logger.info({f"设置信号为1"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "StartInhibitInfo", {"startInhibitInfo":{"validity":0, "isInhibitSts":True}}, timeout=2)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204005)
        sleep(1.5)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "StartInhibitInfo", {"startInhibitInfo":{"validity":4, "isInhibitSts":True}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204005)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "StartInhibitInfo", {"startInhibitInfo":{"validity":0, "isInhibitSts":True}})
        
    @allure.title("StartInhibitInfo_启动场景发送isInhibitSts默认值")
    @pytest.mark.full
    def test_caseid_100168(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "StrtInhbProxyReq", 1)
        logger.info({f"设置信号为1"})
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "GetStartInhibitInfoAsync",{}, {"out":{"validity":0, "isInhibitSts":True}})
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204005)
        self.ssh.rerun_car_service()
        self.soa.empty_all(0.5) 
        self.soa.wait_for_service_reconnect(VEHICLE_MODE_SERVICE_CLIENT)
        sleep(1.5)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "GetStartInhibitInfoAsync", {"out":{"validity":4, "isInhibitSts":False}})
        
    @allure.title("StartInhibitInfo_两次event间隔50ms")
    @pytest.mark.full
    def test_caseid_100166(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "StrtInhbProxyReq", 0)
        self.soa.empty_all(0.5)
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "StrtInhbProxyReq", 1)
        sleep(0.02)
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "StrtInhbProxyReq", 0)
        self.soa.ck_no_event(VEHICLE_MODE_SERVICE_CLIENT, "StartInhibitInfo",{})
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "GetStartInhibitInfoAsync", {"out":{"validity":4, "isInhibitSts":False}})
        

    @allure.title("DynoModeInfo_Validity4")
    @pytest.mark.full
    def test_caseid_100155(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "DynoModSts", 1)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        self.soa.empty_all(1.5) 
        self.soa.ck_s2s_event(VEHICLE_MODE_SERVICE_CLIENT, "DynoModeInfo", {"dynoModeInfo":{"validity":4, "dynoModeSts":1}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        self.soa.ck_s2s_event(VEHICLE_MODE_SERVICE_CLIENT, "DynoModeInfo", {"dynoModeInfo":{"validity":0, "dynoModeSts":1}})
        
    @allure.title("DynoModeInfo_启动场景默认值获取&无通知")
    @pytest.mark.full
    def test_caseid_100157(self):
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        self.ssh.rerun_car_service()
        self.soa.empty_all(0.5) 
        self.soa.wait_for_service_reconnect(VEHICLE_MODE_SERVICE_CLIENT)
        sleep(1.5)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "GetDynoModeInfoAsync",{}, {"out":{"validity":1, "dynoModeSts":255}})
        
    @allure.title("CarModeInfo_降频_100ms内发布多次")
    @pytest.mark.full
    def test_caseid_100158(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast,"VMMGlbSigCarModSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigCarModSts", 2)
        logger.info({f"设置信号为2"})
        sleep(0.02)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigCarModSts", 3)
        sleep(0.02)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigCarModSts", 8)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "CarModeInfo", {"carModeInfo":{"validity":0, "carModeSts":2}})
        
    @allure.title("CarModeInfo_Validity优先级7>4")
    @pytest.mark.full
    def test_caseid_100159(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigCarModSts", 1)
        #设置crc
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "CarModeInfo", {"carModeInfo":{"validity":7, "carModeSts":1}})
        self.soa.soa_partner.empty_all()
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x20FF04)
        sleep(1.5)
        self.soa.ck_no_event(VEHICLE_MODE_SERVICE_CLIENT, "StartInhibitInfo",{})
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "GetcarModeInfoAsync",{}, {"out":{"validity":7, "carModeSts":1}})
        
    @allure.title("CarModeInfo_Validity7")
    @pytest.mark.full
    def test_caseid_100160(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigCarModSts", 1)
        #设置crc
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "CarModeInfo", {"carModeInfo":{"validity":7, "carModeSts":1}})
        #恢复crc
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "CarModeInfo", {"carModeInfo":{"validity":0, "carModeSts":1}})
        
    @allure.title("CarModeInfo_Validity5")
    @pytest.mark.full
    def test_caseid_100161(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigCarModSts", 1)
        #设置crc中checksum错误
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "CarModeInfo", {"carModeInfo":{"validity":5, "carModeSts":1}})
        #恢复crc中checksum错误
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "CarModeInfo", {"carModeInfo":{"validity":0, "carModeSts":1}})
        
    @allure.title("CarModeInfo_Validity3")
    @pytest.mark.full
    def test_caseid_100162(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigCarModSts", 1)
        #设置crc中checkcounter错误
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "CarModeInfo", {"carModeInfo":{"validity":3, "carModeSts":1}})
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigCarModSts", 3)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "CarModeInfo", {"carModeInfo":{"validity":3, "carModeSts":3}})
        #恢复crc中checkcounter错误
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "CarModeInfo", {"carModeInfo":{"validity":0, "carModeSts":3}})
        
    @allure.title("CarModeInfo_启动场景默认值获取&无通知")
    @pytest.mark.full
    def test_caseid_100164(self):
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_Multicast, 0x20FF04)
        self.ssh.rerun_car_service()
        self.soa.empty_all(0.5) 
        self.soa.wait_for_service_reconnect(VEHICLE_MODE_SERVICE_CLIENT)
        sleep(1.5)
        logger.info({f"等待1.5s"})
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "GetCarModeInfoAsync",{}, {"out":{"validity":1, "carModeSts":255}})
        
    @allure.title("OccupyInfo_启动场景默认值获取&无通知")
    @pytest.mark.full
    def test_caseid_100142(self):
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_CCUSOCCD, 0x504007)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuR_Multicast, 0x60FF03)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_Multicast, 0x50FF02)
        self.ssh.rerun_car_service()
        self.soa.empty_all(0.5) 
        self.soa.wait_for_service_reconnect(VEHICLE_MODE_SERVICE_CLIENT)
        sleep(1.5)
        logger.info({f"等待1.5s"})
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "GetOccupyInfoAsync",{}, {"out":{"userInCarStsValidity":1,"userInCarSts":255,"driverInCarStsValidity":1,"driverInCarSts":255,
                                                                                    "driverOccupySts":{"validity":1,"seatOccpyRawSts":255,"seatOccpyActionFusionSts":255,"seatOccpyFaultSts":255},
                                                                                    "passengerOccupySts":{"validity":1,"seatOccpyRawSts":255,"seatOccpyActionFusionSts":255,"seatOccpyFaultSts":255},
                                                                                    "secondLeftOccupySts":{"validity":1,"seatOccpyRawSts":255,"seatOccpyActionFusionSts":255,"seatOccpyFaultSts":255},
                                                                                    "secondMiddleOccupySts":{"validity":1,"seatOccpyRawSts":255,"seatOccpyActionFusionSts":255,"seatOccpyFaultSts":255},
                                                                                    "secondRightOccupySts":{"validity":1,"seatOccpyRawSts":255,"seatOccpyActionFusionSts":255,"seatOccpyFaultSts":255},
                                                                                    "thirdLeftOccupySts":{"validity":1,"seatOccpyRawSts":255,"seatOccpyActionFusionSts":255,"seatOccpyFaultSts":255},
                                                                                    "thirdMiddleOccupySts":{"validity":1,"seatOccpyRawSts":255,"seatOccpyActionFusionSts":255,"seatOccpyFaultSts":255},
                                                                                    "thirdRightOccupySts":{"validity":1,"seatOccpyRawSts":255,"seatOccpyActionFusionSts":255,"seatOccpyFaultSts":255}}})
    
    @allure.title("OccupyInfo_Validity4_不影响其他参数发布")
    @pytest.mark.full
    def test_caseid_100097(self):
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_CCUSOCCD, 0x504007)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuR_Multicast, 0x60FF03)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_Multicast, 0x50FF02)
        self.ssh.rerun_car_service()
        self.soa.empty_all(0.5) 
        self.soa.wait_for_service_reconnect(VEHICLE_MODE_SERVICE_CLIENT)
        sleep(1.5)
        logger.info({f"等待1.5s"})
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "GetOccupyInfoAsync",{}, {"out":{"userInCarStsValidity":1,"userInCarSts":255,"driverInCarStsValidity":1,"driverInCarSts":255,
                                                                                    "driverOccupySts":{"validity":1,"seatOccpyRawSts":255,"seatOccpyActionFusionSts":255,"seatOccpyFaultSts":255},
                                                                                    "passengerOccupySts":{"validity":1,"seatOccpyRawSts":255,"seatOccpyActionFusionSts":255,"seatOccpyFaultSts":255},
                                                                                    "secondLeftOccupySts":{"validity":1,"seatOccpyRawSts":255,"seatOccpyActionFusionSts":255,"seatOccpyFaultSts":255},
                                                                                    "secondMiddleOccupySts":{"validity":1,"seatOccpyRawSts":255,"seatOccpyActionFusionSts":255,"seatOccpyFaultSts":255},
                                                                                    "secondRightOccupySts":{"validity":1,"seatOccpyRawSts":255,"seatOccpyActionFusionSts":255,"seatOccpyFaultSts":255},
                                                                                    "thirdLeftOccupySts":{"validity":1,"seatOccpyRawSts":255,"seatOccpyActionFusionSts":255,"seatOccpyFaultSts":255},
                                                                                    "thirdMiddleOccupySts":{"validity":1,"seatOccpyRawSts":255,"seatOccpyActionFusionSts":255,"seatOccpyFaultSts":255},
                                                                                    "thirdRightOccupySts":{"validity":1,"seatOccpyRawSts":255,"seatOccpyActionFusionSts":255,"seatOccpyFaultSts":255}}})
        
    @allure.title("OccupyInfo_userInCarSts_driverInCarSts_Validity4")
    @pytest.mark.full
    def test_caseid_100140(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "UsrInCarSts", 0)
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "DrvrInCarSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"userInCarStsValidity":4,"userInCarSts":0,"driverInCarStsValidity":4,"driverInCarSts":0}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"userInCarStsValidity":0,"userInCarSts":0,"driverInCarStsValidity":0,"driverInCarSts":0}})
        
    @allure.title("OccupyInfo_driverOccupySts_Validity4_不影响其他参数发布")
    @pytest.mark.full
    def test_caseid_100137(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsDrvrSeatSts", 0)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "DrvrSeatOccpSnsrOKSts", 0)
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsDrvrSeatSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"driverOccupySts":{"validity":4,"seatOccpyActionFusionSts":0,"seatOccpyFaultSts":0,"seatOccpyRawSts":0}}})
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "DrvrSeatOccpSnsrOKSts", 2)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"driverOccupySts":{"validity":4,"seatOccpyActionFusionSts":0,"seatOccpyFaultSts":2,"seatOccpyRawSts":0}}})
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsDrvrSeatSts", 1)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"driverOccupySts":{"validity":4,"seatOccpyActionFusionSts":1,"seatOccpyFaultSts":2,"seatOccpyRawSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"driverOccupySts":{"validity":0,"seatOccpyActionFusionSts":1,"seatOccpyFaultSts":2,"seatOccpyRawSts":0}}})
        
    @allure.title("OccupyInfo_driverOccupySts_Validity4_不影响其他参数发布")
    @pytest.mark.full
    def test_caseid_100137(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsDrvrSeatSts", 0)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "DrvrSeatOccpSnsrOKSts", 0)
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsDrvrSeatSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"driverOccupySts":{"validity":4,"seatOccpyActionFusionSts":0,"seatOccpyFaultSts":0,"seatOccpyRawSts":0}}})
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "DrvrSeatOccpSnsrOKSts", 2)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"driverOccupySts":{"validity":4,"seatOccpyActionFusionSts":0,"seatOccpyFaultSts":2,"seatOccpyRawSts":0}}})
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsDrvrSeatSts", 1)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"driverOccupySts":{"validity":4,"seatOccpyActionFusionSts":1,"seatOccpyFaultSts":2,"seatOccpyRawSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"driverOccupySts":{"validity":0,"seatOccpyActionFusionSts":1,"seatOccpyFaultSts":2,"seatOccpyRawSts":0}}})
        
    @allure.title("OccupyInfo_driverOccupySts_Validity4_不重复上报")
    @pytest.mark.full
    def test_caseid_100136(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsDrvrSeatSts", 0)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "DrvrSeatOccpSnsrOKSts", 0)
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsDrvrSeatSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"driverOccupySts":{"validity":4,"seatOccpyActionFusionSts":0,"seatOccpyFaultSts":0,"seatOccpyRawSts":0}}})
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_CCUSOCCD, 0x504007)
        self.soa.ck_no_event(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {})
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        self.soa.ck_no_event(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {})
        
    @allure.title("OccupyInfo_driverOccupySts_Validity4_不重复上报")
    @pytest.mark.full
    def test_caseid_100137(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsDrvrSeatSts", 0)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "DrvrSeatOccpSnsrOKSts", 0)
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsDrvrSeatSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"driverOccupySts":{"validity":4,"seatOccpyActionFusionSts":0,"seatOccpyFaultSts":0,"seatOccpyRawSts":0}}})
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_CCUSOCCD, 0x504007)
        self.soa.ck_no_event(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {})
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        self.soa.ck_no_event(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {})

    @allure.title("OccupyInfo_passengerOccupySts_seatOccpyActionFusionSts_Validity4")
    @pytest.mark.full
    def test_caseid_100129(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsPassSeatSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"passengerOccupySts":{"validity":0,"seatOccpyActionFusionSts":1}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"passengerOccupySts":{"validity":0,"seatOccpyActionFusionSts":0}}})
        
    @allure.title("OccupyInfo_passengerOccupySts_seatOccpyFaultSts_Validity4")
    @pytest.mark.full
    def test_caseid_100128(self):
        self.mock.set_signal(UdpChannel.LcuR_Multicast, "PassSeatOccpSnsrOKSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuR_Multicast, 0x60FF03)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"passengerOccupySts":{"validity":4,"seatOccpyFaultSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.LcuR_Multicast, 0x60FF03)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"passengerOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
        
    @allure.title("OccupyInfo_passengerOccupySts_seatOccpyRawStss_Validity4")
    @pytest.mark.full
    def test_caseid_100130(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsPassSeatSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"passengerOccupySts":{"validity":4,"seatOccpyRawSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"passengerOccupySts":{"validity":0,"seatOccpyRawSts":0}}})

    @allure.title("OccupyInfo_secondLeftOccupySts_seatOccpyActionFusionSts_Validity4")
    @pytest.mark.full
    def test_caseid_100124(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsSecRowLeSeatSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondLeftOccupySts":{"validity":4,"seatOccpyActionFusionSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondLeftOccupySts":{"validity":0,"seatOccpyActionFusionSts":0}}})
        
    @allure.title("OccupyInfo_secondLeftOccupySts_seatOccpyFaultSts_Validity4")
    @pytest.mark.full
    def test_caseid_100123(self):
        self.mock.set_signal(UdpChannel.LcuL_Multicast, "SecRowLeOccpSnsrOKSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_Multicast, 0x50FF02)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondLeftOccupySts":{"validity":4,"seatOccpyFaultSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.LcuL_Multicast, 0x50FF02)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondLeftOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
        
    @allure.title("OccupyInfo_secondLeftOccupySts_seatOccpyRawStss_Validity4")
    @pytest.mark.full
    def test_caseid_100125(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsSecRowLeSeatSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondLeftOccupySts":{"validity":4,"seatOccpyRawSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondLeftOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
       
    @allure.title("OccupyInfo_secondMiddleOccupySts_seatOccpyActionFusionSts_Validity4")
    @pytest.mark.full
    def test_caseid_100119(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsSecRowMidSeatSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondMiddleOccupySts":{"validity":4,"seatOccpyActionFusionSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondMiddleOccupySts":{"validity":0,"seatOccpyActionFusionSts":0}}})
        
    @allure.title("OccupyInfo_secondMiddleOccupySts_seatOccpyFaultSts_Validity4")
    @pytest.mark.full
    def test_caseid_100118(self):
        self.mock.set_signal(UdpChannel.LcuL_Multicast, "SecRowMidOccpSnsrOKSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_Multicast, 0x50FF02)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondMiddleOccupySts":{"validity":4,"seatOccpyFaultSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.LcuL_Multicast, 0x50FF02)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondMiddleOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
        
    @allure.title("OccupyInfo_secondMiddleOccupySts_seatOccpyRawStss_Validity4")
    @pytest.mark.full
    def test_caseid_100120(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsSecRowMidSeatSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondMiddleOccupySts":{"validity":4,"seatOccpyRawSts":0}}},timeout=3)
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondMiddleOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
            
    @allure.title("OccupyInfo_secondRightOccupySts_seatOccpyActionFusionSts_Validity4")
    @pytest.mark.full
    def test_caseid_100114(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsSecRowRiSeatSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondRightOccupySts":{"validity":4,"seatOccpyActionFusionSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondRightOccupySts":{"validity":0,"seatOccpyActionFusionSts":0}}})
        
    @allure.title("OccupyInfo_secondRightOccupySts_seatOccpyFaultSts_Validity4")
    @pytest.mark.full
    def test_caseid_100113(self):
        self.mock.set_signal(UdpChannel.LcuR_Multicast, "SecRowRiOccpSnsrOKSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuR_Multicast, 0x60FF03)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondRightOccupySts":{"validity":4,"seatOccpyFaultSts":0}}})
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuR_Multicast, 0x60FF03)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondRightOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
        
    @allure.title("OccupyInfo_secondRightOccupySts_seatOccpyRawStss_Validity4")
    @pytest.mark.full
    def test_caseid_100115(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsSecRowRiSeatSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondRightOccupySts":{"validity":4,"seatOccpyRawSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"secondRightOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
          
    @allure.title("OccupyInfo_thirdLeftOccupySts_seatOccpyActionFusionSts_Validity4")
    @pytest.mark.full
    def test_caseid_100109(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsThrdRowLeSeatSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdLeftOccupySts":{"validity":4,"seatOccpyActionFusionSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdLeftOccupySts":{"validity":0,"seatOccpyActionFusionSts":0}}})
        
    @allure.title("OccupyInfo_thirdLeftOccupySts_seatOccpyFaultSts_Validity4")
    @pytest.mark.full
    def test_caseid_100108(self):
        self.mock.set_signal(UdpChannel.LcuL_Multicast, "ThrdRowLeOccpSnsrOKSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_Multicast, 0x50FF02)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdLeftOccupySts":{"validity":4,"seatOccpyFaultSts":0}}})
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_Multicast, 0x50FF02)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdLeftOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
        
    @allure.title("OccupyInfo_thirdLeftOccupySts_seatOccpyRawStss_Validity4")
    @pytest.mark.full
    def test_caseid_100110(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsThrdRowLeSeatSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdLeftOccupySts":{"validity":4,"seatOccpyRawSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdLeftOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
        
    @allure.title("OccupyInfo_thirdMiddleOccupySts_seatOccpyActionFusionSts_Validity4")
    @pytest.mark.full
    def test_caseid_100104(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsThrdRowMidSeatSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdMiddleOccupySts":{"validity":4,"seatOccpyActionFusionSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdMiddleOccupySts":{"validity":0,"seatOccpyActionFusionSts":0}}})
        
    @allure.title("OccupyInfo_thirdMiddleOccupySts_seatOccpyFaultSts_Validity4")
    @pytest.mark.full
    def test_caseid_100103(self):
        self.mock.set_signal(UdpChannel.LcuL_Multicast, "ThrdRowMidOccpSnsrOKSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_Multicast, 0x50FF02)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdMiddleOccupySts":{"validity":4,"seatOccpyFaultSts":0}}})
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_Multicast, 0x50FF02)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdMiddleOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
        
    @allure.title("OccupyInfo_thirdMiddleOccupySts_seatOccpyRawSts_Validity4")
    @pytest.mark.full
    def test_caseid_100105(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsThrdRowMidSeatSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdMiddleOccupySts":{"validity":4,"seatOccpyRawSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdMiddleOccupySts":{"validity":0,"seatOccpyRawSts":0}}})

    @allure.title("OccupyInfo_thirdRightOccupySts_seatOccpyActionFusionSts_Validity4")
    @pytest.mark.full
    def test_caseid_100099(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "ActFusnSeatStsThrdRowRiSeatSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdRightOccupySts":{"validity":4,"seatOccpyActionFusionSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204003)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdRightOccupySts":{"validity":0,"seatOccpyActionFusionSts":0}}})
        
    @allure.title("OccupyInfo_thirdRightOccupySts_seatOccpyFaultSts_Validity4")
    @pytest.mark.full
    def test_caseid_100098(self):
        self.mock.set_signal(UdpChannel.LcuR_Multicast, "ThrdRowRiOccpSnsrOKSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_Multicast, 0x60FF03)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdRightOccupySts":{"validity":4,"seatOccpyFaultSts":0}}})
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_Multicast, 0x60FF03)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdRightOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
        
    @allure.title("OccupyInfo_thirdRightOccupySts_seatOccpyRawSts_Validity4")
    @pytest.mark.full
    def test_caseid_100100(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_CCUSOCCD, "SeatOccpStsThrdRowRiSeatSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        sleep(1.5)
        logger.info({f"停发1.5s"})
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdRightOccupySts":{"validity":4,"seatOccpyRawSts":0}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.CCUMCUCD_CCUSOCCD, 0x204008)
        self.soa.ck_field(VEHICLE_MODE_SERVICE_CLIENT, "OccupyInfo", {"occupyInfo":{"thirdRightOccupySts":{"validity":0,"seatOccpyRawSts":0}}})
        
    @allure.title("SetDynoModeCtrl_RequestOutOfRange_dynoMode")
    @pytest.mark.full
    def test_caseid_100172(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetDynoModeCtrl", {"dynoModeCtrlCmd":{"dynoMode":0} },{"out":0})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetDynoModeCtrl", {"dynoModeCtrlCmd":{"dynoMode":2} },{"out":1})
        
    @allure.title("SetDynoModeCtrl_100ms内下发3次请求响应最新值")
    @pytest.mark.full
    def test_caseid_100173(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetDynoModeCtrl", {"dynoModeCtrlCmd":{"dynoMode":0} },{"out":0})
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetDynoModeCtrl", {"dynoModeCtrlCmd":{"dynoMode":0} },{"out":0})
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetDynoModeCtrl", {"dynoModeCtrlCmd":{"dynoMode":1} },{"out":0})
        sleep(1)
        self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'SetDynoModProxyReq',[2,2,2])
        
    @allure.title("SetDynoModeCtrl_打断响应最新接口调用值1被1打断")
    @pytest.mark.full
    def test_caseid_100174(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetDynoModeCtrl", {"dynoModeCtrlCmd":{"dynoMode":1} },{"out":0})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetDynoModeCtrl", {"dynoModeCtrlCmd":{"dynoMode":0} },{"out":0})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetDynoModeCtrl", {"dynoModeCtrlCmd":{"dynoMode":0} },{"out":0})
        sleep(1)
        self.mock.ck_interrupt(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, "SetDynoModProxyReq",[2,1,1], 3, idle=0)
        
    @allure.title("SetKeepUsageModeCtrl_RequestOutOfRange")
    @pytest.mark.full
    def test_caseid_100187(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd":{"usageMode":4}},{"out":1})
        sleep(0.2)
        self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'KeepUsgModProxyReq',[0, 0])
            
    @allure.title("SetKeepUsageModeCtrl_1000ms期间调用下发KeepUsgModProxyReq= 0_Idle")
    @pytest.mark.full
    def test_caseid_100184(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd":{"usageMode":2}},{"out":0})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd":{"usageMode":1}},{"out":9})
        sleep(0.5)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd":{"usageMode":1}},{"out":0})
        sleep(1.1)
        self.mock.ck_interrupt(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, "KeepUsgModProxyReq",[2,1], 10, idle=0)
        
    @allure.title("SetKeepUsageModeCtrl_1000ms窗口可以被任意请求打断")
    @pytest.mark.full
    def test_caseid_100182(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd":{"usageMode":2}},{"out":0})
        sleep(0.3)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd":{"usageMode":1}},{"out":0})
        sleep(0.3)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd":{"usageMode":3}},{"out":0})
        sleep(1.1)
        self.mock.ck_interrupt(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, "KeepUsgModProxyReq",[2,1,13], 10, idle=0)

    @allure.title("SetKeepUsageModeCtrl_UsageModeNotAllowed")
    @pytest.mark.full
    def test_caseid_100345(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetKeepUsageModeCtrl", {"keepUsageModeCmd":{"usageMode":2}},{"out":3})
        
    @allure.title("SetParkingComfortModeCtrl_100ms内下发3次请求响应最新值")
    @pytest.mark.full
    def test_caseid_100177(self):
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetParkingComfortModeCtrl", {"parkingComfortModeCtrlCmd":{"isOpenReq":False}},{"out":0})
        sleep(0.02)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetParkingComfortModeCtrl", {"parkingComfortModeCtrlCmd":{"isOpenReq":False}},{"out":0})
        sleep(0.02)
        self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetParkingComfortModeCtrl", {"parkingComfortModeCtrlCmd":{"isOpenReq":True}},{"out":0})
        sleep(1)
        self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'CnvModProxyReq',[2, 2, 2, 0])

