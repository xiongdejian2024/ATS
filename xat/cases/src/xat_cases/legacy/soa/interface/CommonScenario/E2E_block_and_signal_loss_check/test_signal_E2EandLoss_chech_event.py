# -*- coding: utf-8 -*-

"""
@Time    : 2024/06/25 08:55
@Author  : lei.tao
@Email   : lei.tao@jiduauto.com
"""
import time
import pytest
import allure
from xat_ecu.legacy.common.data_type_handing import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import S2sBaseClass
from xat_ecu.legacy.soa_partner.src.partner_const import *


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/E2E故障&信号丢失校验event事件场景")
class TestChassisServiceSignalE2EAndLoss(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("ChassisService", "client")])
        self.partner_key = "ChassisService" + "_client"
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr40, "WhlSpdCircumlFrntLeQf", 3
        )  # 前置 故障列表没有 3
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr40, "WhlSpdCircumlFrntRiQf", 3
        )  # 前置 故障列表没有 4
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr40, "WhlSpdCircumlReLeQf", 3
        )  # 前置 故障列表没有 5
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr40, "WhlSpdCircumlReRiQf", 3
        )  # 前置 故障列表没有 6
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr06, "VehSpdLgtQf", 3
        )  # 前置 故障列表没有 1，2
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00, "VehMtnStVehMtnSt", 4
        )  # 前置 故障列表没有 15
        time.sleep(15)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        self.partner.empty_all()
        # 防止报错造成总线恢复失败
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)

    @allure.title(
        "ChassisService::ChassisFault_VehMtnStChks::BackboneFR::55-0-1信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987573(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "55-0-1")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehMtnSt")
            self.partner.ck_s2s_event(
                self.partner_key, "ChassisFault", {"faults": [15]}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(1)
            self.partner.ck_no_event(self.partner_key, "ChassisFault")
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "ChassisFault")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehMtnSt")
            self.partner.ck_s2s_event(
                self.partner_key, "ChassisFault", {"faults": [0]}, timeout=3
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehMtnSt")
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::ChassisFault_WhlRotToothCntrChks::BackboneFR::51-0-2信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987572(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "51-0-2")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlRotToothCntr"
            )
            self.partner.ck_s2s_event(
                self.partner_key, "ChassisFault", {"faults": [7, 8, 9, 10]}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(1)
            self.partner.ck_s2s_event(
                self.partner_key, "ChassisFault", {"faults": [3, 4, 5, 6, 7, 8, 9, 10]}
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.ck_s2s_event(
                self.partner_key, "ChassisFault", {"faults": [7, 8, 9, 10]}
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlRotToothCntr"
            )
            self.partner.ck_s2s_event(
                self.partner_key, "ChassisFault", {"faults": [0]}, timeout=3
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlRotToothCntr"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::ChassisFault_WhlSpdCircumlFrntChks::BackboneFR::51-0-2信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987571(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "51-0-2")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlFrnt"
            )
            self.partner.ck_s2s_event(
                self.partner_key, "ChassisFault", {"faults": [3, 4]}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(1)
            self.partner.ck_s2s_event(
                self.partner_key, "ChassisFault", {"faults": [3, 4, 5, 6, 7, 8, 9, 10]}
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.ck_s2s_event(
                self.partner_key, "ChassisFault", {"faults": [3, 4]}
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlFrnt"
            )
            self.partner.ck_s2s_event(
                self.partner_key, "ChassisFault", {"faults": [0]}, timeout=3
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlFrnt"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::ChassisFault_WhlSpdCircumlReChks::BackboneFR::51-0-2信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987570(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "51-0-2")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlRe"
            )
            self.partner.ck_s2s_event(
                self.partner_key, "ChassisFault", {"faults": [5, 6]}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(1)
            self.partner.ck_s2s_event(
                self.partner_key, "ChassisFault", {"faults": [3, 4, 5, 6, 7, 8, 9, 10]}
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.ck_s2s_event(
                self.partner_key, "ChassisFault", {"faults": [5, 6]}
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlRe"
            )
            self.partner.ck_s2s_event(
                self.partner_key, "ChassisFault", {"faults": [0]}, timeout=3
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlRe"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::epbDisplayReqSts_EpbLampReqChks::BackboneFR::57-23-64信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987569(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "57-23-64")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReq")
            self.partner.ck_s2s_event(
                self.partner_key,
                "epbDisplayReqSts",
                {"sts": {"highPriSts": 5, "lowPriSts": 5}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.ck_no_event(self.partner_key, "epbDisplayReqSts")
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "epbDisplayReqSts")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReq")
            self.partner.ck_s2s_event(
                self.partner_key,
                "epbDisplayReqSts",
                {"sts": {"highPriSts": 0, "lowPriSts": 0}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReq")
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::epbDisplayReqSts_EpbLampReqSecChks::BackboneFR::7-8-64信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987568(self):
        self.ipdu.set(
            self.ipdu.backbonefr.CemBackBoneFr02, "VehModMngtGlbSafe1UsgModSts", 2
        )
        msg_id = self.ipdu.get_signal_message("backbonefr", "7-8-64")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReqSec"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "epbDisplayReqSts",
                {"sts": {"highPriSts": 5, "lowPriSts": 5}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.ck_no_event(self.partner_key, "epbDisplayReqSts")
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "epbDisplayReqSts")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReqSec"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "epbDisplayReqSts",
                {"sts": {"highPriSts": 0, "lowPriSts": 0}},
                timeout=3,
            )
            self.ipdu.set(
                self.ipdu.backbonefr.CemBackBoneFr02, "VehModMngtGlbSafe1UsgModSts", 1
            )  # 恢复信号
        except Exception as e:
            self.ipdu.set(
                self.ipdu.backbonefr.CemBackBoneFr02, "VehModMngtGlbSafe1UsgModSts", 1
            )  # 恢复信号
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReqSec"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::epbIndicatorLightReqStsValidity_EpbLampReqChks::BackboneFR::57-23-64信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987567(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "57-23-64")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReq")
            self.partner.ck_s2s_event(
                self.partner_key,
                "epbIndicatorLightReqStsValidity",
                {"sts": {"value": 1, "validity": 7}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.ck_no_event(
                self.partner_key, "epbIndicatorLightReqStsValidity"
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.ck_no_event(
                self.partner_key, "epbIndicatorLightReqStsValidity"
            )
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReq")
            self.partner.ck_s2s_event(
                self.partner_key,
                "epbIndicatorLightReqStsValidity",
                {"sts": {"value": 1, "validity": 0}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReq")
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::epbIndicatorLightReqStsValidity_EpbLampReqSecChks::BackboneFR::7-8-64信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987566(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "7-8-64")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReqSec"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "epbIndicatorLightReqStsValidity",
                {"sts": {"value": 1, "validity": 7}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.ck_no_event(
                self.partner_key, "epbIndicatorLightReqStsValidity"
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.ck_no_event(
                self.partner_key, "epbIndicatorLightReqStsValidity"
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReqSec"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "epbIndicatorLightReqStsValidity",
                {"sts": {"value": 1, "validity": 0}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReqSec"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::escOffIndicateLightSts_DrvModEscOffChks::BackboneFR::57-23-64信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987565(self):
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr39, "DrvModEscOffDrvModEscOff", 0
        )
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, "EscStEscSt", 1)
        self.partner.send_request_and_ck_resp(
            CHASSIS_SERVICE_CLIENT,
            "getESCOffIndicateLightSts",
            {},
            {"out": 0},
            timeout=3,
        )
        msg_id = self.ipdu.get_signal_message("backbonefr", "57-23-64")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "DrvModEscOff")
            self.partner.ck_s2s_event(
                self.partner_key, "escOffIndicateLightSts", {"sts": 1}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.ck_no_event(self.partner_key, "escOffIndicateLightSts")
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "escOffIndicateLightSts")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "DrvModEscOff"
            )
            self.partner.ck_s2s_event(
                self.partner_key, "escOffIndicateLightSts", {"sts": 0}, timeout=3
            )
            self.ipdu.set(
                self.ipdu.backbonefr.BcmVddmBackBoneFr39, "DrvModEscOffDrvModEscOff", 0
            )  # 恢复信号
            self.ipdu.set(
                self.ipdu.backbonefr.BcmVddmBackBoneFr03, "EscStEscSt", 0
            )  # 恢复信号
        except Exception as e:
            self.ipdu.set(
                self.ipdu.backbonefr.BcmVddmBackBoneFr39, "DrvModEscOffDrvModEscOff", 0
            )  # 恢复信号
            self.ipdu.set(
                self.ipdu.backbonefr.BcmVddmBackBoneFr03, "EscStEscSt", 0
            )  # 恢复信号
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "DrvModEscOff"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::escOffIndicateLightSts_EscStChks::BackboneFR::56-1-2信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987564(self):
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr39, "DrvModEscOffDrvModEscOff", 0
        )
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, "EscStEscSt", 1)
        msg_id = self.ipdu.get_signal_message("backbonefr", "56-1-2")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EscSt")
            self.partner.ck_s2s_event(
                self.partner_key, "escOffIndicateLightSts", {"sts": 1}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.ck_no_event(self.partner_key, "escOffIndicateLightSts")
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "escOffIndicateLightSts")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EscSt")
            self.partner.ck_s2s_event(
                self.partner_key, "escOffIndicateLightSts", {"sts": 0}, timeout=3
            )
            self.ipdu.set(
                self.ipdu.backbonefr.BcmVddmBackBoneFr39, "DrvModEscOffDrvModEscOff", 0
            )  # 恢复信号
            self.ipdu.set(
                self.ipdu.backbonefr.BcmVddmBackBoneFr03, "EscStEscSt", 0
            )  # 恢复信号
        except Exception as e:
            self.ipdu.set(
                self.ipdu.backbonefr.BcmVddmBackBoneFr39, "DrvModEscOffDrvModEscOff", 0
            )  # 恢复信号
            self.ipdu.set(
                self.ipdu.backbonefr.BcmVddmBackBoneFr03, "EscStEscSt", 0
            )  # 恢复信号
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EscSt")
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::ESCWorkStatus_EscStChks::BackboneFR::56-1-2信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987563(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr03, "EscStEscSt", 0)
        msg_id = self.ipdu.get_signal_message("backbonefr", "56-1-2")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EscSt")
            self.partner.ck_s2s_event(
                self.partner_key, "ESCWorkStatus", {"state": 2}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.ck_no_event(self.partner_key, "ESCWorkStatus")
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "ESCWorkStatus")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EscSt")
            self.partner.ck_s2s_event(
                self.partner_key, "ESCWorkStatus", {"state": 0}, timeout=3
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EscSt")
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::Gear_TrsmParkLockdChks::PropulsionCAN::0x155信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987562(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, "GearLvrIndcn", 0)
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropComFr10, "TrsmParkLockdTrsmParkLockd", 0
        )
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x155")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "TrsmParkLockd"
            )
            self.partner.ck_s2s_event(self.partner_key, "Gear", {"gear": 5}, timeout=3)
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("propulsioncan", f"{msg_id}")
            time.sleep(1)
            self.partner.ck_no_event(self.partner_key, "Gear")
            self.ipdu.resume_send_pdu("propulsioncan", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "Gear")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "TrsmParkLockd"
            )
            self.partner.ck_s2s_event(self.partner_key, "Gear", {"gear": 0}, timeout=3)
        except Exception as e:
            self.ipdu.resume_send_pdu("propulsioncan", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "TrsmParkLockd"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::getABSWarnIndicateReqSts_BrkAndAbsWarnIndcnReqChks::BackboneFR::57-23-64信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987561(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "57-23-64")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "BrkAndAbsWarnIndcnReq"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getABSWarnIndicateReqSts", {}, {"out": 1}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getABSWarnIndicateReqSts", {}, {"out": 1}
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getABSWarnIndicateReqSts", {}, {"out": 1}
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "BrkAndAbsWarnIndcnReq"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getABSWarnIndicateReqSts", {}, {"out": 1}, timeout=3
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "BrkAndAbsWarnIndcnReq"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::getBrkSysWarnIndicateReqSts_EpbLampReqChks::BackboneFR::57-23-64信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987560(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "57-23-64")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReq")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getBrkSysWarnIndicateReqSts",
                {},
                {"out": 1},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getBrkSysWarnIndicateReqSts", {}, {"out": 2}
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getBrkSysWarnIndicateReqSts", {}, {"out": 1}
            )
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReq")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getBrkSysWarnIndicateReqSts",
                {},
                {"out": 1},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReq")
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::getBrkSysWarnIndicateReqSts_EpbLampReqSecChks::BackboneFR::7-8-64信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987559(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, "BrkFldLvl", 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, "BrkSysWarnIndcnReq", 1)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, "BrkSysWarnIndcnReqSec", 1)
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr39,
            "BrkAndAbsWarnIndcnReqBrkWarnIndcnReq",
            1,
        )
        time.sleep(5)
        self.partner.send_request_and_ck_resp(
            self.partner_key, "getBrkSysWarnIndicateReqSts", {}, {"out": 0}, timeout=3
        )
        msg_id = self.ipdu.get_signal_message("backbonefr", "7-8-64")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReqSec"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getBrkSysWarnIndicateReqSts",
                {},
                {"out": 1},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getBrkSysWarnIndicateReqSts", {}, {"out": 1}
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getBrkSysWarnIndicateReqSts", {}, {"out": 1}
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReqSec"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getBrkSysWarnIndicateReqSts",
                {},
                {"out": 0},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReqSec"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::GetChassisFault_VehMtnStChks::BackboneFR::55-0-1信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987558(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "55-0-1")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehMtnSt")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetChassisFault", {}, {"out": [15]}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(1)
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetChassisFault", {}, {"out": [15]}
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetChassisFault", {}, {"out": [15]}
            )
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehMtnSt")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetChassisFault", {}, {"out": [0]}, timeout=3
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehMtnSt")
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::GetChassisFault_VehSpdLgtChks::BackboneFR::57-0-4信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987557(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "57-0-4")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehSpdLgt")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetChassisFault", {}, {"out": [1]}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(1)
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetChassisFault", {}, {"out": [1]}
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetChassisFault", {}, {"out": [1]}
            )
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehSpdLgt")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetChassisFault", {}, {"out": [0]}, timeout=3
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehSpdLgt")
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::GetChassisFault_WhlRotToothCntrChks::BackboneFR::51-0-2信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987556(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "51-0-2")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlRotToothCntr"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetChassisFault",
                {},
                {"out": [7, 8, 9, 10]},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(1)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetChassisFault",
                {},
                {"out": [3, 4, 5, 6, 7, 8, 9, 10]},
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetChassisFault", {}, {"out": [7, 8, 9, 10]}
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlRotToothCntr"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetChassisFault", {}, {"out": [0]}, timeout=3
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlRotToothCntr"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::GetChassisFault_WhlSpdCircumlFrntChks::BackboneFR::51-0-2信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987555(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "51-0-2")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlFrnt"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetChassisFault", {}, {"out": [3, 4]}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(1)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetChassisFault",
                {},
                {"out": [3, 4, 5, 6, 7, 8, 9, 10]},
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetChassisFault", {}, {"out": [3, 4]}
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlFrnt"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetChassisFault", {}, {"out": [0]}, timeout=3
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlFrnt"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::GetChassisFault_WhlSpdCircumlReChks::BackboneFR::51-0-2信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987554(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "51-0-2")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlRe"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetChassisFault", {}, {"out": [5, 6]}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(1)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetChassisFault",
                {},
                {"out": [3, 4, 5, 6, 7, 8, 9, 10]},
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetChassisFault", {}, {"out": [5, 6]}
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlRe"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetChassisFault", {}, {"out": [0]}, timeout=3
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlRe"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::getDisplayReqSts_EpbLampReqSecChks::BackboneFR::7-8-64信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987553(self):
        self.ipdu.set(
            self.ipdu.backbonefr.CemBackBoneFr02, "VehModMngtGlbSafe1UsgModSts", 2
        )
        msg_id = self.ipdu.get_signal_message("backbonefr", "7-8-64")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReqSec"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getDisplayReqSts",
                {},
                {"out": {"highPriSts": 5, "lowPriSts": 5}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getDisplayReqSts",
                {},
                {"out": {"highPriSts": 5, "lowPriSts": 5}},
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getDisplayReqSts",
                {},
                {"out": {"highPriSts": 5, "lowPriSts": 5}},
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReqSec"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getDisplayReqSts",
                {},
                {"out": {"highPriSts": 0, "lowPriSts": 0}},
                timeout=3,
            )
            self.ipdu.set(
                self.ipdu.backbonefr.CemBackBoneFr02, "VehModMngtGlbSafe1UsgModSts", 1
            )  # 恢复信号
        except Exception as e:
            self.ipdu.set(
                self.ipdu.backbonefr.CemBackBoneFr02, "VehModMngtGlbSafe1UsgModSts", 1
            )  # 恢复信号
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReqSec"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::getESCOffIndicateLightSts_DrvModEscOffChks::BackboneFR::57-23-64信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987552(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "57-23-64")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "DrvModEscOff")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getESCOffIndicateLightSts", {}, {"out": 1}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getESCOffIndicateLightSts", {}, {"out": 1}
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getESCOffIndicateLightSts", {}, {"out": 1}
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "DrvModEscOff"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getESCOffIndicateLightSts", {}, {"out": 1}, timeout=3
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "DrvModEscOff"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::getESCOffIndicateLightSts_EscStChks::BackboneFR::56-1-2信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987551(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "56-1-2")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EscSt")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getESCOffIndicateLightSts", {}, {"out": 1}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getESCOffIndicateLightSts", {}, {"out": 1}
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getESCOffIndicateLightSts", {}, {"out": 1}
            )
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EscSt")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getESCOffIndicateLightSts", {}, {"out": 1}, timeout=3
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EscSt")
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::getESCWarnIndicateReqSts_EscWarnIndcnReqChks::BackboneFR::57-5-8信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987550(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "57-5-8")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EscWarnIndcnReq"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getESCWarnIndicateReqSts", {}, {"out": 0}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getESCWarnIndicateReqSts", {}, {"out": 0}
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getESCWarnIndicateReqSts", {}, {"out": 0}
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EscWarnIndcnReq"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key, "getESCWarnIndicateReqSts", {}, {"out": 0}, timeout=3
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EscWarnIndcnReq"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::GetESCWorkStatus_EscStChks::BackboneFR::56-1-2信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987549(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "56-1-2")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EscSt")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetESCWorkStatus", {}, {"out": 2}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetESCWorkStatus", {}, {"out": 2}
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetESCWorkStatus", {}, {"out": 2}
            )
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EscSt")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetESCWorkStatus", {}, {"out": 0}, timeout=3
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EscSt")
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::GetGear_TrsmParkLockdChks::PropulsionCAN::0x155信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987548(self):
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, "GearLvrIndcn", 0)
        self.ipdu.set(
            self.ipdu.propulsioncan.EcmPropComFr10, "TrsmParkLockdTrsmParkLockd", 0
        )
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x155")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "TrsmParkLockd"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetGear", {}, {"out": 5}, timeout=3
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("propulsioncan", f"{msg_id}")
            time.sleep(1)
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetGear", {}, {"out": 5}
            )
            self.ipdu.resume_send_pdu("propulsioncan", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetGear", {}, {"out": 5}
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "TrsmParkLockd"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetGear", {}, {"out": 0}, timeout=3
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("propulsioncan", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "TrsmParkLockd"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::getIndicatorLightReqStsValidity_EpbLampReqChks::BackboneFR::57-23-64信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987545(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "57-23-64")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReq")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getIndicatorLightReqStsValidity",
                {},
                {"out": {"value": 1, "validity": 7}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getIndicatorLightReqStsValidity",
                {},
                {"out": {"value": 1, "validity": 7}},
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getIndicatorLightReqStsValidity",
                {},
                {"out": {"value": 1, "validity": 7}},
            )
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReq")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getIndicatorLightReqStsValidity",
                {},
                {"out": {"value": 1, "validity": 0}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReq")
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::getIndicatorLightReqStsValidity_EpbLampReqSecChks::BackboneFR::7-8-64信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987544(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "7-8-64")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReqSec"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getIndicatorLightReqStsValidity",
                {},
                {"out": {"value": 1, "validity": 7}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getIndicatorLightReqStsValidity",
                {},
                {"out": {"value": 1, "validity": 7}},
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getIndicatorLightReqStsValidity",
                {},
                {"out": {"value": 1, "validity": 7}},
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReqSec"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getIndicatorLightReqStsValidity",
                {},
                {"out": {"value": 1, "validity": 0}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "EpbLampReqSec"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::GetSpeed_VehSpdLgtChks::BackboneFR::57-0-4信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987543(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "57-0-4")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehSpdLgt")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetSpeed",
                {},
                {"out": {"speed": 0, "isvalid": 0}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(1)
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetSpeed", {}, {"out": {"speed": 0, "isvalid": 0}}
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key, "GetSpeed", {}, {"out": {"speed": 0, "isvalid": 0}}
            )
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehSpdLgt")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetSpeed",
                {},
                {"out": {"speed": 0, "isvalid": 0}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehSpdLgt")
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::GetVehicleMotionState_VehMtnStChks::BackboneFR::55-0-1信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987542(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "55-0-1")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehMtnSt")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetVehicleMotionState",
                {},
                {"out": {"isvalid": False}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(1)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetVehicleMotionState",
                {},
                {"out": {"isvalid": False}},
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetVehicleMotionState",
                {},
                {"out": {"isvalid": False}},
            )
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehMtnSt")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetVehicleMotionState",
                {},
                {"out": {"isvalid": True}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehMtnSt")
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::GetVehicleStandStillSts_StandStillMgrStsForHldChks::ChassisCAN1::0x1F0信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987541(self):
        self.ipdu.set(self.ipdu.chassiscan1.VddmChas1Fr53, "StandStillMgrStsForHld1", 0)
        self.partner.send_request_and_ck_resp(
            CHASSIS_SERVICE_CLIENT, "GetVehicleStandStillSts", {}, {"out": {"value": 0}}
        )
        msg_id = self.ipdu.get_signal_message("chassiscan1", "0x1F0")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "StandStillMgrStsForHld"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetVehicleStandStillSts",
                {},
                {"out": {"value": 0, "validity": 7}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("chassiscan1", f"{msg_id}")
            time.sleep(2)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetVehicleStandStillSts",
                {},
                {"out": {"value": 0, "validity": 7}},
            )
            self.ipdu.resume_send_pdu("chassiscan1", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetVehicleStandStillSts",
                {},
                {"out": {"value": 0, "validity": 7}},
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "StandStillMgrStsForHld"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetVehicleStandStillSts",
                {},
                {"out": {"value": 0, "validity": 0}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("chassiscan1", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "StandStillMgrStsForHld"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::GetWheelImpluseCounter_WhlRotToothCntrChks::BackboneFR::51-0-2信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987540(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "51-0-2")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlRotToothCntr"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetWheelImpluseCounter",
                {"wheels": [1, 2, 3, 4]},
                {
                    "out": [
                        {"wheelId": 1, "wheelImpluseCounter": 0, "isvalid": 0},
                        {"wheelId": 2, "wheelImpluseCounter": 0, "isvalid": 0},
                        {"wheelId": 3, "wheelImpluseCounter": 0, "isvalid": 0},
                        {"wheelId": 4, "wheelImpluseCounter": 0, "isvalid": 0},
                    ]
                },
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(1)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetWheelImpluseCounter",
                {"wheels": [1, 2, 3, 4]},
                {
                    "out": [
                        {"wheelId": 1, "wheelImpluseCounter": 0, "isvalid": 0},
                        {"wheelId": 2, "wheelImpluseCounter": 0, "isvalid": 0},
                        {"wheelId": 3, "wheelImpluseCounter": 0, "isvalid": 0},
                        {"wheelId": 4, "wheelImpluseCounter": 0, "isvalid": 0},
                    ]
                },
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetWheelImpluseCounter",
                {"wheels": [1, 2, 3, 4]},
                {
                    "out": [
                        {"wheelId": 1, "wheelImpluseCounter": 0, "isvalid": 0},
                        {"wheelId": 2, "wheelImpluseCounter": 0, "isvalid": 0},
                        {"wheelId": 3, "wheelImpluseCounter": 0, "isvalid": 0},
                        {"wheelId": 4, "wheelImpluseCounter": 0, "isvalid": 0},
                    ]
                },
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlRotToothCntr"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetWheelImpluseCounter",
                {"wheels": [1, 2, 3, 4]},
                {
                    "out": [
                        {"wheelId": 1, "wheelImpluseCounter": 0, "isvalid": 1},
                        {"wheelId": 2, "wheelImpluseCounter": 0, "isvalid": 1},
                        {"wheelId": 3, "wheelImpluseCounter": 0, "isvalid": 1},
                        {"wheelId": 4, "wheelImpluseCounter": 0, "isvalid": 1},
                    ]
                },
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlRotToothCntr"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::GetWheelSpeed_WhlSpdCircumlFrntChks::BackboneFR::51-0-2信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987539(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "51-0-2")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlFrnt"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetWheelSpeed",
                {"wheels": [1, 2, 3, 4]},
                {
                    "out": [
                        {"wheelId": 1, "speed": 0.0, "isvalid": False},
                        {"wheelId": 2, "speed": 0.0, "isvalid": False},
                        {"wheelId": 3, "speed": 0.0, "isvalid": True},
                        {"wheelId": 4, "speed": 0.0, "isvalid": True},
                    ]
                },
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(1)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetWheelSpeed",
                {"wheels": [1, 2, 3, 4]},
                {
                    "out": [
                        {"wheelId": 1, "speed": 0.0, "isvalid": False},
                        {"wheelId": 2, "speed": 0.0, "isvalid": False},
                        {"wheelId": 3, "speed": 0.0, "isvalid": False},
                        {"wheelId": 4, "speed": 0.0, "isvalid": False},
                    ]
                },
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetWheelSpeed",
                {"wheels": [1, 2, 3, 4]},
                {
                    "out": [
                        {"wheelId": 1, "speed": 0.0, "isvalid": False},
                        {"wheelId": 2, "speed": 0.0, "isvalid": False},
                        {"wheelId": 3, "speed": 0.0, "isvalid": True},
                        {"wheelId": 4, "speed": 0.0, "isvalid": True},
                    ]
                },
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlFrnt"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetWheelSpeed",
                {"wheels": [1, 2, 3, 4]},
                {
                    "out": [
                        {"wheelId": 1, "speed": 0.0, "isvalid": True},
                        {"wheelId": 2, "speed": 0.0, "isvalid": True},
                        {"wheelId": 3, "speed": 0.0, "isvalid": True},
                        {"wheelId": 4, "speed": 0.0, "isvalid": True},
                    ]
                },
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlFrnt"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::GetWheelSpeed_WhlSpdCircumlReChks::BackboneFR::51-0-2信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987538(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "51-0-2")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlRe"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetWheelSpeed",
                {"wheels": [1, 2, 3, 4]},
                {
                    "out": [
                        {"wheelId": 1, "speed": 0.0, "isvalid": True},
                        {"wheelId": 2, "speed": 0.0, "isvalid": True},
                        {"wheelId": 3, "speed": 0.0, "isvalid": False},
                        {"wheelId": 4, "speed": 0.0, "isvalid": False},
                    ]
                },
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(1)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetWheelSpeed",
                {"wheels": [1, 2, 3, 4]},
                {
                    "out": [
                        {"wheelId": 1, "speed": 0.0, "isvalid": False},
                        {"wheelId": 2, "speed": 0.0, "isvalid": False},
                        {"wheelId": 3, "speed": 0.0, "isvalid": False},
                        {"wheelId": 4, "speed": 0.0, "isvalid": False},
                    ]
                },
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetWheelSpeed",
                {"wheels": [1, 2, 3, 4]},
                {
                    "out": [
                        {"wheelId": 1, "speed": 0.0, "isvalid": True},
                        {"wheelId": 2, "speed": 0.0, "isvalid": True},
                        {"wheelId": 3, "speed": 0.0, "isvalid": False},
                        {"wheelId": 4, "speed": 0.0, "isvalid": False},
                    ]
                },
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlRe"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetWheelSpeed",
                {"wheels": [1, 2, 3, 4]},
                {
                    "out": [
                        {"wheelId": 1, "speed": 0.0, "isvalid": True},
                        {"wheelId": 2, "speed": 0.0, "isvalid": True},
                        {"wheelId": 3, "speed": 0.0, "isvalid": True},
                        {"wheelId": 4, "speed": 0.0, "isvalid": True},
                    ]
                },
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlSpdCircumlRe"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::VehicleMotionState_VehMtnStChks::BackboneFR::55-0-1信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987537(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, "VehMtnStVehMtnSt", 0)
        self.partner.send_request_and_ck_resp(
            "ChassisService_client",
            "GetVehicleMotionState",
            {},
            {"out": {"motionState": 0, "isvalid": True}},
            timeout=3,
        )
        msg_id = self.ipdu.get_signal_message("backbonefr", "55-0-1")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehMtnSt")
            self.partner.ck_s2s_event(
                self.partner_key,
                "VehicleMotionState",
                {"state": {"motionState": 0, "isvalid": False}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(1)
            self.partner.ck_no_event(self.partner_key, "VehicleMotionState")
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "VehicleMotionState")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehMtnSt")
            self.partner.ck_s2s_event(
                self.partner_key,
                "VehicleMotionState",
                {"state": {"motionState": 0, "isvalid": True}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(eval(f"self.ipdu.backbonefr.{msg_id}"), "VehMtnSt")
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::VehicleStandStillSts_StandStillMgrStsForHldChks::ChassisCAN1::0x1F0信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987536(self):
        msg_id = self.ipdu.get_signal_message("chassiscan1", "0x1F0")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "StandStillMgrStsForHld"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "VehicleStandStillSts",
                {"sts": {"value": 0, "validity": 7}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("chassiscan1", f"{msg_id}")
            time.sleep(2)
            self.partner.ck_no_event(self.partner_key, "VehicleStandStillSts")
            self.ipdu.resume_send_pdu("chassiscan1", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "VehicleStandStillSts")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "StandStillMgrStsForHld"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "VehicleStandStillSts",
                {"sts": {"value": 0, "validity": 0}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("chassiscan1", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "StandStillMgrStsForHld"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "ChassisService::WheelImpluseCounter_WhlRotToothCntrChks::BackboneFR::51-0-2信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987535(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "51-0-2")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlRotToothCntr"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "WheelImpluseCounter",
                {
                    "wheelsImpluseCounter": [
                        {"wheelId": 1, "wheelImpluseCounter": 0, "isvalid": 0},
                        {"wheelId": 2, "wheelImpluseCounter": 0, "isvalid": 0},
                        {"wheelId": 3, "wheelImpluseCounter": 0, "isvalid": 0},
                        {"wheelId": 4, "wheelImpluseCounter": 0, "isvalid": 0},
                    ]
                },
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(1)
            self.partner.ck_no_event(self.partner_key, "WheelImpluseCounter")
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "WheelImpluseCounter")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlRotToothCntr"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "WheelImpluseCounter",
                {
                    "wheelsImpluseCounter": [
                        {"wheelId": 1, "wheelImpluseCounter": 0, "isvalid": 1},
                        {"wheelId": 2, "wheelImpluseCounter": 0, "isvalid": 1},
                        {"wheelId": 3, "wheelImpluseCounter": 0, "isvalid": 1},
                        {"wheelId": 4, "wheelImpluseCounter": 0, "isvalid": 1},
                    ]
                },
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "WhlRotToothCntr"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/E2E故障&信号丢失校验event事件场景")
class TestDrivingAssistServiceSignalE2EAndLoss(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("DrivingAssistService", "client")])
        self.partner_key = "DrivingAssistService" + "_client"
        self.ipdu.set(
            self.ipdu.backbonefr.CemBackBoneFr02, "VehModMngtGlbSafe1UsgModSts", 1
        )  # 前置
        self.ipdu.set(
            self.ipdu.backbonefr.CemBackBoneFr02, "VehModMngtGlbSafe1CarModSts1", 0
        )  # 前置
        time.sleep(15)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        self.partner.empty_all()
        # 防止报错造成总线恢复失败
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)

    @allure.title(
        "DrivingAssistService::getHandOFFSts_HandsOnDetectionChks::CEM_LIN4::0x18信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987534(self):
        msg_id = self.ipdu.get_signal_message("cem_lin4", "0x18")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.cem_lin4.{msg_id}"), "HandsOnDetection"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getHandOFFSts",
                {},
                {"out": {"onSts": 0, "errSts": 3}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("cem_lin4", f"{msg_id}")
            time.sleep(1)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getHandOFFSts",
                {},
                {"out": {"onSts": 0, "errSts": 3}},
            )
            self.ipdu.resume_send_pdu("cem_lin4", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getHandOFFSts",
                {},
                {"out": {"onSts": 0, "errSts": 3}},
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.cem_lin4.{msg_id}"), "HandsOnDetection"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "getHandOFFSts",
                {},
                {"out": {"onSts": 0, "errSts": 0}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("cem_lin4", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.cem_lin4.{msg_id}"), "HandsOnDetection"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "DrivingAssistService::handOFFSts_HandsOnDetectionChks::CEM_LIN4::0x18信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987533(self):
        msg_id = self.ipdu.get_signal_message("cem_lin4", "0x18")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.cem_lin4.{msg_id}"), "HandsOnDetection"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "handOFFSts",
                {"sts": {"onSts": 0, "errSts": 3}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("cem_lin4", f"{msg_id}")
            time.sleep(1)
            self.partner.ck_no_event(self.partner_key, "handOFFSts")
            self.ipdu.resume_send_pdu("cem_lin4", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "handOFFSts")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.cem_lin4.{msg_id}"), "HandsOnDetection"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "handOFFSts",
                {"sts": {"onSts": 0, "errSts": 0}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("cem_lin4", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.cem_lin4.{msg_id}"), "HandsOnDetection"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/E2E故障&信号丢失校验event事件场景")
class TestPedalServiceSignalE2EAndLoss(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("PedalService", "client")])
        self.partner_key = "PedalService" + "_client"
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr08, "BrkPedlrRatQf", 3
        )  # 前置
        self.ipdu.set(
            self.ipdu.backbonefr.BcmVddmBackBoneFr00, "BrkPedlPsdQf", 3
        )  # 前置
        time.sleep(15)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        self.partner.empty_all()
        # 防止报错造成总线恢复失败
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)

    @allure.title(
        "PedalService::AccPedalPosition_AccrPedlRatChks::PropulsionCAN::0x04A信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987532(self):
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x04A")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "AccrPedlRat"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "AccPedalPosition",
                {"position": {"position": 0, "statusValidity": 7}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("propulsioncan", f"{msg_id}")
            time.sleep(2)
            self.partner.ck_no_event(self.partner_key, "AccPedalPosition")
            self.ipdu.resume_send_pdu("propulsioncan", f"{msg_id}")
            self.partner.ck_s2s_event(
                self.partner_key,
                "AccPedalPosition",
                {"position": {"position": 0, "statusValidity": 7}},
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "AccrPedlRat"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "AccPedalPosition",
                {"position": {"position": 0, "statusValidity": 0}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("propulsioncan", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "AccrPedlRat"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "PedalService::AccPedalStatus_AccrPedlPsdChks::ChassisCAN2::0x100信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987531(self):
        msg_id = self.ipdu.get_signal_message("chassiscan2", "0x100")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.chassiscan2.{msg_id}"), "AccrPedlPsd")
            self.partner.ck_s2s_event(
                self.partner_key,
                "AccPedalStatus",
                {"status": {"value": 0, "validity": 7}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("chassiscan2", f"{msg_id}")
            time.sleep(1)
            self.partner.ck_no_event(self.partner_key, "AccPedalStatus")
            self.ipdu.resume_send_pdu("chassiscan2", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "AccPedalStatus")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan2.{msg_id}"), "AccrPedlPsd"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "AccPedalStatus",
                {"status": {"value": 0, "validity": 0}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("chassiscan2", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan2.{msg_id}"), "AccrPedlPsd"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "PedalService::GetPedalFault_AccrPedlPsdChks::ChassisCAN2::0x100信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987530(self):
        msg_id = self.ipdu.get_signal_message("chassiscan2", "0x100")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.chassiscan2.{msg_id}"), "AccrPedlPsd")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetPedalFault",
                {},
                {"out": [{"faultId": 1, "faultMsg": "", "id": 0}]},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("chassiscan2", f"{msg_id}")
            time.sleep(1)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetPedalFault",
                {},
                {"out": [{"faultId": 1, "faultMsg": "", "id": 0}]},
            )
            self.ipdu.resume_send_pdu("chassiscan2", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetPedalFault",
                {},
                {"out": [{"faultId": 1, "faultMsg": "", "id": 0}]},
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan2.{msg_id}"), "AccrPedlPsd"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetPedalFault",
                {},
                {"out": [{"faultId": 0, "faultMsg": "", "id": 2}]},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("chassiscan2", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan2.{msg_id}"), "AccrPedlPsd"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "PedalService::GetPedalFault_AccrPedlRatChks::PropulsionCAN::0x04A信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987529(self):
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x04A")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "AccrPedlRat"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetPedalFault",
                {},
                {"out": [{"faultId": 2, "faultMsg": "", "id": 0}]},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("propulsioncan", f"{msg_id}")
            time.sleep(2)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetPedalFault",
                {},
                {"out": [{"faultId": 2, "faultMsg": "", "id": 0}]},
            )
            self.ipdu.resume_send_pdu("propulsioncan", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetPedalFault",
                {},
                {"out": [{"faultId": 2, "faultMsg": "", "id": 0}]},
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "AccrPedlRat"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetPedalFault",
                {},
                {"out": [{"faultId": 0, "faultMsg": "", "id": 2}]},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("propulsioncan", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "AccrPedlRat"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "PedalService::GetStatus_AccrPedlPsdChks::ChassisCAN2::0x100信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987528(self):
        msg_id = self.ipdu.get_signal_message("chassiscan2", "0x100")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.chassiscan2.{msg_id}"), "AccrPedlPsd")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetStatus",
                {"pedals": [0]},
                {"out": [{"id": 0, "status": 0}]},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("chassiscan2", f"{msg_id}")
            time.sleep(1)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetStatus",
                {"pedals": [0]},
                {"out": [{"id": 0, "status": 0}]},
            )
            self.ipdu.resume_send_pdu("chassiscan2", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetStatus",
                {"pedals": [0]},
                {"out": [{"id": 0, "status": 0}]},
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan2.{msg_id}"), "AccrPedlPsd"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetStatus",
                {"pedals": [0]},
                {"out": [{"id": 0, "status": 0}]},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("chassiscan2", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan2.{msg_id}"), "AccrPedlPsd"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "PedalService::GetStatusValidity_AccrPedlPsdChks::ChassisCAN2::0x100信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987527(self):
        msg_id = self.ipdu.get_signal_message("chassiscan2", "0x100")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.chassiscan2.{msg_id}"), "AccrPedlPsd")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetStatusValidity",
                {"pedals": [0]},
                {"out": [{"value": {"id": 0, "status": 0}, "statusValidity": 7}]},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("chassiscan2", f"{msg_id}")
            time.sleep(1)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetStatusValidity",
                {"pedals": [0]},
                {"out": [{"value": {"id": 0, "status": 0}, "statusValidity": 7}]},
            )
            self.ipdu.resume_send_pdu("chassiscan2", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetStatusValidity",
                {"pedals": [0]},
                {"out": [{"value": {"id": 0, "status": 0}, "statusValidity": 7}]},
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan2.{msg_id}"), "AccrPedlPsd"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetStatusValidity",
                {"pedals": [0]},
                {"out": [{"value": {"id": 0, "status": 0}, "statusValidity": 0}]},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("chassiscan2", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan2.{msg_id}"), "AccrPedlPsd"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "PedalService::PedalFault_AccrPedlPsdChks::ChassisCAN2::0x100信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987526(self):
        msg_id = self.ipdu.get_signal_message("chassiscan2", "0x100")
        try:
            self.ipdu.set_no_crc(eval(f"self.ipdu.chassiscan2.{msg_id}"), "AccrPedlPsd")
            self.partner.ck_s2s_event(
                self.partner_key,
                "PedalFault",
                {"faults": [{"faultId": 1, "faultMsg": "", "id": 0}]},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("chassiscan2", f"{msg_id}")
            time.sleep(1)
            self.partner.ck_no_event(self.partner_key, "PedalFault")
            self.ipdu.resume_send_pdu("chassiscan2", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "PedalFault")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan2.{msg_id}"), "AccrPedlPsd"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "PedalFault",
                {"faults": [{"faultId": 0, "faultMsg": "", "id": 2}]},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("chassiscan2", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan2.{msg_id}"), "AccrPedlPsd"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "PedalService::PedalFault_AccrPedlRatChks::PropulsionCAN::0x04A信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987525(self):
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x04A")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "AccrPedlRat"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "PedalFault",
                {"faults": [{"faultId": 2, "faultMsg": "", "id": 0}]},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("propulsioncan", f"{msg_id}")
            time.sleep(2)
            self.partner.ck_no_event(self.partner_key, "PedalFault")
            self.ipdu.resume_send_pdu("propulsioncan", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "PedalFault")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "AccrPedlRat"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "PedalFault",
                {"faults": [{"faultId": 0, "faultMsg": "", "id": 2}]},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("propulsioncan", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "AccrPedlRat"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/E2E故障&信号丢失校验event事件场景")
class TestSteerWheelServiceSignalE2EAndLoss(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("SteerWheelService", "client")])
        self.partner_key = "SteerWheelService" + "_client"
        self.ipdu.set(
            self.ipdu.chassiscan1.PscmChas1Fr07, "PinionSteerAgGroupSteerWhlTqQf", 3
        )  # 前置
        self.ipdu.set(
            self.ipdu.backbonefr.VddmBackBoneFr02, "SteerWhlSnsrQf", 3
        )  # 前置
        time.sleep(15)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        self.partner.empty_all()
        # 防止报错造成总线恢复失败
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)

    @allure.title(
        "SteerWheelService::GetFaultInfo_PinionSteerAgGroupChks::ChassisCAN1::0x04E信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987524(self):
        msg_id = self.ipdu.get_signal_message("chassiscan1", "0x04E")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "PinionSteerAgGroup"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetFaultInfo",
                {},
                {"out": [{"fault": 18, "faultMsg": ""}]},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("chassiscan1", f"{msg_id}")
            time.sleep(2)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetFaultInfo",
                {},
                {"out": [{"fault": 18, "faultMsg": ""}]},
            )
            self.ipdu.resume_send_pdu("chassiscan1", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetFaultInfo",
                {},
                {"out": [{"fault": 18, "faultMsg": ""}]},
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "PinionSteerAgGroup"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetFaultInfo",
                {},
                {"out": [{"fault": 0, "faultMsg": ""}]},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("chassiscan1", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "PinionSteerAgGroup"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "SteerWheelService::GetTorqueInfo_PinionSteerAgGroupChks::ChassisCAN1::0x04E信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987523(self):
        msg_id = self.ipdu.get_signal_message("chassiscan1", "0x04E")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "PinionSteerAgGroup"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetTorqueInfo",
                {},
                {"out": {"torque": 0, "isvalid": False}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("chassiscan1", f"{msg_id}")
            time.sleep(2)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetTorqueInfo",
                {},
                {"out": {"torque": 0, "isvalid": False}},
            )
            self.ipdu.resume_send_pdu("chassiscan1", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetTorqueInfo",
                {},
                {"out": {"torque": 0, "isvalid": False}},
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "PinionSteerAgGroup"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetTorqueInfo",
                {},
                {"out": {"torque": 0, "isvalid": True}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("chassiscan1", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "PinionSteerAgGroup"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "SteerWheelService::SteerWheelFault_PinionSteerAgGroupChks::ChassisCAN1::0x04E信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987522(self):
        msg_id = self.ipdu.get_signal_message("chassiscan1", "0x04E")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "PinionSteerAgGroup"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "SteerWheelFault",
                {"faults": [{"fault": 18, "faultMsg": ""}]},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("chassiscan1", f"{msg_id}")
            time.sleep(2)
            self.partner.ck_no_event(self.partner_key, "SteerWheelFault")
            self.ipdu.resume_send_pdu("chassiscan1", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "SteerWheelFault")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "PinionSteerAgGroup"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "SteerWheelFault",
                {"faults": [{"fault": 0, "faultMsg": ""}]},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("chassiscan1", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "PinionSteerAgGroup"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "SteerWheelService::Torque_PinionSteerAgGroupChks::ChassisCAN1::0x04E信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987521(self):
        msg_id = self.ipdu.get_signal_message("chassiscan1", "0x04E")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "PinionSteerAgGroup"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "Torque",
                {"fTorque": {"torque": 0, "isvalid": False}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("chassiscan1", f"{msg_id}")
            time.sleep(2)
            self.partner.ck_no_event(self.partner_key, "Torque")
            self.ipdu.resume_send_pdu("chassiscan1", f"{msg_id}")
            self.partner.ck_s2s_event(
                self.partner_key, "Torque", {"fTorque": {"torque": 0, "isvalid": False}}
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "PinionSteerAgGroup"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "Torque",
                {"fTorque": {"torque": 0, "isvalid": True}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("chassiscan1", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.chassiscan1.{msg_id}"), "PinionSteerAgGroup"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"


@pytest.mark.full
@allure.feature("SOA服务接口")
@allure.story("通用场景/E2E故障&信号丢失校验event事件场景")
class TestVehicleModeServiceSignalE2EAndLoss(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("VehicleModeService", "client")])
        self.partner_key = "VehicleModeService" + "_client"
        self.ipdu.set(
            self.ipdu.backbonefr.CemBackBoneFr02, "VehModMngtGlbSafe1UsgModSts", 1
        )  # 前置
        self.ipdu.set(
            self.ipdu.backbonefr.CemBackBoneFr02, "VehModMngtGlbSafe1CarModSts1", 0
        )  # 前置
        time.sleep(15)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        self.partner.empty_all()
        # 防止报错造成总线恢复失败
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)

    @allure.title(
        "VehicleModeService::CarModeChangedValidity_VehModMngtGlbSafe1Chks::BackboneFR::36-0-1信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987520(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "36-0-1")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "VehModMngtGlbSafe1"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "CarModeChangedValidity",
                {"mode": {"value": 0, "validity": 7}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.ck_no_event(self.partner_key, "CarModeChangedValidity")
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "CarModeChangedValidity")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "VehModMngtGlbSafe1"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "CarModeChangedValidity",
                {"mode": {"value": 0, "validity": 0}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "VehModMngtGlbSafe1"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "VehicleModeService::GetCarModeValidity_VehModMngtGlbSafe1Chks::BackboneFR::36-0-1信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987518(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "36-0-1")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "VehModMngtGlbSafe1"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetCarModeValidity",
                {},
                {"out": {"value": 0, "validity": 7}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetCarModeValidity",
                {},
                {"out": {"value": 0, "validity": 7}},
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetCarModeValidity",
                {},
                {"out": {"value": 0, "validity": 7}},
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "VehModMngtGlbSafe1"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetCarModeValidity",
                {},
                {"out": {"value": 0, "validity": 0}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "VehModMngtGlbSafe1"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "VehicleModeService::GetExhibitionModeSts_ExhibitionModeStsChks::PropulsionCAN::0x27C信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987516(self):
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x27C")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "ExhibitionModeSts"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetExhibitionModeSts",
                {},
                {"out": {"isOpen": False, "isValid": False}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("propulsioncan", f"{msg_id}")
            time.sleep(1)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetExhibitionModeSts",
                {},
                {"out": {"isOpen": False, "isValid": False}},
            )
            self.ipdu.resume_send_pdu("propulsioncan", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetExhibitionModeSts",
                {},
                {"out": {"isOpen": False, "isValid": False}},
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "ExhibitionModeSts"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetExhibitionModeSts",
                {},
                {"out": {"isOpen": False, "isValid": True}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("propulsioncan", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "ExhibitionModeSts"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "VehicleModeService::GetUsageModeValidity_VehModMngtGlbSafe1Chks::BackboneFR::36-0-1信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987515(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "36-0-1")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "VehModMngtGlbSafe1"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetUsageModeValidity",
                {},
                {"out": {"value": 1, "validity": 7}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetUsageModeValidity",
                {},
                {"out": {"value": 1, "validity": 7}},
            )
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetUsageModeValidity",
                {},
                {"out": {"value": 1, "validity": 7}},
            )
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "VehModMngtGlbSafe1"
            )
            self.partner.send_request_and_ck_resp(
                self.partner_key,
                "GetUsageModeValidity",
                {},
                {"out": {"value": 1, "validity": 0}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "VehModMngtGlbSafe1"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "VehicleModeService::NotifyExhibitionModeSts_ExhibitionModeStsChks::PropulsionCAN::0x27C信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987513(self):
        msg_id = self.ipdu.get_signal_message("propulsioncan", "0x27C")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "ExhibitionModeSts"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "NotifyExhibitionModeSts",
                {"sts": {"isOpen": False, "isValid": False}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("propulsioncan", f"{msg_id}")
            time.sleep(1)
            self.partner.ck_no_event(self.partner_key, "NotifyExhibitionModeSts")
            self.ipdu.resume_send_pdu("propulsioncan", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "NotifyExhibitionModeSts")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "ExhibitionModeSts"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "NotifyExhibitionModeSts",
                {"sts": {"isOpen": False, "isValid": True}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("propulsioncan", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.propulsioncan.{msg_id}"), "ExhibitionModeSts"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"

    @allure.title(
        "VehicleModeService::UsageModeChangedValidity_VehModMngtGlbSafe1Chks::BackboneFR::36-0-1信号E2E故障存在时制造信号丢失不会上报异常event"
    )
    def test_caseid_1987512(self):
        msg_id = self.ipdu.get_signal_message("backbonefr", "36-0-1")
        try:
            self.ipdu.set_no_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "VehModMngtGlbSafe1"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "UsageModeChangedValidity",
                {"mode": {"value": 1, "validity": 7}},
                timeout=3,
            )
            self.partner.empty_all(1)
            self.ipdu.stop_send_pdu("backbonefr", f"{msg_id}")
            time.sleep(2)
            self.partner.ck_no_event(self.partner_key, "UsageModeChangedValidity")
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.partner.ck_no_event(self.partner_key, "UsageModeChangedValidity")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "VehModMngtGlbSafe1"
            )
            self.partner.ck_s2s_event(
                self.partner_key,
                "UsageModeChangedValidity",
                {"mode": {"value": 1, "validity": 0}},
                timeout=3,
            )
        except Exception as e:
            self.ipdu.resume_send_pdu("backbonefr", f"{msg_id}")
            self.ipdu.restore_crc(
                eval(f"self.ipdu.backbonefr.{msg_id}"), "VehModMngtGlbSafe1"
            )
            logger.info(f"故障清除或信号丢失报错{e}")
            assert False, f"故障清除或信号丢失报错{e}"
