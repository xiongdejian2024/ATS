#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :PowerSupplyService.py
@Time         :2024/11/06 18:00
@Author       :jingjing.wang@jiduauto.com
@Description  :
"""
import pytest
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.nuc_app import partner_process_check
from xat_ecu.legacy.soa_partner.src.partner_const_dp2 import *
from xat_ecu.legacy.sdk.Internal_ETH.tools.mock_udp_tcp_server_dp2 import MockUdp, MockTcp
from xat_ecu.legacy.sdk.Internal_ETH.tools.common_dp2 import TcpChannel, UdpChannel
from xat_ecu.api.interfaces.dp2.cd_service.soa import Soa
from xat_cases.dp2.cd_service.case_helper.test_sil_abc_base import *
from xat_ecu.legacy.common.logger import logger


class TestPowerSupplyService(TestSILAbcBase):
    def before_class(self, ecu: EcuInfo):
        super().before_class(self, ecu)
        logger.info("before_class")
        self.ssh.service_sil_test_preparation()
        self.soa.update([POWERSUPPLY_SERVICE_CLIENT, VEHICLE_MODE_SERVICE_CLIENT])
        self.mock.update_channel({
                                    # UdpChannel.CCUMCUCD_Multicast: None,
                                    #  UdpChannel.LcuL_Multicast: None,
                                    #  UdpChannel.LcuR_Multicast: None,
                                    #  UdpChannel.CCUMCUAD_CCUSOCCD: None,
                                    #  UdpChannel.CCUMCUCD_CCUSOCCD: None,
                                     UdpChannel.LcuL_CCUSOCCD: None,
                                     UdpChannel.LcuR_CCUSOCCD: None,
                                    #  TcpChannel.CdMcuTCPServer_CdSocTCPClient1: None,
                                    #  TcpChannel.LcuLTCPServer_CdSocTCPClient3: None,
                                    #  TcpChannel.LcuRTCPServer_CdSocTCPClient4: None,
                                    #  TcpChannel.AdMcuTCPServer_CdSocTCPClient2: None,
                                     })
        sleep(1)
        self.mock.resume_send_all_cycle_pdu()

    def before_each_func(self, ecu: EcuInfo):
        super().before_each_func(ecu)
        logger.info("before_each_func")
        # self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        

    def after_each_func(self, ecu: EcuInfo):
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu: EcuInfo):
        super().after_class(self, ecu)
        logger.info("after_class")

    @allure.title("SetPowerSupplyCtrl_OK")
    @pytest.mark.smoke
    def test_caseid_100273(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":{"sourceId": 1,"powerSupplyCtrl":[{"ecuName":"OPCR","switchReq":0}]}},
                                          {"out":0})
        self.soa.soa_partner.empty_all(0.5)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":{"sourceId": 1,"powerSupplyCtrl":[{"ecuName":"OPCR","switchReq":1},
                                                                                                                                                    {"ecuName":"DPOD","switchReq":1}]}},
                                          {"out":0})
        
    @allure.title("SetPowerSupplyCtrl_UsageModeNotAllowed")
    @pytest.mark.sanity
    def test_caseid_100272(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 0)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":{"powerSupplyCtrl":[{"ecuName":"OPCR","switchReq":1}]}},
                                          {"out":3})
        result = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'LoadPwrProxyReqOPCRPwrProxyReq')
        assert result == []
        
    @allure.title("SetPowerSupplyCtrl_校验下行pdu")
    @pytest.mark.smoke
    def test_caseid_100267(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":{"powerSupplyCtrl":[{"ecuName":"OPCR","switchReq":1}]}},
                                          {"out":0})
        sleep(3)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":{"powerSupplyCtrl":[{"ecuName":"OPCR","switchReq":0}]}},
                                          {"out":0})
        sleep(3)
        result = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'LoadPwrProxyReqOPCRPwrProxyReq')
        assert result == [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
        
    @allure.title("SetPowerSupplyCtrl_usgmode13调用多个ecu包含不允许设置的ecu")
    @pytest.mark.smoke
    def test_caseid_100258(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 3)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":
            {"powerSupplyCtrl":[{"ecuName":"OPCR","switchReq":0},{"ecuName":"DPOD","switchReq":1}, {"ecuName":"HCML","switchReq":1}, 
                                {"ecuName":"HCMR" ,"switchReq":0}, {"ecuName":"RCML" ,"switchReq":1}, {"ecuName":"RCMR" ,"switchReq":1}, {"ecuName":"CD","switchReq":0}]}},
                                          {"out":3})
        sleep(1)
        result1 = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'LoadPwrProxyReqOPCRPwrProxyReq')
        # result = self.mock.get_signal_values(TcpChannel.LcuLTCPServer_CdSocTCPClient3, ['LoadPwrProxyReqOPCRPwrProxyReq','LoadPwrProxyReqDPODPwrProxyReq','LoadPwrProxyReqHCMLPwrProxyReq',
        #                                                                                     'LoadPwrProxyReqRCMLPwrProxyReq','LoadPwrProxyReqRCMRPwrProxyReq',
        #                                                                                     'LoadPwrProxyReqCDPwrProxyReq'])
        result2 = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'LoadPwrProxyReqHCMRPwrProxyReq')
        # result = self.mock.get_signal_values(TcpChannel.LcuRTCPServer_CdSocTCPClient4, [ 'LoadPwrProxyReqHCMRPwrProxyReq','LoadPwrProxyReqRCMRPwrProxyReq'])
        assert result1 == []
        assert result2 == []
        
    @allure.title("SetPowerSupplyCtrl_对多个ECU上下电")
    @pytest.mark.smoke
    def test_caseid_100257(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":
            {"powerSupplyCtrl":[{"ecuName":'OPCR',"switchReq":0},{"ecuName":'DPOD',"switchReq":1}]}},
                                          {"out":0})
        self.soa.soa_partner.empty_all(3)
        result1 = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'LoadPwrProxyReqOPCRPwrProxyReq')
        result2 = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'LoadPwrProxyReqDPODPwrProxyReq')
        assert result1 == [1,1,1,1,1,0,0,0,0,0]
        assert result2 == [2,2,2,2,2,0,0,0,0,0]
        
    @allure.title("SetPowerSupplyCtrl_对多个ECU上下电_校验errorcode以及下发pdu")
    @pytest.mark.smoke
    def test_caseid_100256(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":
            {"powerSupplyCtrl":[{"ecuName":'OPCR',"switchReq":0},{"ecuName":'DPOD',"switchReq":1}]}},
                                          {"out":0})
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":
            {"powerSupplyCtrl":[{"ecuName":'OPCR',"switchReq":1},{"ecuName":'DPOD',"switchReq":0}]}},
                                          {"out":9})
        sleep(1.6)
        result1 = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'LoadPwrProxyReqOPCRPwrProxyReq')
        result2 = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'LoadPwrProxyReqDPODPwrProxyReq')
        assert result1 == [1, 1, 2, 2, 2, 2, 2]
        assert result2 == [0, 2, 2, 2, 2, 2, 2]
        
    @allure.title("SetConstantChannelCtrl_OK")
    @pytest.mark.smoke 
    def test_caseid_100255(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        for channelArea in range(2):
            logger.info({f'当前通道区域为{channelArea}'})
            for constantChannelID in range(101,106):
                logger.info({f'当前通道ID为{constantChannelID}'})
                for switchReq in range(2):
                    logger.info({f'当前通道开关为{switchReq}'})
                    self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetConstantChannelCtrl", {"constantChannelCtrlCmd":
                        {"ConstantChannelCtrlCmd":[{"config":{"channelArea":channelArea,"constantChannelID":constantChannelID,"switchReq":switchReq}}]}},
                                                        {"out":0})
                    self.soa.soa_partner.empty_all(0.5)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetConstantChannelCtrl", {"constantChannelCtrlCmd":
                        {"ConstantChannelCtrlCmd":[{"config":{"channelArea":0,"constantChannelID":101,"switchReq":1}},
                                                   {"config":{"channelArea":1,"constantChannelID":104,"switchReq":0}}]}},
                                                        {"out":0})
                    
    @allure.title("SetConstantChannelCtrl_OK_usgmode遍历")
    @pytest.mark.smoke 
    def test_caseid_100254(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 2)
        self.soa.soa_partner.empty_all(0.5)
        for usgMode in range(1,4):
            logger.info({f'当前usgMode为{usgMode}'})
            self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", usgMode)
            self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetConstantChannelCtrl", {"constantChannelCtrlCmd":{"config":[{"channelArea":0,"constantChannelID":101,"switchReq":0}]}},
                                                {"out":0})
            self.soa.soa_partner.empty_all(0.5)
            
    @allure.title("SetConstantChannelCtrl_下行pdu校验")
    @pytest.mark.smoke 
    def test_caseid_100244(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetConstantChannelCtrl", {"constantChannelCtrlCmd":{"config":[{"channelArea":0,"constantChannelID":101,"switchReq":0}]}},
                                            {"out":0})
        sleep(1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetConstantChannelCtrl", {"constantChannelCtrlCmd":{"config":[{"channelArea":0,"constantChannelID":101,"switchReq":1}]}},
                                            {"out":0})
        sleep(1)
        result = self.mock.get_signal_values(TcpChannel.LcuLTCPServer_CdSocTCPClient3, 'PwrContnsChLeCfgReqContnsLeCh1CfgReq')
        assert result == [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0]
        
    @allure.title("SetPowerSupplyProtectResetCtrl_OK")
    @pytest.mark.smoke 
    def test_caseid_100243(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyProtectResetCtrl", {},
                                            {"out":0})
        
    @allure.title("SetPowerSupplyProtectResetCtrl_OK_遍历usgmode")
    @pytest.mark.smoke 
    def test_caseid_100241(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        for usgMode in range(4):
            logger.info({f'当前usgMode为{usgMode}'})
            self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", usgMode)
            self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetConstantChannelCtrl", {},
                                                {"out":0})
            
    @allure.title("SetPowerSupplyProtectResetCtrl_下行pdu校验")
    @pytest.mark.smoke 
    def test_caseid_100240(self):
        sleep(1)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        sleep(0.5)
        self.soa.send_method_request(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyProtectResetCtrl", {})
        sleep(1.6)
        result1 = self.mock.get_signal_values(TcpChannel.LcuLTCPServer_CdSocTCPClient3, 'PwrChProtRstReq')
        result2 = self.mock.get_signal_values(TcpChannel.LcuRTCPServer_CdSocTCPClient4, 'PwrChProtRstReq')
        assert result1 == [1,1,1,1,1,0]
        assert result2 == [1,1,1,1,1,0]
        
    @allure.title("SetPowerSupplyCtrl_打断_回idle过程中")
    @pytest.mark.sanity 
    def test_caseid_100262(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":{"powerSupplyCtrl":[{"ecuName":'RML',"switchReq":1}]}},
                                                                                                                                                                        {"out":0})
        sleep(0.5)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":{"powerSupplyCtrl":[{"ecuName":'RML',"switchReq":1}]}},
                                                                                                                                                                        {"out":0})
        sleep(3)
        result = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'LoadPwrProxyReqRMLPwrProxyReq')
        assert result == [2,2,2,2,2,2,2,2,2,2,0,0,0,0,0]
        
    @allure.title("SetPowerSupplyProtectResetCtrl_打断_复位时打断")
    @pytest.mark.sanity
    def test_caseid_100238(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyProtectResetCtrl", {},{"out":0})
        sleep(1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyProtectResetCtrl", {},{"out":0})
        sleep(2)
        result1 = self.mock.get_signal_values(TcpChannel.LcuLTCPServer_CdSocTCPClient3, 'PwrChProtRstReq')
        result2 = self.mock.get_signal_values(TcpChannel.LcuRTCPServer_CdSocTCPClient4, 'PwrChProtRstReq')
        assert result1 == [1,1,1,1,1,1,1,1,1,1,0, 0, 0, 0, 0]
        assert result2 == [1,1,1,1,1,1,1,1,1,1,0, 0, 0, 0, 0]
        
    @allure.title("SetPowerSupplyProtectResetCtrl_打断_发送时打断")
    @pytest.mark.sanity
    def test_caseid_100239(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyProtectResetCtrl", {},{"out":0})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyProtectResetCtrl", {},{"out":0})
        sleep(2)
        result1 = self.mock.get_signal_values(TcpChannel.LcuLTCPServer_CdSocTCPClient3, 'PwrChProtRstReq')
        result2 = self.mock.get_signal_values(TcpChannel.LcuRTCPServer_CdSocTCPClient4, 'PwrChProtRstReq')
        assert result1 == [1,1,1,1,1,1,1,1,0, 0, 0, 0, 0]
        assert result2 == [1,1,1,1,1,1,1,1,0, 0, 0, 0, 0]
    
    @allure.title("SetPowerSupplyProtectResetCtrl_UsageModeNotAllowed")
    @pytest.mark.sanity
    def test_caseid_100242(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 0)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyProtectResetCtrl", {},{"out":3})
        
    @allure.title("SetPowerSupplyCtrl_打断_发送过程中")
    @pytest.mark.sanity 
    def test_caseid_100263(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":{"powerSupplyCtrl":[{"ecuName":'RML',"switchReq":1}]}},
                                                                                                                                                                        {"out":0})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":{"powerSupplyCtrl":[{"ecuName":'RML',"switchReq":1}]}},
                                                                                                                                                                        {"out":0})
        sleep(3)
        result = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'LoadPwrProxyReqRMLPwrProxyReq')
        assert result == [2,2,2,2,2,2,2,2,0,0,0,0,0]
        
    @allure.title("SetPowerSupplyCtrl_仲裁_上电打断下电")
    @pytest.mark.sanity 
    def test_caseid_100265(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":
            {"powerSupplyCtrl":[{"ecuName":'OPCR',"switchReq":1}]}},
                                          {"out":0})
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":
            {"powerSupplyCtrl":[{"ecuName":'OPCR',"switchReq":0}]}},{"out":9})
        sleep(3)
        result = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'LoadPwrProxyReqOPCRPwrProxyReq')
        assert result == [2, 2, 2, 2, 2, 0, 0, 0, 0, 0]
        
    @allure.title("SetPowerSupplyCtrl_仲裁_上电打断下电")
    @pytest.mark.sanity 
    def test_caseid_100264(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":
            {"powerSupplyCtrl":[{"ecuName":'OPCR',"switchReq":0}]}},
                                          {"out":0})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":
            {"powerSupplyCtrl":[{"ecuName":'OPCR',"switchReq":1}]}},{"out":0})
        sleep(3)
        result = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, 'LoadPwrProxyReqOPCRPwrProxyReq')
        assert result == [1,1,1,2,2,2,2,2,2,0,0,0,0,0]
        
    @allure.title("SetPowerSupplyCtrl_仲裁_OtherError")
    @pytest.mark.sanity 
    def test_caseid_100268(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 13)
        for ecuname in ["HCML","HCMR","RCML","RCMR","CD"]:
            self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetPowerSupplyCtrl", {"powerSupplyCtrlCmd":
                                                                        {"powerSupplyCtrl":[{"ecuName":ecuname,"switchReq":0}]}},
                                                                                                                            {"out":65535})
            sleep(0.1)
        
    @allure.title("SetConstantChannelCtrl_打断_复位时打断")
    @pytest.mark.sanity 
    def test_caseid_100247(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetConstantChannelCtrl", {"constantChannelCtrlCmd":{"config":[{"channelArea":0,"constantChannelID":101,"switchReq":0}]}},
                                            {"out":0})
        sleep(0.25)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetConstantChannelCtrl", {"constantChannelCtrlCmd":{"config":[{"channelArea":0,"constantChannelID":101,"switchReq":0}]}},
                                            {"out":0})
        sleep(2)
        self.mock.ck_ordered_array(TcpChannel.LcuLTCPServer_CdSocTCPClient3, 'PwrContnsChLeCfgReqContnsLeCh1CfgReq',[1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1,0, 0, 0, 0, 0])
    
    
    @allure.title("SetConstantChannelCtrl_打断_发送时打断")
    @pytest.mark.sanity 
    def test_caseid_100248(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetConstantChannelCtrl", {"constantChannelCtrlCmd":{"config":[{"channelArea":0,"constantChannelID":101,"switchReq":0}]}},
                                            {"out":0})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetConstantChannelCtrl", {"constantChannelCtrlCmd":{"config":[{"channelArea":0,"constantChannelID":101,"switchReq":0}]}},
                                            {"out":0})
        sleep(2)
        self.mock.ck_ordered_array(TcpChannel.LcuLTCPServer_CdSocTCPClient3, 'PwrContnsChLeCfgReqContnsLeCh1CfgReq',[1, 1, 1, 1, 1, 1, 1,0, 0, 0, 0, 0])
        
    @allure.title("SetConstantChannelCtrl_打断_信号不同不打断")
    @pytest.mark.sanity 
    def test_caseid_100250(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetConstantChannelCtrl", {"constantChannelCtrlCmd":{"config":[{"channelArea":0,"constantChannelID":101,"switchReq":0}]}},
                                            {"out":0})
        sleep(0.1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetConstantChannelCtrl", {"constantChannelCtrlCmd":{"config":[{"channelArea":0,"constantChannelID":102,"switchReq":0}]}},
                                            {"out":0})
        sleep(2)
        self.mock.ck_ordered_array(TcpChannel.LcuLTCPServer_CdSocTCPClient3, 'PwrContnsChLeCfgReqContnsLeCh1CfgReq',[ 1, 1, 1, 1, 1,0, 0, 0, 0, 0])
        self.mock.ck_ordered_array(TcpChannel.LcuLTCPServer_CdSocTCPClient3, 'PwrContnsChLeCfgReqContnsLeCh2CfgReq',[ 1, 1, 1, 1, 1,0, 0, 0, 0, 0])
        
    @allure.title("SetConstantChannelCtrl_UsageModeNotAllowed")
    @pytest.mark.sanity 
    def test_caseid_100253(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "VMMGlbSigUsgModSts", 0)
        sleep(1)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "SetConstantChannelCtrl", {"constantChannelCtrlCmd":{"config":[{"channelArea":0,"constantChannelID":101,"switchReq":0}]}},
                                            {"out":3})
        
    @allure.title("PowerSupplyInfo_参数变化发布_powerSupplyStatus")
    @pytest.mark.sanity 
    def test_caseid_100226(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "LoadPwrActStsOPCRPwrActSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_mul in range(2):
            logger.info({f"设置信号LoadPwrActStsOPCRPwrActSts{mcu_mul}"})
            self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "LoadPwrActStsOPCRPwrActSts", mcu_mul)
            self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "PowerSupplyInfo", {"powerSupplyInfo":{"channelStatus":[{"powerSupplyStatus":[{"validity":0,"ecuName":"OPCR","lvECUSts":mcu_mul}]}]}})
            
    @allure.title("PowerSupplyInfo_参数变化发布_ecuNameList&ecuAmount")
    @pytest.mark.sanity 
    def test_caseid_100227(self):
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrChLeCurrValSwilPwrChLe1CurrVal", 1)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrChLeCurrValSwilPwrChLe6CurrVal", 1)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrChLeCurrValSwilPwrChLe1CurrVal", 0)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrChLeCurrValSwilPwrChLe6CurrVal", 0)
        logger.info({f"设置信号LoadPwrActStsOPCRPwrActSts"})
        self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "PowerSupplyInfo", {"powerSupplyInfo":{"channelStatus":[{"ecuNameList":["OPCR"],"ecuAmount":1},{"ecuNameList":["SWTL", "SWTR", "HOD"],"ecuAmount":3}]}})
            
    @allure.title("PowerSupplyInfo_参数变化发布_channelSwitchSts")
    @pytest.mark.sanity 
    def test_caseid_100231(self):
        self.mock.set_signal(UdpChannel.LcuL_Multicast, "PwrChLeActStsSwilPwrChLe1ActSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for lcul_mul in range(2):
            logger.info({f"设置信号PwrChLeActStsSwilPwrChLe1ActSts{lcul_mul}"})
            self.mock.set_signal(UdpChannel.LcuL_Multicast, "PwrChLeActStsSwilPwrChLe1ActSts", lcul_mul)
            self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "PowerSupplyInfo", {"powerSupplyInfo":{"channelStatus":[{"channelSwitchSts":lcul_mul}]}})
            
    @allure.title("PowerSupplyInfo_参数变化发布_channelErrorSts_softwareErrorSts")
    @pytest.mark.sanity 
    def test_caseid_100229(self):
        self.mock.set_signal(UdpChannel.LcuL_Multicast, "PwrChLeErrSwilPwrChLe1Err", 0)
        self.soa.soa_partner.empty_all(0.5)
        for lcul_mul in [8, 127, 128]:
            logger.info({f"设置信号PwrChLeErrSwilPwrChLe1Err{lcul_mul}"})
            self.mock.set_signal(UdpChannel.LcuL_Multicast, "PwrChLeErrSwilPwrChLe1Err", lcul_mul)
            if lcul_mul ==127 :
                self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "PowerSupplyInfo", {"powerSupplyInfo":{"channelStatus":[{"channelErrorSts":{"softwareErrorSts":1}}]}})
            else:
                self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "PowerSupplyInfo", {"powerSupplyInfo":{"channelStatus":[{"channelErrorSts":{"softwareErrorSts":0}}]}})
                
    @allure.title("PowerSupplyInfo_参数变化发布_channelErrorSts_hardwareErrorSts")
    @pytest.mark.sanity 
    def test_caseid_100228(self):
        self.mock.set_signal(UdpChannel.LcuL_Multicast, "PwrChLeErrSwilPwrChLe1Err", 8)
        self.soa.soa_partner.empty_all(0.5)
        for lcul_mul in [1,62,255,128]:
            logger.info({f"设置信号PwrChLeErrSwilPwrChLe1Err{lcul_mul}"})
            self.mock.set_signal(UdpChannel.LcuL_Multicast, "PwrChLeErrSwilPwrChLe1Err", lcul_mul)
            if lcul_mul <= 62 :
                self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "PowerSupplyInfo", {"powerSupplyInfo":{"channelStatus":[{"channelErrorSts":{"hardwareErrorSts":[1]}}]}})
            else:
                self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "PowerSupplyInfo", {"powerSupplyInfo":{"channelStatus":[{"channelErrorSts":{"hardwareErrorSts":[0]}}]}})
                
    @allure.title("PowerSupplyInfo_参数变化发布_channelErrorSts_errorSts")
    @pytest.mark.sanity 
    def test_caseid_100230(self):
        self.mock.set_signal(UdpChannel.LcuL_Multicast, "PwrChLeErrSwilPwrChLe1Err", 1)
        self.soa.soa_partner.empty_all(0.5)
        for lcul_mul in [127, 0, 8]:
            logger.info({f"设置信号PwrChLeErrSwilPwrChLe1Err{lcul_mul}"})
            self.mock.set_signal(UdpChannel.LcuL_Multicast, "PwrChLeErrSwilPwrChLe1Err", lcul_mul)
            if lcul_mul != 0 :
                self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "PowerSupplyInfo", {"powerSupplyInfo":{"channelStatus":[{"channelErrorSts":{"errorSts":1}}]}})
            else:
                self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "PowerSupplyInfo", {"powerSupplyInfo":{"channelStatus":[{"channelErrorSts":{"errorSts":0}}]}})
                
    @allure.title("PowerSupplyInfo_参数变化发布_channelCurrent(包含超范围)")
    @pytest.mark.sanity 
    def test_caseid_100232(self):
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrChLeCurrValSwilPwrChLe1CurrVal", 20.0)
        logger.info({f"设置信号PwrChLeCurrValSwilPwrChLe1CurrVal发了20"})
        self.soa.soa_partner.empty_all(0.5)
        for lcul_soc in [0.0, 101.0]:
            logger.info({f"设置信号PwrChLeCurrValSwilPwrChLe1CurrVal{lcul_soc}"})
            self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrChLeCurrValSwilPwrChLe1CurrVal", lcul_soc)
            if lcul_soc == 101.0 :
                self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "PowerSupplyInfo", {"powerSupplyInfo":{"channelStatus":[{"channelCurrent":100.00}]}})
            else:
                self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "PowerSupplyInfo", {"powerSupplyInfo":{"channelStatus":[{"channelCurrent":lcul_soc}]}})
                
    @allure.title("ConstantChannelInfo_参数变化发布_左侧")
    @pytest.mark.sanity 
    def test_caseid_100221(self):
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh1CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh2CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh3CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh4CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh5CfgSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        for lcul_soc in [1, 0]:
            logger.info({f"设置信号为{lcul_soc}"})
            self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh1CfgSts", lcul_soc)
            self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh2CfgSts", lcul_soc)
            self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh3CfgSts", lcul_soc)
            self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh4CfgSts", lcul_soc)
            self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh5CfgSts", lcul_soc)
            self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "ConstantChannelInfo", {"constantChannelInfo":{"constantLeftValidity":0, "constantLeftChannel1":{"constantSwitchSts":lcul_soc},
                                                                                      "constantLeftChannel2":{"constantSwitchSts":lcul_soc},
                                                                                      "constantLeftChannel3":{"constantSwitchSts":lcul_soc},
                                                                                      "constantLeftChannel4":{"constantSwitchSts":lcul_soc},
                                                                                      "constantLeftChannel5":{"constantSwitchSts":lcul_soc}}},timeout=2)
            
    @allure.title("ConstantChannelInfo_参数变化发布_右侧")
    @pytest.mark.sanity 
    def test_caseid_100219(self):
        self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh1CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh2CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh3CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh4CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh5CfgSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        for lcur_soc in [1, 0]:
            logger.info({f"设置信号为{lcur_soc}"})
            self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh1CfgSts", lcur_soc)
            self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh2CfgSts", lcur_soc)
            self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh3CfgSts", lcur_soc)
            self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh4CfgSts", lcur_soc)
            self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh5CfgSts", lcur_soc)
            self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "ConstantChannelInfo", {"constantChannelInfo":{"constantRightValidity":0, "constantRightChannel1":{"constantSwitchSts":lcur_soc},
                                                                                      "constantRightChannel2":{"constantSwitchSts":lcur_soc},
                                                                                      "constantRightChannel3":{"constantSwitchSts":lcur_soc},
                                                                                      "constantRightChannel4":{"constantSwitchSts":lcur_soc},
                                                                                      "constantRightChannel5":{"constantSwitchSts":lcur_soc}}},timeout=2)
            
    @allure.title("ConstantChannelInfo_参数变化发布")
    @pytest.mark.sanity 
    def test_caseid_100220(self):
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh1CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh2CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh3CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh4CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh5CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh1CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh2CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh3CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh4CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh5CfgSts", 0)
        self.soa.soa_partner.empty_all(0.5)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh1CfgSts", 1)
        self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh4CfgSts", 1)
        logger.info({f"设置信号为"})
        sleep(0.5)
        self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "ConstantChannelInfo", {"constantChannelInfo":{"constantLeftValidity":0, "constantLeftChannel1":{"constantSwitchSts":1},
                                                                                      "constantLeftChannel2":{"constantSwitchSts":0},
                                                                                      "constantLeftChannel3":{"constantSwitchSts":0},
                                                                                      "constantLeftChannel4":{"constantSwitchSts":0},
                                                                                      "constantLeftChannel5":{"constantSwitchSts":0},
                                        "constantRightValidity":0, "constantRightChannel1":{"constantSwitchSts":0},
                                                                                      "constantRightChannel2":{"constantSwitchSts":0},
                                                                                      "constantRightChannel3":{"constantSwitchSts":0},
                                                                                      "constantRightChannel4":{"constantSwitchSts":1},
                                                                                      "constantRightChannel5":{"constantSwitchSts":0}}},timeout=2)

    @allure.title("GetPowerSupplyInfoByName_参数变化发布_channelErrorSts_softwareErrorSts")
    @pytest.mark.sanity
    def test_caseid_100211(self):
        self.mock.set_signal(UdpChannel.LcuL_Multicast, "PwrChLeErrSwilPwrChLe1Err", 0)
        self.soa.soa_partner.empty_all(0.5)
        for lucl_mul in [8, 127, 128]:
            logger.info({f"设置信号为{lucl_mul}"})
            self.mock.set_signal(UdpChannel.LcuL_Multicast, "PwrChLeErrSwilPwrChLe1Err", lucl_mul)
            if lucl_mul ==127 :
                self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "GetPowerSupplyInfoByName", {"req":{"ecuName":['OPCR']}},{"out":{"channelStatus":[{"channelErrorSts":{"softwareErrorSts":1}}]}})
            else:
                self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "GetPowerSupplyInfoByName", {"req":{"ecuName":['OPCR']}},{"out":{"channelStatus":[{"channelErrorSts":{"softwareErrorSts":0}}]}})
                
    @allure.title("GetPowerSupplyInfoByName_参数变化发布_channelErrorSts_hardwareErrorSts")
    @pytest.mark.sanity
    def test_caseid_100210(self):
        self.mock.set_signal(UdpChannel.LcuL_Multicast, "PwrChLeErrSwilPwrChLe1Err", 0)
        self.soa.soa_partner.empty_all(0.5)
        for lucl_mul in [1,62,255,128]:
            logger.info({f"设置信号为{lucl_mul}"})
            self.mock.set_signal(UdpChannel.LcuL_Multicast, "PwrChLeErrSwilPwrChLe1Err", lucl_mul)
            if lucl_mul == 62:
                self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "GetPowerSupplyInfoByName", {"req":{"ecuName":['OPCR']}},{"out":{"channelStatus":[{"channelErrorSts":{"hardwareErrorSts":[2,3,4,5,6]}}]}})
            elif lucl_mul ==255:
                self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "GetPowerSupplyInfoByName", {"req":{"ecuName":['OPCR']}},{"out":{"channelStatus":[{"channelErrorSts":{"hardwareErrorSts":[1,2,3,4,5,6]}}]}})
            elif lucl_mul ==1:
                self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "GetPowerSupplyInfoByName", {"req":{"ecuName":['OPCR']}},{"out":{"channelStatus":[{"channelErrorSts":{"hardwareErrorSts":[1]}}]}})
            else:
                self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "GetPowerSupplyInfoByName", {"req":{"ecuName":['OPCR']}},{"out":{"channelStatus":[{"channelErrorSts":{"hardwareErrorSts":[0]}}]}})
                
    @allure.title("GetPowerSupplyInfoByName_参数变化发布_powerSupplyStatus")
    @pytest.mark.sanity
    def test_caseid_100209(self):
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "LoadPwrActStsOPCRPwrActSts", 1)
        self.soa.soa_partner.empty_all(0.5)
        for mcu_soc in range(2):
            logger.info({f"设置信号为{mcu_soc}"})
            self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "LoadPwrActStsOPCRPwrActSts", mcu_soc)
            self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "GetPowerSupplyInfoByName", {"req":{"ecuName":['OPCR']}},{"out":{"channelStatus":[{"powerSupplyStatus":[{"validity":0,"ecuName":"OPCR","lvECUSts":mcu_soc}]}]}})
            
    @allure.title("GetPowerSupplyInfoByName_不存在ecu名称")
    @pytest.mark.full
    def test_caseid_100214(self):
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "GetPowerSupplyInfoByName", {"req":{"ecuName":['ABC']}},{"out":{"channelStatus":[]}})
        
    @allure.title("GetPowerSupplyInfoByName_启动场景_获取到部分参数状态信息")
    @pytest.mark.full
    def test_caseid_100215(self):
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_CCUSOCCD, 0x50400A)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_Multicast, 0x50FF01)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuR_CCUSOCCD, 0x604002)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuR_Multicast, 0x60FF01)
        self.ssh.rerun_car_service()
        self.soa.empty_all(0.5) 
        self.soa.wait_for_service_reconnect(POWERSUPPLY_SERVICE_CLIENT)
        sleep(1.5)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "LoadPwrActStsOPCRPwrActSts", 0)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "GetPowerSupplyInfoByName", {"req":{"ecuName":['OPCR']}},{"out":{"channelStatus":[{"channelAreaSts":255,"channelNumber":255,"validity":0,"channelCurrent":-1.0,"channelSwitchSts":255,
                                                                                                                                                        "channelErrorSts":{"errorSts":255,"softwareErrorSts":255,"hardwareErrorSts":[]},
                                                                                                                                                        "ecuNameList":["OPCR"],"ecuAmount":1,
                                                                                                                                                        "powerSupplyStatus":[{"validity":0,"ecuName":"OPCR","lvECUSts":0}]}]}})
           
    @allure.title("GetPowerSupplyInfoByName_启动场景_未获取到任意参数状态信息")
    @pytest.mark.full
    def test_caseid_100216(self):
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_CCUSOCCD, 0x50400A)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_Multicast, 0x50FF01)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuR_CCUSOCCD, 0x604002)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuR_Multicast, 0x60FF01)
        self.mock.stop_send_cycle_pdu(UdpChannel.CCUMCUCD_Multicast, 0x20FF03)
        self.ssh.rerun_car_service()
        self.soa.empty_all(0.5) 
        self.soa.wait_for_service_reconnect(POWERSUPPLY_SERVICE_CLIENT)
        sleep(1.5)
        self.mock.set_signal(UdpChannel.CCUMCUCD_Multicast, "LoadPwrActStsOPCRPwrActSts", 0)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "GetPowerSupplyInfoByName", {"req":{"ecuName":['ABC']}},{"out":{"channelStatus":[{"channelAreaSts":255,"channelNumber":255,"validity":1,"channelCurrent":255,"channelSwitchSts":255,
                                                                                                                                                        "channelErrorSts":{"errorSts":255,"softwareErrorSts":255,"hardwareErrorSts":[255]},
                                                                                                                                                        "ecuNameList":["OPCR"],"ecuAmount":1,
                                                                                                                                                        "powerSupplyStatus":[{"validity":1,"ecuName":"","lvECUSts":255}]}]}})
        
    @allure.title("CConstantChannelInfo_ValidityLevel=4_停单帧不影响其他帧上信号映射")
    @pytest.mark.full
    def test_caseid_100217(self):
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh1CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh1CfgSts", 0)
        self.soa.empty_all(0.5)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh1CfgSts", 1)
        self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "ConstantChannelInfo", {"constantChannelInfo":{"constantLeftValidity":0, "constantLeftChannel1":{"constantSwitchSts":1},
                                                                                                "constantRightValidity":0,"constantRightChannel1":{"constantSwitchSts":0}}})
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_CCUSOCCD, 0x504003)
        sleep(2)
        logger.info({f"停发左侧"})
        self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "ConstantChannelInfo", {"constantChannelInfo":{"constantLeftValidity":4, "constantLeftChannel1":{"constantSwitchSts":1},
                                                                                                "constantRightValidity":0,"constantRightChannel1":{"constantSwitchSts":0}}})
        self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh1CfgSts", 1)
        self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "ConstantChannelInfo", {"constantChannelInfo":{"constantLeftValidity":4, "constantLeftChannel1":{"constantSwitchSts":1},
                                                                                                "constantRightValidity":0,"constantRightChannel1":{"constantSwitchSts":1}}})
        self.mock.resume_send_cycle_pdu(UdpChannel.LcuL_CCUSOCCD, 0x504003)
        self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "ConstantChannelInfo", {"constantChannelInfo":{"constantLeftValidity":0, "constantLeftChannel1":{"constantSwitchSts":1},
                                                                                                "constantRightValidity":0,"constantRightChannel1":{"constantSwitchSts":1}}})
        
    @allure.title("CConstantChannelInfo_ValidityLevel=4_停单帧不影响其他帧上信号映射")
    @pytest.mark.full
    def test_caseid_100218(self):
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh1CfgSts", 0)
        self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh1CfgSts", 0)
        self.soa.empty_all(0.5)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh1CfgSts", 1)
        sleep(0.1)
        self.mock.set_signal(UdpChannel.LcuR_CCUSOCCD, "PwrContnsChRiCfgStsContnsRiCh1CfgSts", 1)
        self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "ConstantChannelInfo", {"constantChannelInfo":{"constantLeftValidity":0, "constantLeftChannel1":{"constantSwitchSts":1},
                                                                                                "constantRightValidity":0,"constantRightChannel1":{"constantSwitchSts":1}}})
    
    @allure.title("ConstantChannelInfo_启动场景_未获取到任意参数状态信息")
    @pytest.mark.full
    def test_caseid_100222(self):
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_CCUSOCCD, 0x504003)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuR_CCUSOCCD, 0x604004)
        self.ssh.rerun_car_service()
        self.soa.empty_all(0.5) 
        self.soa.wait_for_service_reconnect(VEHICLE_MODE_SERVICE_CLIENT)
        sleep(1.5)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "GetConstantChannelInfoAsync",{},{"out":{"constantLeftValidity":1, "constantLeftChannel1":{"constantSwitchSts":255},
                                                                                      "constantLeftChannel2":{"constantSwitchSts":255},
                                                                                      "constantLeftChannel3":{"constantSwitchSts":255},
                                                                                      "constantLeftChannel4":{"constantSwitchSts":255},
                                                                                      "constantLeftChannel5":{"constantSwitchSts":255},
                                        "constantRightValidity":1, "constantRightChannel1":{"constantSwitchSts":255},
                                                                                      "constantRightChannel2":{"constantSwitchSts":255},
                                                                                      "constantRightChannel3":{"constantSwitchSts":255},
                                                                                      "constantRightChannel4":{"constantSwitchSts":255},
                                                                                      "constantRightChannel5":{"constantSwitchSts":255}}})
        
    @allure.title("ConstantChannelInfo_ValidityLevel_value1到4")
    @pytest.mark.full
    def test_caseid_100223(self):
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuL_CCUSOCCD, 0x504003)
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuR_CCUSOCCD, 0x604004)
        self.ssh.rerun_car_service()
        self.soa.empty_all(0.5) 
        self.soa.wait_for_service_reconnect(POWERSUPPLY_SERVICE_CLIENT)
        sleep(1.5)
        self.soa.send_request_and_ck_resp(POWERSUPPLY_SERVICE_CLIENT, "GetConstantChannelInfoAsync",{},{"out":{"constantLeftValidity":1,"constantRightValidity":1}})
        self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "ConstantChannelInfo", {"constantChannelInfo":{"constantLeftValidity":4,"constantRightValidity":4}},timeout = 2)
        
    @allure.title("ConstantChannelInfo_启动场景_获取到部分参数状态信息")
    @pytest.mark.full
    def test_caseid_100224(self):
        self.mock.stop_send_cycle_pdu(UdpChannel.LcuR_CCUSOCCD, 0x604004)
        self.mock.set_signal(UdpChannel.LcuL_CCUSOCCD, "PwrContnsChLeCfgStsContnsLeCh1CfgSts", 0)
        self.ssh.rerun_car_service()
        self.soa.empty_all(0.5) 
        self.soa.wait_for_service_reconnect(VEHICLE_MODE_SERVICE_CLIENT)
        sleep(1.5)
        self.soa.ck_field(POWERSUPPLY_SERVICE_CLIENT, "ConstantChannelInfo",{"constantChannelInfo":{"constantLeftValidity":0, "constantLeftChannel1":{"constantSwitchSts":0},
                                                                                      "constantLeftChannel2":{"constantSwitchSts":0},
                                                                                      "constantLeftChannel3":{"constantSwitchSts":0},
                                                                                      "constantLeftChannel4":{"constantSwitchSts":0},
                                                                                      "constantLeftChannel5":{"constantSwitchSts":0},
                                                        "constantRightValidity":1, "constantRightChannel1":{"constantSwitchSts":255},
                                                                                      "constantRightChannel2":{"constantSwitchSts":255},
                                                                                      "constantRightChannel3":{"constantSwitchSts":255},
                                                                                      "constantRightChannel4":{"constantSwitchSts":255},
                                                                                      "constantRightChannel5":{"constantSwitchSts":255}}})    