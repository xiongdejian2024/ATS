#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_demo.py
@Time         :2024/10/23 13:57
@Author       :dejian.xiong@jiduauto.com
@Description  :
"""
import pytest
from xat_cases.dp2.cd_service.case_helper.test_sil_abc_base import *
from xat_ecu.legacy.soa_partner.src.partner_const_dp2 import CHARGELID_SERVICE_CLIENT, VEHICLE_MODE_SERVICE_CLIENT, \
    CENTRAL_LOCK_SERVICE_CLIENT


class TestDemo(TestSILAbcBase):
    def before_class(self, ecu: EcuInfo):
        super().before_class(self, ecu)
        logger.info("before_class")
        self.ssh.service_sil_test_preparation()
        self.soa.update([CHARGELID_SERVICE_CLIENT, VEHICLE_MODE_SERVICE_CLIENT, CENTRAL_LOCK_SERVICE_CLIENT])
        self.mock.update_channel({
            # UdpChannel.CCUMCUAD_Multicast: None,
            # UdpChannel.CCUMCUCD_Multicast: None,
            # UdpChannel.LcuL_Multicast: None,
            # UdpChannel.LcuR_Multicast: None,
            # UdpChannel.CCUMCUAD_CCUSOCCD: None,
            # UdpChannel.CCUMCUCD_CCUSOCCD: None,
            UdpChannel.LcuL_CCUSOCCD: None,
            # UdpChannel.LcuR_CCUSOCCD: None,
            TcpChannel.CdMcuTCPServer_CdSocTCPClient1: None,
            # TcpChannel.LcuLTCPServer_CdSocTCPClient3: None,
            # TcpChannel.LcuRTCPServer_CdSocTCPClient4: None,
            # TcpChannel.AdMcuTCPServer_CdSocTCPClient2: None,
        })
        self.mock.resume_send_all_cycle_pdu()

    def before_each_func(self, ecu: EcuInfo):
        super().before_each_func(ecu)
        logger.info("before_each_func")

    def after_each_func(self, ecu: EcuInfo):
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu: EcuInfo):
        super().after_class(self, ecu)
        logger.info("after_class")
    
    def test_caseid_100013(self):
        self.ssh.is_process_running("log_j")
        self.ssh.rerun_car_service()
        sleep(10)

    @pytest.mark.full
    def test_caseid_1983974(self):
        print(123)
        self.soa.wait_for_service_reconnect(CHARGELID_SERVICE_CLIENT)
        sleep(1)
        for cmd in [0, 1, 0, 1]:
            self.soa.send_method_request(CHARGELID_SERVICE_CLIENT, "SetChargeLidMoveCtrl",
                                         {"moveCmd": {"moveDirectionCmd": cmd}})
            sleep(2)
        self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, "NormChargeLidMoveCtrl")

        for i in range(5):
            self.mock.set_signal(UdpChannel.LcuL_Multicast, "ChargeLidMoveSts", i)
            sleep(0.2)

    @allure.title("ChargeLidMoveInfo_参数变化发布")
    @pytest.mark.sanity
    def test_caseid_100004(self):
        self.mock.set_signal(UdpChannel.LcuL_Multicast, "ChargeLidMoveSts", 0)
        sleep(1)
        for sts in [1, 2, 3, 4, 5, 0]:
            logger.info(f"sts=={sts}")
            self.mock.set_signal(UdpChannel.LcuL_Multicast, "ChargeLidMoveSts", sts)
            if sts != 5:
                self.soa.ck_field(CHARGELID_SERVICE_CLIENT, "ChargeLidMoveInfo",
                                  {"moveInfo": {"moveSts": sts, "validity": 0}})

    @allure.title("SetCarModeCtrl_下行pdu校验")
    @pytest.mark.sanity
    def test_caseid_100208(self):
        self.soa.send_method_request(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl", {"carModeCtrlCmd": {"carMode": 1}})
        self.soa.soa_partner.empty_all(0.5)
        for carmode in range(3):
            self.soa.send_request_and_ck_resp(VEHICLE_MODE_SERVICE_CLIENT, "SetCarModeCtrl",
                                              {"carModeCtrlCmd": {"carMode": carmode}}, {"out": 0})
            sleep(1)
        result = self.mock.get_signal_values(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, "SetCarModProxyReq")
        logger.info(f"a =={result}")

    def test_caseid_100012(self):
        self.soa.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "SetChargeLidMoveCtrl", {"moveCmd": {"moveDirectionCmd": 0}},
                                              {"out":0}) 
        sleep(0.06)
        self.soa.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "SetChargeLidMoveCtrl", {"moveCmd": {"moveDirectionCmd": 1}},
                                              {"out":0})
        sleep(0.06)
        self.soa.send_request_and_ck_resp(CHARGELID_SERVICE_CLIENT, "SetChargeLidMoveCtrl", {"moveCmd": {"moveDirectionCmd": 1}},
                                              {"out":0})
        sleep(1)
        self.mock.ck_ordered_array(TcpChannel.CdMcuTCPServer_CdSocTCPClient1, "NormChargeLidMoveCtrl",[0,1,2,0])
