#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_encryption.py
@Time         :2023/08/02 17:30:31
@Author       :jingjing.wang@jiduauto.com
@Description  :
"""
import uuid
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import * #封装所有soa的接口,底层调用从这里走的
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_ecu.legacy.common.data_type_handing import logger, DataTypeHanding#数据类型转换
from xat_ecu.legacy.soa_partner.src.partner_const import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *#数字钥匙所有的
from xat_cases.legacy.soa.case_helper.update_salt import * #修改idl进行编译
from xat_ecu.legacy.sdk.digital_key.RVCTSPMessage_pb2 import *

KEY_MATCH_INFO = {1: [2, 3, 4, 5, 6, 8, 0xA, 0xB],
                  2: [2, 3, 4, 5, 6, 0xA, 0xB],
                  3: [3, 6, 0xA],
                  4: [4, 6, 0xB],
                  6: [8],
                  7: [8],
                  8: [8]
                  }
default_ccp_list = DataTypeHanding.hexstr_to_inlist(
    "A3018006FD030101A302090304020102858B06010004050203000001048C800C0101010102010202010216010701010100030102028089020301010302736E03010101010101010302020202020A010103820201010102020103010201800202020201800000008182118003010103020102020302800102010102010104010101010101010203010103020101830201020201012902010402038002820103040128030A800104010201020203820402810101020101130301010101010205020101000302020304020202010101020001010101010101010180030A0101040607070A0A07070A0A00000400000201010101010280030301020000000202020102020200010102000000010300000100008100000000000000000000000000000080000000000000000000000100010100000200000080000000008403010100000000020100000000000000000002018001020101010101020103020180018002020101010101050380020601030110000002030100000000000000000000000000000000000000000000000000000002000000000001010301000000000200000000000000000000000000000000000000000000000000010201000000000085040102020201020202040301020201028004030101020201030101010202020101020101010101030000000180020201010202010202020102010302020101010101010101000103010201010502020204010101010301010402010201010101020101010101010100000000000001020301010109030101010202020101030104010401010101010201030105020001010101010101010101010101010101010101010101010202010101010102010101010201000001010401000000010100000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001030202080100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001010201020102020101020101010101010201010201010101010202010201010101020202020202010202010202010201010101020101010102010101000102010101000101010101020202010101020201010101010102020102010101010101010001010101010101020101010101020101010101010101010101010101010101010101020201020101010101010100000101010101010101020101010101010101010202000101010101010202020101010100000000000000000000000000000000000000000000000000000000000000000000020202020202020101010101010101020101010101010202020202010002020101020102020201020001")


@allure.feature("SOA中间件测试")
@allure.story("信息安全/domin cdcq")
@pytest.mark.wjj
class Testencryption(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = None

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkNotEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEKeyPrsntStsZone7', 'Validity_NotValid')
        self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4})
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])  # 5门硬线均关闭
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.sd_tester.send_data([0x22, 0xF1, 0x90])  # 查vin码
        logger.info(self.sd_tester.return_udsdata_and_check_and_print_response_result(
            "Send xxxto get result"))  # 读vindayin出来,打印出来后在not++里面转阿克斯码
        self.tc_vin_list = self.write_vin(self.tc_config['vin'])

    def after_each_func(self, ecu):
        self.bgmcli.get_set_salt()
        self.write_vin(self.tc_config['vin'])
        reset_soa_partner()  # 恢复soapartner
        super().after_each_func(ecu, start=False)

    def write_vin(self, vin_str):
        """写入vin码"""
        self.sd_tester.enter_extended_session()
        self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 1003 to get result")
        self.sd_tester.security_access_level_l3()
        self.sd_tester.write_vin(vin_str)
        self.sd_tester.return_udsdata_and_check_and_print_response_result("Send 2EF190 to get result")
        return list(bytes(vin_str, encoding="ascii"))

    def write_ccp(self, ccp_list=default_ccp_list):
        self.sd_tester.write_multi_ccp({index + 1: ccp_list[index] for index in range(1556)})

    def update_key(self, key, value):
        get_set_salt(key, value)  # 修改AesKey值

    def get_ccp(self, count):
        """获取ccp#？的值, ccp1即第0个ccp"""
        return self.sd_tester.read_ccp()[1][count - 1]

    def get_vin_list_from_canbus(self):
        """从总线获取mcu发出的vin码"""
        vin = [0] * 17
        res = [1, 2, 3]
        st = time.time()
        while time.time() - st < 20:
            Nr = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr08, 'VinBlockNr')
            logger.info(Nr)
            if Nr in res:
                for i in range(7 if Nr in [1, 2] else 3):
                    vin[i + 7 * (Nr - 1)] = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr08,
                                                                                  f'VinVINSignalPos{i + 1}')
                res.remove(Nr)
                if not res:
                    return vin
            sleep(0.005)
        else:
            assert False, "超时未获取到vin信息"

    def get_config_list_from_canbus(self):
        """从总线获取mcu发出的ccp#1-504数据"""
        config_list = [0] * 504
        res = [index + 1 for index in range(72)]
        st = time.time()
        while time.time() - st < 20:
            Nr = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr06,
                                                       'VehCfgPrmBlkIDBytePosn1_0_CEMBackBoneSignalIpdu06')
            if Nr in res:
                for i in range(7):
                    config_list[7 * (Nr - 1) + i] = self.ipdu.get_recent_signal_raw_value(
                        self.ipdu.backbonefr.CemBackBoneFr06, f'VehCfgPrmCCPBytePosn{i + 2}_0_CEMBackBoneSignalIpdu06')
                res.remove(Nr)
                if not res:
                    return config_list
            sleep(0.005)
        else:
            assert False, "超时未获取到ccp#1-504信息"

    def get_extendconfig_list_from_canbus(self):
        """从总线获取mcu发出的ccp#505-1008数据"""
        extendConfig_list = [0] * 504
        res = [index + 1 for index in range(72)]
        st = time.time()
        while time.time() - st < 20:
            Nr = self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr23,
                                                       'VehCfgPrmExtBlkIDBytePosn1_0_CemBackBoneSignalIPdu23')
            if Nr in res:
                for i in range(7):
                    extendConfig_list[7 * (Nr - 1) + i] = self.ipdu.get_recent_signal_raw_value(
                        self.ipdu.backbonefr.CemBackBoneFr23,
                        f'VehCfgPrmExtCCPBytePosn{i + 2}_0_CemBackBoneSignalIPdu23')
                res.remove(Nr)
                logger.info(res)
                if not res:
                    return extendConfig_list
            sleep(0.005)
        else:
            assert False, "超时未获取到ccp#505-1008信息"

    def get_nodelist_from_canbus(self):
        """从总线获取mcu发出的nodelist数据"""
        res = []
        for i in range(8):
            res.append(
                self.ipdu.get_recent_signal_raw_value(self.ipdu.backbonefr.CemBackBoneFr11, f'ListOfNodAv{i + 1}'))
        return res
    
    @allure.title("BGM-ServerLv1_ClientLv0_Event_Method均失败")
    @pytest.mark.full
    def test_caseid_111610(self):
        backup_service("DoorService.jidl")
        update_security_level("DoorService.jidl", "FrntLeftDoorSts", 0)
        update_security_level("DoorService.jidl", "GetAntiPinch", 0)
        rebuild_soa_partner("DoorService.jidl")
        self.partner = S2sBaseClass([DOOR_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(DOOR_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 0)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts")
        self.partner.send_request_and_ck_failtype(DOOR_SERVICE_CLIENT, "GetAntiPinch", {"doors": [0]},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("BGM-ServerLv1_ClientLv1_Event_Method均成功")
    @pytest.mark.smoke
    def test_caseid_111606(self):
        self.partner = S2sBaseClass([DOOR_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(DOOR_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 0)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {"sts": {"isAntiPinch": False}})
        self.partner.send_request_and_ck_failtype(DOOR_SERVICE_CLIENT, "GetAntiPinch", {"doors": [0]},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("BGM-ServerLv1_ClientLv1_AesKey_Event_Method均成功")
    @pytest.mark.sanity
    def test_caseid_111605(self):
        get_set_salt("aes_key", "c5e00149cc51620e5179693762679600")  # 修改AesKey值
        self.partner = S2sBaseClass([DOOR_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(DOOR_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 0)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {"sts": {"isAntiPinch": False}})
        self.partner.send_request_and_ck_failtype(DOOR_SERVICE_CLIENT, "GetAntiPinch", {"doors": [0]},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("BGM-ServerLv1_ClientLv1_AesIv_Event_Method均成功")
    @pytest.mark.sanity
    def test_caseid_111604(self):
        get_set_salt("aes_iv", "7b6d98f7b3058a92a1a32dfaecd70183")
        self.partner = S2sBaseClass([DOOR_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(DOOR_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 0)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {"sts": {"isAntiPinch": False}})
        self.partner.send_request_and_ck_failtype(DOOR_SERVICE_CLIENT, "GetAntiPinch", {"doors": [0]},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("BGM-ServerLv1_ClientLv1_CmacKey_Event_Method均成功")
    @pytest.mark.sanity
    def test_caseid_111603(self):
        get_set_salt("cmac_key", __import__("os").environ['XAT_CREDENTIAL_SCAN_288613059C8544DB1874'])
        self.partner = S2sBaseClass([DOOR_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(DOOR_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 0)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {"sts": {"isAntiPinch": False}})
        self.partner.send_request_and_ck_failtype(DOOR_SERVICE_CLIENT, "GetAntiPinch", {"doors": [0]},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("BGM-ServerLv1_ClientLv2_Event_Method均失败")
    @pytest.mark.sanity
    def test_caseid_111602(self):
        backup_service("DoorService.jidl")
        update_security_level("DoorService.jidl", "FrntLeftDoorSts", 2)
        update_security_level("DoorService.jidl", "GetAntiPinch", 2)
        rebuild_soa_partner("DoorService.jidl")
        self.partner = S2sBaseClass([DOOR_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(DOOR_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 0)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts")
        self.partner.send_request_and_ck_failtype(DOOR_SERVICE_CLIENT, "GetAntiPinch", {"doors": [0]},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("BGM-ServerLv1_ClientLv3_Event_Method均失败")
    @pytest.mark.full
    def test_caseid_111598(self):
        backup_service("DoorService.jidl")
        update_security_level("DoorService.jidl", "FrntLeftDoorSts", 3)
        update_security_level("DoorService.jidl", "GetAntiPinch", 3)
        rebuild_soa_partner("DoorService.jidl")
        self.partner = S2sBaseClass([DOOR_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(DOOR_SERVICE_CLIENT)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 0)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts")
        self.partner.send_request_and_ck_failtype(DOOR_SERVICE_CLIENT, "GetAntiPinch", {"doors": [0]},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("BGM-ServerLv0_ClientLv0_Event_Method均成功")
    @pytest.mark.smoke
    def test_caseid_111594(self):
        self.partner = S2sBaseClass([SEAT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(SEAT_SERVICE_CLIENT)
        self.io.driver_seat_notpresent()
        sleep(0.5)
        self.io.driver_seat_present()
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatus",
                                  {"infos": [{"seatId": 0, "rawSensorStatus": 1}]})
        self.partner.send_request_and_ck_failtype(SEAT_SERVICE_CLIENT, "GetOccupied", {"seats": [0]},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("BGM-ServerLv0_ClientLv0_AesKey_Event_Method均成功")
    @pytest.mark.sanity
    def test_caseid_1911932(self):
        get_set_salt("aes_key", "c5e00149cc51620e5179693762679600")
        self.partner = S2sBaseClass([SEAT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(SEAT_SERVICE_CLIENT)
        self.io.driver_seat_notpresent()
        sleep(0.5)
        self.io.driver_seat_present()
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatus",
                                  {"infos": [{"seatId": 0, "rawSensorStatus": 1}]})
        self.partner.send_request_and_ck_failtype(SEAT_SERVICE_CLIENT, "GetOccupied", {"seats": [0]},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("BGM-ServerLv0_ClientLv0_AesIv_Event_Method均成功")
    @pytest.mark.sanity
    def test_caseid_1911955(self):
        get_set_salt("aes_iv", "7b6d98f7b3058a92a1a32dfaecd70183")
        self.partner = S2sBaseClass([SEAT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(SEAT_SERVICE_CLIENT)
        self.io.driver_seat_notpresent()
        sleep(0.5)
        self.io.driver_seat_present()
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatus",
                                  {"infos": [{"seatId": 0, "rawSensorStatus": 0, "status": 1}]})
        self.partner.send_request_and_ck_failtype(SEAT_SERVICE_CLIENT, "GetOccupied", {"seats": [0]},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("BGM-ServerLv0_ClientLv0_CmacKey_Event_Method均成功")
    @pytest.mark.sanity
    def test_caseid_1912001(self):
        get_set_salt("cmac_key", __import__("os").environ['XAT_CREDENTIAL_SCAN_668AAC172824EA40812E'])
        self.partner = S2sBaseClass([SEAT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(SEAT_SERVICE_CLIENT)
        self.io.driver_seat_notpresent()
        sleep(0.5)
        self.io.driver_seat_present()
        self.partner.ck_s2s_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatus",
                                  {"infos": [{"seatId": 0, "rawSensorStatus": 0, "status": 1}]})
        self.partner.send_request_and_ck_failtype(SEAT_SERVICE_CLIENT, "GetOccupied", {"seats": [0]},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("BGM-ServerLv0_ClientLv1_Event成功_Method失败")
    @pytest.mark.full
    def test_caseid_111590(self):
        backup_service("SeatService.jidl")
        update_security_level("SeatService.jidl", "SeatOccupyStatus", 1)
        update_security_level("SeatService.jidl", "GetOccupied", 1)
        rebuild_soa_partner("SeatService.jidl")
        self.partner = S2sBaseClass([SEAT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(SEAT_SERVICE_CLIENT)
        self.io.driver_seat_present()
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatus")
        self.partner.send_request_and_ck_failtype(SEAT_SERVICE_CLIENT, "GetOccupied", {"seats": [0]},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("BGM-ServerLv0_ClientLv2_Event_Method均失败")
    @pytest.mark.full
    def test_caseid_111586(self):
        backup_service("SeatService.jidl")
        update_security_level("SeatService.jidl", "SeatOccupyStatus", 2)
        update_security_level("SeatService.jidl", "GetOccupied", 2)
        rebuild_soa_partner("SeatService.jidl")
        self.partner = S2sBaseClass([SEAT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(SEAT_SERVICE_CLIENT)
        self.io.driver_seat_notpresent()
        sleep(0.5)
        self.io.driver_seat_present()
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatus")
        self.partner.send_request_and_ck_failtype(SEAT_SERVICE_CLIENT, "GetOccupied", {"seats": [0]},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("BGM-ServerLv0_ClientLv3_Event_Method均失败")
    @pytest.mark.full
    def test_caseid_111582(self):
        backup_service("SeatService.jidl")
        update_security_level("SeatService.jidl", "SeatOccupyStatus", 3)
        update_security_level("SeatService.jidl", "GetOccupied", 3)
        rebuild_soa_partner("SeatService.jidl")
        self.partner = S2sBaseClass([SEAT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(SEAT_SERVICE_CLIENT)
        self.io.driver_seat_notpresent()
        sleep(0.5)
        self.io.driver_seat_present()
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "SeatOccupyStatus")
        self.partner.send_request_and_ck_failtype(SEAT_SERVICE_CLIENT, "GetOccupied", {"seats": [0]},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)
        
    @allure.title("BGM-ServerLv3_ClientLv3_Event_Method均成功")#idl7以上
    @pytest.mark.smoke
    def test_caseid_1983470(self):
        self.partner = S2sBaseClass([KEY_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(KEY_SERVICE_CLIENT)
        execid = str(uuid.uuid1()).replace("-", "")
        self.dk.send_rke_lock(exec_id=execid)
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = execid
        real_cmd.vid = f'{1:032}'
        real_cmd.vehicleModel = 61
        real_cmd.cmdCode = 1
        real_cmd.timestamp = 1000000012345678

        cd = CmdDetail()
        lc = LockControl()
        lc.op = 2
        lc.keyId = f'{1:032}'
        lc.userId = ''
        cd.lock_control.MergeFrom(lc)
        real_cmd.cmdDetail.MergeFrom(cd)
        ble_payload = real_cmd.SerializeToString().hex()
        ck_data = DataTypeHanding.hexstr_to_inlist(f'21{1 + len(ble_payload) // 2:04X}{1:02X}{ble_payload}')
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyDataUp", {"data": ck_data}, fuzz_match=False)  # case写死
        self.partner.send_request_and_ck_failtype(KEY_SERVICE_CLIENT, "GetDigitalKeyDataUp", {}, FailType.FAILTYPE_SUCCESS)

    @allure.title("BGM-ServerLv3_ClientLv3_AesKey_Method失败")#idl7以上
    @pytest.mark.sanity
    def test_caseid_1983471(self):
        get_set_salt("aes_key", "c5e00149cc51620e5179693762679600")
        self.partner = S2sBaseClass([KEY_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(KEY_SERVICE_CLIENT)
        execid = str(uuid.uuid1()).replace("-", "")
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.send_rke_lock(exec_id=execid)
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = execid
        real_cmd.vid = f'{1:032}'
        real_cmd.vehicleModel = 61
        real_cmd.cmdCode = 1
        real_cmd.timestamp = 1000000012345678

        self.partner.ck_no_event(KEY_SERVICE_CLIENT, "DigitalKeyDataUp")  # case写死
        self.partner.send_request_and_ck_failtype(KEY_SERVICE_CLIENT, "GetDigitalKeyDataUp", {}, FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("BGM-ServerLv3_ClientLv3_AesIv_Method失败")#idl7以上
    @pytest.mark.full
    def test_caseid_1983472(self):
        get_set_salt("aes_iv", "7b6d98f7b3058a92a1a32dfaecd70183")
        self.partner = S2sBaseClass([KEY_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(KEY_SERVICE_CLIENT)
        execid = str(uuid.uuid1()).replace("-", "")
        self.dk.send_rke_lock(exec_id=execid)
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = execid
        real_cmd.vid = f'{1:032}'
        real_cmd.vehicleModel = 61
        real_cmd.cmdCode = 1
        real_cmd.timestamp = 1000000012345678

        self.partner.ck_no_event(KEY_SERVICE_CLIENT, "DigitalKeyDataUp") 
        self.partner.send_request_and_ck_failtype(KEY_SERVICE_CLIENT, "GetDigitalKeyDataUp", {}, FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("BGM-ServerLv3_ClientLv3_CmacKey_Method均失败")#idl7以上
    @pytest.mark.full
    def test_caseid_1983473(self):
        get_set_salt("cmac_key", __import__("os").environ['XAT_CREDENTIAL_SCAN_6EF1D7A7FDB711843FC8'])
        self.partner = S2sBaseClass([KEY_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(KEY_SERVICE_CLIENT)
        execid = str(uuid.uuid1()).replace("-", "")
        self.dk.send_rke_lock(exec_id=execid)
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = execid
        real_cmd.vid = f'{1:032}'
        real_cmd.vehicleModel = 61
        real_cmd.cmdCode = 1
        real_cmd.timestamp = 1000000012345678
        self.partner.ck_no_event(KEY_SERVICE_CLIENT, "DigitalKeyDataUp") 
        self.partner.send_request_and_ck_failtype(KEY_SERVICE_CLIENT, "GetDigitalKeyDataUp", {}, FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("BGM-ServerLv3_ClientLv0_Method均失败")#idl7以上
    @pytest.mark.smoke
    def test_caseid_1983474(self):
        backup_service("KeyService.jidl")
        update_security_level("KeyService.jidl", "GetDigitalKeyDataUp", 0)
        rebuild_soa_partner("KeyService.jidl")
        self.partner = S2sBaseClass([KEY_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(KEY_SERVICE_CLIENT)
        execid = str(uuid.uuid1()).replace("-", "")
        self.dk.send_rke_lock(exec_id=execid)
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = execid
        real_cmd.vid = f'{1:032}'
        real_cmd.vehicleModel = 61
        real_cmd.cmdCode = 1
        real_cmd.timestamp = 1000000012345678
        self.partner.ck_no_event(KEY_SERVICE_CLIENT, "DigitalKeyDataUp") 
        self.partner.send_request_and_ck_failtype(KEY_SERVICE_CLIENT, "GetDigitalKeyDataUp", {}, FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("BGM-ServerLv3_ClientLv1_Event_Method均失败")#idl7以上
    @pytest.mark.full
    def test_caseid_1983475(self):
        backup_service("KeyService.jidl")
        update_security_level("KeyService.jidl", "GetDigitalKeyDataUp", 1)
        rebuild_soa_partner("KeyService.jidl")
        self.partner = S2sBaseClass([KEY_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(KEY_SERVICE_CLIENT)
        execid = str(uuid.uuid1()).replace("-", "")
        self.dk.send_rke_lock(exec_id=execid)
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = execid
        real_cmd.vid = f'{1:032}'
        real_cmd.vehicleModel = 61
        real_cmd.cmdCode = 1
        real_cmd.timestamp = 1000000012345678

        self.partner.ck_no_event(KEY_SERVICE_CLIENT, "DigitalKeyDataUp")
        self.partner.send_request_and_ck_failtype(KEY_SERVICE_CLIENT, "GetDigitalKeyDataUp", {}, FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("BGM-ServerLv3_ClientLv2_Event_Method均失败")#idl7以上
    @pytest.mark.full
    def test_caseid_1983476(self):
        backup_service("KeyService.jidl")
        update_security_level("KeyService.jidl", "GetDigitalKeyDataUp", 2)
        rebuild_soa_partner("KeyService.jidl")
        self.partner = S2sBaseClass([KEY_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(KEY_SERVICE_CLIENT)
        execid = str(uuid.uuid1()).replace("-", "")
        self.dk.send_rke_lock(exec_id=execid)
        real_cmd = RealtimeCmdReq()
        real_cmd.execId = execid
        real_cmd.vid = f'{1:032}'
        real_cmd.vehicleModel = 61
        real_cmd.cmdCode = 1
        real_cmd.timestamp = 1000000012345678

        self.partner.ck_no_event(KEY_SERVICE_CLIENT, "DigitalKeyDataUp") 
        self.partner.send_request_and_ck_failtype(KEY_SERVICE_CLIENT, "GetDigitalKeyDataUp", {}, FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("BGM-ServerLv2_ClientLv2_Event_Method均成功")
    @pytest.mark.smoke
    def test_caseid_111571(self):
        self.partner = S2sBaseClass([CARCONFIG_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(CARCONFIG_SERVICE_CLIENT)
        vin = self.write_vin('11111111111111111')
        self.partner.ck_s2s_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN", {"vin": {"vin": vin}}, fuzz_match=False,
                                  timeout=3)
        self.partner.send_request_and_ck_failtype(CARCONFIG_SERVICE_CLIENT, "GetVIN", {}, FailType.FAILTYPE_SUCCESS)

    @allure.title("BGM-ServerLv2_ClientLv2_AesKey_Event_Method均失败")
    @pytest.mark.sanity
    def test_caseid_1912509(self):
        get_set_salt("aes_key", "c5e00149cc51620e5179693762679600")
        self.partner = S2sBaseClass([CARCONFIG_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(CARCONFIG_SERVICE_CLIENT)
        vin = self.write_vin('11111111111111111')
        self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN")
        self.partner.send_request_and_ck_failtype(CARCONFIG_SERVICE_CLIENT, "GetVIN", {},
                                                  FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("BGM-ServerLv2_ClientLv2_AesIv_Event_Method均失败")
    @pytest.mark.sanity
    def test_caseid_1912007(self):
        get_set_salt("aes_iv", "7b6d98f7b3058a92a1a32dfaecd70183")
        self.partner = S2sBaseClass([CARCONFIG_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(CARCONFIG_SERVICE_CLIENT)
        vin = self.write_vin('11111111111111111')
        self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN")
        self.partner.send_request_and_ck_failtype(CARCONFIG_SERVICE_CLIENT, "GetVIN", {},
                                                  FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("BGM-ServerLv2_ClientLv2_CmacKey_Event_Method均成功")
    @pytest.mark.sanity
    def test_caseid_111568(self):
        get_set_salt("cmac_key", __import__("os").environ['XAT_CREDENTIAL_SCAN_2EE9644D5FF276FD4EB8'])
        self.partner = S2sBaseClass([CARCONFIG_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(CARCONFIG_SERVICE_CLIENT)
        vin = self.write_vin('11111111111111111')
        sleep(0.5)
        vin = self.write_vin('22222222222222222')
        self.partner.ck_s2s_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN", {"vin": {"vin": vin}}, fuzz_match=False)
        self.partner.send_request_and_ck_failtype(CARCONFIG_SERVICE_CLIENT, "GetVIN", {}, FailType.FAILTYPE_SUCCESS)

    @allure.title("BGM-ServerLv2_ClientLv0_Event_Method均失败")
    @pytest.mark.full
    def test_caseid_111567(self):
        backup_service("CarConfigService.jidl")
        update_security_level("CarConfigService.jidl", "NotifyVIN", 0)
        update_security_level("CarConfigService.jidl", "GetVIN", 0)
        rebuild_soa_partner("CarConfigService.jidl")
        self.partner = S2sBaseClass([CARCONFIG_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(CARCONFIG_SERVICE_CLIENT)
        vin = self.write_vin('11111111111111111')
        self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN")
        self.partner.send_request_and_ck_failtype(CARCONFIG_SERVICE_CLIENT, "GetVIN", {},
                                                  FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("BGM-ServerLv2_ClientLv1_Event_Method均失败")
    @pytest.mark.full
    def test_caseid_111566(self):
        backup_service("CarConfigService.jidl")
        update_security_level("CarConfigService.jidl", "NotifyVIN", 1)
        update_security_level("CarConfigService.jidl", "GetVIN", 1)
        rebuild_soa_partner("CarConfigService.jidl")
        self.partner = S2sBaseClass([CARCONFIG_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(CARCONFIG_SERVICE_CLIENT)
        vin = self.write_vin('11111111111111111')
        self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN")
        self.partner.send_request_and_ck_failtype(CARCONFIG_SERVICE_CLIENT, "GetVIN", {},
                                                  FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("BGM-ServerLv2_ClientLv3_Event_Method均失败")
    @pytest.mark.sanity
    def test_caseid_111565(self):
        backup_service("CarConfigService.jidl")
        update_security_level("CarConfigService.jidl", "NotifyVIN", 3)
        update_security_level("CarConfigService.jidl", "GetVIN", 3)
        rebuild_soa_partner("CarConfigService.jidl")
        self.partner = S2sBaseClass([CARCONFIG_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(CARCONFIG_SERVICE_CLIENT)
        vin = self.write_vin('11111111111111111')
        self.partner.ck_no_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN")
        self.partner.send_request_and_ck_failtype(CARCONFIG_SERVICE_CLIENT, "GetVIN", {},
                                                  FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("BGM-ServerLv2_ClientLv2_Event_Method均成功压测")
    @pytest.mark.full
    def test_caseid_111564(self):
        self.partner = S2sBaseClass([CARCONFIG_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(CARCONFIG_SERVICE_CLIENT)
        vin = self.write_vin('11111111111111111')
        for i in range(21):
            self.restart_bgm_and_connect_service(CARCONFIG_SERVICE_CLIENT)
            logger.info(f"压测第{i}次")
            self.partner.ck_s2s_event(CARCONFIG_SERVICE_CLIENT, "NotifyVIN", {"vin": {"vin": vin}}, fuzz_match=False)
            self.partner.send_request_and_ck_failtype(CARCONFIG_SERVICE_CLIENT, "GetVIN", {}, FailType.FAILTYPE_SUCCESS)

    @allure.title("CDC-ServerLv1_ClientLv0_Method失败")
    @pytest.mark.full
    def test_caseid_1903544(self):
        backup_service("NaviService.jidl")
        update_security_level("NaviService.jidl", "GetSDMapMatchInfo", 0)
        rebuild_soa_partner("NaviService.jidl")
        self.partner = S2sBaseClass([NAVI_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(NAVI_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(NAVI_SERVICE_CLIENT, "GetSDMapMatchInfo", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("CDC-ServerLv1_ClientLv1_Method成功")
    @pytest.mark.full
    def test_caseid_1903543(self):
        self.partner = S2sBaseClass([NAVI_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(NAVI_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(NAVI_SERVICE_CLIENT, "GetSDMapMatchInfo", {},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("CDC-ServerLv1_ClientLv1_AesKey_Method成功")
    @pytest.mark.full
    def test_caseid_1903542(self):
        get_set_salt("aes_key", "c5e00149cc51620e5179693762679600")
        self.partner = S2sBaseClass([NAVI_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(NAVI_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(NAVI_SERVICE_CLIENT, "GetSDMapMatchInfo", {},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("CDC-ServerLv1_ClientLv1_AesIv_Method成功")
    @pytest.mark.full
    def test_caseid_1903541(self):
        get_set_salt("aes_iv", "7b6d98f7b3058a92a1a32dfaecd70183")
        self.partner = S2sBaseClass([NAVI_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(NAVI_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(NAVI_SERVICE_CLIENT, "GetSDMapMatchInfo", {},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("CDC-ServerLv1_ClientLv1_CmacKey_Method成功")
    @pytest.mark.full
    def test_caseid_1903540(self):
        get_set_salt("cmac_key", __import__("os").environ['XAT_CREDENTIAL_SCAN_B4CF82E20E9EF16D5BE1'])
        self.partner = S2sBaseClass([NAVI_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(NAVI_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(NAVI_SERVICE_CLIENT, "GetSDMapMatchInfo", {},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("CDC-ServerLv1_ClientLv2_Method失败")
    @pytest.mark.full
    def test_caseid_1903539(self):
        backup_service("NaviService.jidl")
        update_security_level("NaviService.jidl", "GetSDMapMatchInfo", 2)
        rebuild_soa_partner("NaviService.jidl")
        self.partner = S2sBaseClass([NAVI_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(NAVI_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(NAVI_SERVICE_CLIENT, "GetSDMapMatchInfo", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("CDC-ServerLv1_ClientLv3_Method失败")
    @pytest.mark.full
    def test_caseid_1903538(self):
        backup_service("NaviService.jidl")
        update_security_level("NaviService.jidl", "GetSDMapMatchInfo", 3)
        rebuild_soa_partner("NaviService.jidl")
        self.partner = S2sBaseClass([NAVI_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(NAVI_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(NAVI_SERVICE_CLIENT, "GetSDMapMatchInfo", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("CDC-ServerLv3_ClientLv1_Method失败")
    @pytest.mark.full
    def test_caseid_1903537(self):
        backup_service("account_service.jidl")
        update_security_level("account_service.jidl", "getAccountSts", 1)
        rebuild_soa_partner("account_service.jidl")
        self.partner = S2sBaseClass([ACCOUNT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(ACCOUNT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACCOUNT_SERVICE_CLIENT, "getAccountSts", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("CDC-ServerLv3_ClientLv2_Method失败")
    @pytest.mark.full
    def test_caseid_1903536(self):
        backup_service("account_service.jidl")
        update_security_level("account_service.jidl", "getAccountSts", 2)
        rebuild_soa_partner("account_service.jidl")
        self.partner = S2sBaseClass([ACCOUNT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(ACCOUNT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACCOUNT_SERVICE_CLIENT, "getAccountSts", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("CDC-ServerLv3_ClientLv3_Method成功")
    @pytest.mark.full
    def test_caseid_1903535(self):
        self.partner = S2sBaseClass([ACCOUNT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(ACCOUNT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACCOUNT_SERVICE_CLIENT, "getAccountSts", {},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("CDC-ServerLv3_ClientLv3_AesKey_Method失败")
    @pytest.mark.full
    def test_caseid_1903534(self):
        get_set_salt("aes_key", "c5e00149cc51620e5179693762679600")
        self.partner = S2sBaseClass([ACCOUNT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(ACCOUNT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACCOUNT_SERVICE_CLIENT, "getAccountSts", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("CDC-ServerLv3_ClientLv3_AesIv_Method失败")
    @pytest.mark.full
    def test_caseid_1903533(self):
        get_set_salt("aes_iv", "7b6d98f7b3058a92a1a32dfaecd70183")
        self.partner = S2sBaseClass([ACCOUNT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(ACCOUNT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACCOUNT_SERVICE_CLIENT, "getAccountSts", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("CDC-ServerLv3_ClientLv3_CmacKey_Method失败")
    @pytest.mark.full
    def test_caseid_1903532(self):
        get_set_salt("cmac_key", __import__("os").environ['XAT_CREDENTIAL_SCAN_FB793EF9B68BACEFA462'])
        self.partner = S2sBaseClass([ACCOUNT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(ACCOUNT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACCOUNT_SERVICE_CLIENT, "getAccountSts", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("CDC-ServerLv2_ClientLv1_Method失败")
    @pytest.mark.full
    def test_caseid_1903531(self):
        backup_service("account_service.jidl")
        update_security_level("account_service.jidl", "getAccountsAuthorityInfo", 1)
        rebuild_soa_partner("account_service.jidl")
        self.partner = S2sBaseClass([ACCOUNT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(ACCOUNT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACCOUNT_SERVICE_CLIENT, "getAccountsAuthorityInfo", {},
                                                  FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("CDC-ServerLv2_ClientLv2_Method成功")
    @pytest.mark.full
    def test_caseid_1903530(self):
        self.partner = S2sBaseClass([ACCOUNT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(ACCOUNT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACCOUNT_SERVICE_CLIENT, "getAccountsAuthorityInfo", {},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("CDC-ServerLv2_ClientLv2_AesKey_Method失败")
    @pytest.mark.full
    def test_caseid_1903529(self):
        get_set_salt("aes_key", "c5e00149cc51620e5179693762679600")
        self.partner = S2sBaseClass([ACCOUNT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(ACCOUNT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACCOUNT_SERVICE_CLIENT, "getAccountsAuthorityInfo", {},
                                                  FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("CDC-ServerLv2_ClientLv2_AesIv_Method失败")
    @pytest.mark.full
    def test_caseid_1903528(self):
        get_set_salt("aes_iv", "7b6d98f7b3058a92a1a32dfaecd70183")
        self.partner = S2sBaseClass([ACCOUNT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(ACCOUNT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACCOUNT_SERVICE_CLIENT, "getAccountsAuthorityInfo", {},
                                                  FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("CDC-ServerLv2_ClientLv2_CmacKey_Method成功")
    @pytest.mark.full
    def test_caseid_1903527(self):
        get_set_salt("cmac_key", __import__("os").environ['XAT_CREDENTIAL_SCAN_9E78AD08D42A16889583'])
        self.partner = S2sBaseClass([ACCOUNT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(ACCOUNT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACCOUNT_SERVICE_CLIENT, "getAccountsAuthorityInfo", {},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("CDC-ServerLv2_ClientLv3_Method失败")
    @pytest.mark.full
    def test_caseid_1903526(self):
        backup_service("account_service.jidl")
        update_security_level("account_service.jidl", "getAccountsAuthorityInfo", 3)
        rebuild_soa_partner("account_service.jidl")
        self.partner = S2sBaseClass([ACCOUNT_SERVICE_CLIENT], domin='tcam')
        self.partner.wait_for_service_reconnect(ACCOUNT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACCOUNT_SERVICE_CLIENT, "getAccountsAuthorityInfo", {},
                                                  FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)
    