#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_encryption.py
@Time         :2023/08/02 17:30:31
@Author       :jingjing.wang@jiduauto.com
@Description  :
"""
import datetime
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
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.sd_tester.send_data([0x22, 0xF1, 0x90])  # 查vin码
        logger.info(self.sd_tester.return_udsdata_and_check_and_print_response_result(
            "Send xxxto get result"))  # 读vindayin出来,打印出来后在not++里面转阿克斯码
        self.tc_vin_list = self.write_vin(self.tc_config['vin'])

    def after_each_func(self, ecu):
        self.bgmcli.get_set_salt()
        self.write_vin(self.tc_config['vin'])
        self.sd_tester.stop_tester_present()
        self.sd_tester.diagnostic_client_sim_close()
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

    def getdatetime(self, minute=1):
        date = self.bgmcli.type_commands('date +"%Y-%m-%d %H:%M:%S"')  # 进入bgm执行命令
        print(date)
        date1 = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        delta_second = 60 * minute - date1.second
        date3 = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
            seconds=delta_second) + datetime.timedelta(hours=8)
        print(date3)
        return int(date3.timestamp()), delta_second

    @allure.title("TCAM-ServerLv2_ClientLv0_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903586(self):
        backup_service("NetWorkService.jidl")
        update_security_level("NetWorkService.jidl", "GetNodeBInfo", 0)
        rebuild_soa_partner("NetWorkService.jidl")
        self.partner = S2sBaseClass([NETSTAT_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(NETSTAT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(NETSTAT_SERVICE_CLIENT, 'GetNodeBInfo', {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("TCAM-ServerLv2_ClientLv1_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903585(self):
        backup_service("NetWorkService.jidl")
        update_security_level("NetWorkService.jidl", "GetNodeBInfo", 1)
        rebuild_soa_partner("NetWorkService.jidl")
        self.partner = S2sBaseClass([NETSTAT_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(NETSTAT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(NETSTAT_SERVICE_CLIENT, 'GetNodeBInfo', {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("TCAM-ServerLv2_ClientLv2_Method成功")
    @pytest.mark.smoke
    @pytest.mark.cdcq
    def test_caseid_1903584(self):
        self.partner = S2sBaseClass([NETSTAT_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(NETSTAT_SERVICE_CLIENT)
        self.partner.send_method_request(
            NETSTAT_SERVICE_CLIENT,
            'GetNodeBInfo', {}, {"out": {"mcc": 460, "mnc": 0}})  # ,"lac":6183,"cid":142709458)

    @allure.title("TCAM-ServerLv2_ClientLv2_AesKey_Method失败")
    @pytest.mark.sanity
    @pytest.mark.cdcq
    def test_caseid_1918660(self):
        get_set_salt("aes_key", "c5e00149cc51620e5179693762679600")
        self.partner = S2sBaseClass([NETSTAT_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(NETSTAT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(NETSTAT_SERVICE_CLIENT, 'GetNodeBInfo', {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("TCAM-ServerLv2_ClientLv2_AesIv_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1919042(self):
        get_set_salt("aes_iv", "7b6d98f7b3058a92a1a32dfaecd70183")
        self.partner = S2sBaseClass([NETSTAT_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(NETSTAT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(NETSTAT_SERVICE_CLIENT, 'GetNodeBInfo', {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("TCAM-ServerLv2_ClientLv2_CmacKey_Method成功")
    @pytest.mark.sanity
    @pytest.mark.cdcq
    def test_caseid_1919038(self):
        get_set_salt("cmac_key", __import__("os").environ['XAT_CREDENTIAL_SCAN_757D959206BE237A384D'])
        self.partner = S2sBaseClass([NETSTAT_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(NETSTAT_SERVICE_CLIENT)
        self.partner.send_method_request(
            NETSTAT_SERVICE_CLIENT,
            'GetNodeBInfo', {}, {"out": {"mcc": 460, "mnc": 0}})  # ,"lac":6183,"cid":142709458)

    @allure.title("TCAM-ServerLv2_ClientLv3_Method失败")
    @pytest.mark.sanity
    @pytest.mark.cdcq
    def test_caseid_1919041(self):
        backup_service("NetWorkService.jidl")
        update_security_level("NetWorkService.jidl", "GetNodeBInfo", 3)
        rebuild_soa_partner("NetWorkService.jidl")
        self.partner = S2sBaseClass([NETSTAT_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(NETSTAT_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(NETSTAT_SERVICE_CLIENT, 'GetNodeBInfo', {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("TCAM-ServerLv1_ClientLv0_Method失败")
    @pytest.mark.sanity
    @pytest.mark.cdcq
    def test_caseid_1919046(self):
        backup_service("RtcAlarmService.jidl")
        update_security_level("RtcAlarmService.jidl", "SetBookEvent", 0)
        rebuild_soa_partner("RtcAlarmService.jidl")
        self.partner = S2sBaseClass([RTCALARM_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RTCALARM_SERVICE_CLIENT)
        start_time, delta_second = self.getdatetime(2)
        timerHandler_config_ifo = \
            self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",
                                                      {"bookEventInfo": {"serviceName": "eat4",
                                                                         "repeatType": 0,
                                                                         "rtcTime": start_time,
                                                                         "timerFlag": "eatapple4",
                                                                         "rtcFlag": False,
                                                                         "bookInfo":
                                                                             {"bookType": "1",
                                                                              "repeatType": 0,
                                                                              "startTime": start_time,
                                                                              "stopTime": start_time + 1000}}},
                                                      timeout=7)[
                "out"]  # 结束时间
        if timerHandler_config_ifo == "":
            assert True
        else:
            assert False

    @allure.title("TCAM-ServerLv1_ClientLv1_Method成功")
    @pytest.mark.smoke
    @pytest.mark.cdcq
    def test_caseid_1919081(self):
        self.partner = S2sBaseClass([RTCALARM_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RTCALARM_SERVICE_CLIENT)
        start_time, delta_second = self.getdatetime(2)
        timerHandler_config_ifo = \
            self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",
                                                      {"bookEventInfo": {"serviceName": "eat4",
                                                                         "repeatType": 0,
                                                                         "rtcTime": start_time,
                                                                         "timerFlag": "eatapple4",
                                                                         "rtcFlag": False,
                                                                         "bookInfo":
                                                                             {"bookType": "1",
                                                                              "repeatType": 0,
                                                                              "startTime": start_time,
                                                                              "stopTime": start_time + 1000}}})[
                "out"]  # 结束时间
        if timerHandler_config_ifo == "":
            assert False
        else:
            assert True

    @allure.title("TCAM-ServerLv1_ClientLv1_AesKey_Method成功")
    @pytest.mark.sanity
    @pytest.mark.cdcq
    def test_caseid_1919093(self):
        get_set_salt("aes_key", "c5e00149cc51620e5179693762679600")
        self.partner = S2sBaseClass([RTCALARM_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RTCALARM_SERVICE_CLIENT)
        start_time, delta_second = self.getdatetime(2)
        timerHandler_config_ifo = \
            self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",
                                                      {"bookEventInfo": {"serviceName": "eat4",
                                                                         "repeatType": 0,
                                                                         "rtcTime": start_time,
                                                                         "timerFlag": "eatapple4",
                                                                         "rtcFlag": False,
                                                                         "bookInfo":
                                                                             {"bookType": "1",
                                                                              "repeatType": 0,
                                                                              "startTime": start_time,
                                                                              "stopTime": start_time + 1000}}})[
                "out"]  # 结束时间
        if timerHandler_config_ifo == "":
            assert False
        else:
            assert True

    @allure.title("TCAM-ServerLv1_ClientLv1_AesIv_Method成功")
    @pytest.mark.smoke
    @pytest.mark.cdcq
    def test_caseid_1919095(self):
        get_set_salt("aes_iv", "7b6d98f7b3058a92a1a32dfaecd70183")
        self.partner = S2sBaseClass([RTCALARM_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RTCALARM_SERVICE_CLIENT)
        start_time, delta_second = self.getdatetime(2)
        timerHandler_config_ifo = \
            self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",
                                                      {"bookEventInfo": {"serviceName": "eat4",
                                                                         "repeatType": 0,
                                                                         "rtcTime": start_time,
                                                                         "timerFlag": "eatapple4",
                                                                         "rtcFlag": False,
                                                                         "bookInfo":
                                                                             {"bookType": "1",
                                                                              "repeatType": 0,
                                                                              "startTime": start_time,
                                                                              "stopTime": start_time + 1000}}})[
                "out"]  # 结束时间
        if timerHandler_config_ifo == "":
            assert False
        else:
            assert True

    @allure.title("TCAM-ServerLv1_ClientLv1_CmacKey_Method成功")
    @pytest.mark.sanity
    @pytest.mark.cdcq
    def test_caseid_1919254(self):
        get_set_salt("cmac_key", __import__("os").environ['XAT_CREDENTIAL_SCAN_D7584C4B99C89D2C5F17'])
        self.partner = S2sBaseClass([RTCALARM_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RTCALARM_SERVICE_CLIENT)
        start_time, delta_second = self.getdatetime(2)
        timerHandler_config_ifo = \
            self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",
                                                      {"bookEventInfo": {"serviceName": "eat4",
                                                                         "repeatType": 0,
                                                                         "rtcTime": start_time,
                                                                         "timerFlag": "eatapple4",
                                                                         "rtcFlag": False,
                                                                         "bookInfo":
                                                                             {"bookType": "1",
                                                                              "repeatType": 0,
                                                                              "startTime": start_time,
                                                                              "stopTime": start_time + 1000}}})[
                "out"]  # 结束时间
        if timerHandler_config_ifo == "":
            assert False
        else:
            assert True

    @allure.title("TCAM-ServerLv1_ClientLv2_Method失败")
    @pytest.mark.sanity
    def test_caseid_1919258(self):
        backup_service("RtcAlarmService.jidl")
        update_security_level("RtcAlarmService.jidl", "SetBookEvent", 2)
        rebuild_soa_partner("RtcAlarmService.jidl")
        self.partner = S2sBaseClass([RTCALARM_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RTCALARM_SERVICE_CLIENT)
        start_time, delta_second = self.getdatetime(2)
        timerHandler_config_ifo = \
            self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",
                                                      {"bookEventInfo": {"serviceName": "eat4",
                                                                         "repeatType": 0,
                                                                         "rtcTime": start_time,
                                                                         "timerFlag": "eatapple4",
                                                                         "rtcFlag": False,
                                                                         "bookInfo":
                                                                             {"bookType": "1",
                                                                              "repeatType": 0,
                                                                              "startTime": start_time,
                                                                              "stopTime": start_time + 1000}}},
                                                      timeout=7)[
                "out"]  # 结束时间
        if timerHandler_config_ifo == "":
            assert True
        else:
            assert False

    @allure.title("TCAM-ServerLv1_ClientLv3_Method失败")
    @pytest.mark.sanity
    @pytest.mark.cdcq
    def test_caseid_1919259(self):
        backup_service("RtcAlarmService.jidl")
        update_security_level("RtcAlarmService.jidl", "SetBookEvent", 3)
        rebuild_soa_partner("RtcAlarmService.jidl")
        self.partner = S2sBaseClass([RTCALARM_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RTCALARM_SERVICE_CLIENT)
        start_time, delta_second = self.getdatetime(2)
        timerHandler_config_ifo = \
            self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",
                                                      {"bookEventInfo": {"serviceName": "eat4",
                                                                         "repeatType": 0,
                                                                         "rtcTime": start_time,
                                                                         "timerFlag": "eatapple4",
                                                                         "rtcFlag": False,
                                                                         "bookInfo":
                                                                             {"bookType": "1",
                                                                              "repeatType": 0,
                                                                              "startTime": start_time,
                                                                              "stopTime": start_time + 1000}}},
                                                      timeout=7)[
                "out"]  # 结束时间
        if timerHandler_config_ifo == "":
            assert True
        else:
            assert False

    @allure.title("TCAM-ServerLv3_ClientLv0_Method失败")
    @pytest.mark.sanity
    @pytest.mark.cdcq
    def test_caseid_1919278(self):
        backup_service("RemoteCtrlService.jidl")
        update_security_level("RemoteCtrlService.jidl", "GetRemoteAuthStartSts", 0)
        rebuild_soa_partner("RemoteCtrlService.jidl")
        self.partner = S2sBaseClass([REMOTECTRL_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(REMOTECTRL_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartSts", {},
                                                  FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("TCAM-ServerLv3_ClientLv1_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903571(self):
        backup_service("RemoteCtrlService.jidl")
        update_security_level("RemoteCtrlService.jidl", "GetRemoteAuthStartSts", 1)
        rebuild_soa_partner("RemoteCtrlService.jidl")
        self.partner = S2sBaseClass([REMOTECTRL_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(REMOTECTRL_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartSts", {},
                                                  FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("TCAM-ServerLv3_ClientLv2_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903570(self):
        backup_service("RemoteCtrlService.jidl")
        update_security_level("RemoteCtrlService.jidl", "GetRemoteAuthStartSts", 2)
        rebuild_soa_partner("RemoteCtrlService.jidl")
        self.partner = S2sBaseClass([REMOTECTRL_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(REMOTECTRL_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartSts", {},
                                                  FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("TCAM-ServerLv3_ClientLv3_Method成功")
    @pytest.mark.smoke
    @pytest.mark.cdcq
    def test_caseid_1903569(self):
        self.partner = S2sBaseClass([REMOTECTRL_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(REMOTECTRL_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartSts", {},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("TCAM-ServerLv3_ClientLv3_AesKey_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903568(self):
        get_set_salt("aes_key", "c5e00149cc51620e5179693762679600")
        self.partner = S2sBaseClass([REMOTECTRL_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(REMOTECTRL_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartSts", {},
                                                  FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("TCAM-ServerLv3_ClientLv3_AesIv_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903567(self):
        get_set_salt("aes_iv", "7b6d98f7b3058a92a1a32dfaecd70183")
        self.partner = S2sBaseClass([REMOTECTRL_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(REMOTECTRL_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartSts", {},
                                                  FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("TCAM-ServerLv3_ClientLv3_CmacKey_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903566(self):
        get_set_salt("cmac_key", __import__("os").environ['XAT_CREDENTIAL_SCAN_142E9CDBD220F8E08352'])
        self.partner = S2sBaseClass([REMOTECTRL_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(REMOTECTRL_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartSts", {},
                                                  FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("ACU-ServerLv3_ClientLv0_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903565(self):
        backup_service("RPAAPAService.jidl")
        update_security_level("RPAAPAService.jidl", "GetAPARemoteInfo", 0)
        rebuild_soa_partner("RPAAPAService.jidl")
        self.partner = S2sBaseClass([RPAAPA_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RPAAPA_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(RPAAPA_SERVICE_CLIENT, "GetAPARemoteInfo", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("ACU-ServerLv3_ClientLv1_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903564(self):
        backup_service("RPAAPAService.jidl")
        update_security_level("RPAAPAService.jidl", "GetAPARemoteInfo", 1)
        rebuild_soa_partner("RPAAPAService.jidl")
        self.partner = S2sBaseClass([RPAAPA_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RPAAPA_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(RPAAPA_SERVICE_CLIENT, "GetAPARemoteInfo", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("ACU-ServerLv3_ClientLv2_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903563(self):
        backup_service("RPAAPAService.jidl")
        update_security_level("RPAAPAService.jidl", "GetAPARemoteInfo", 2)
        rebuild_soa_partner("RPAAPAService.jidl")
        self.partner = S2sBaseClass([RPAAPA_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RPAAPA_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(RPAAPA_SERVICE_CLIENT, "GetAPARemoteInfo", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("ACU-ServerLv3_ClientLv3_Method成功")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903562(self):
        self.partner = S2sBaseClass([RPAAPA_SERVICE_CLIENT], domin='cdcq')
        # self.partner.wait_for_service_reconnect(RPAAPA_SERVICE_CLIENT)
        sleep(10000)
        self.partner.send_request_and_ck_failtype(RPAAPA_SERVICE_CLIENT, "GetAPARemoteInfo", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("ACU-ServerLv3_ClientLv3_AesKey_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903561(self):
        get_set_salt("aes_key", "c5e00149cc51620e5179693762679600")
        self.partner = S2sBaseClass([RPAAPA_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RPAAPA_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(RPAAPA_SERVICE_CLIENT, "GetAPARemoteInfo", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("ACU-ServerLv3_ClientLv3_AesIv_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903560(self):
        get_set_salt("aes_iv", "7b6d98f7b3058a92a1a32dfaecd70183")
        self.partner = S2sBaseClass([RPAAPA_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RPAAPA_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(RPAAPA_SERVICE_CLIENT, "GetAPARemoteInfo", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("ACU-ServerLv3_ClientLv3_CmacKey_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903559(self):
        get_set_salt("cmac_key", __import__("os").environ['XAT_CREDENTIAL_SCAN_E4B21F88A779656ED094'])
        self.partner = S2sBaseClass([RPAAPA_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RPAAPA_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(RPAAPA_SERVICE_CLIENT, "GetAPARemoteInfo", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("ACU-ServerLv2_ClientLv0_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903558(self):
        backup_service("RPAAPAService.jidl")
        update_security_level("RPAAPAService.jidl", "GetPARemoteStatus", 0)
        rebuild_soa_partner("RPAAPAService.jidl")
        self.partner = S2sBaseClass([RPAAPA_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RPAAPA_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(RPAAPA_SERVICE_CLIENT, "GetPARemoteStatus", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("ACU-ServerLv2_ClientLv1_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903557(self):
        backup_service("RPAAPAService.jidl")
        update_security_level("RPAAPAService.jidl", "GetPARemoteStatus", 1)
        rebuild_soa_partner("RPAAPAService.jidl")
        self.partner = S2sBaseClass([RPAAPA_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RPAAPA_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(RPAAPA_SERVICE_CLIENT, "GetPARemoteStatus", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("ACU-ServerLv2_ClientLv2_Method成功")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903556(self):
        self.partner = S2sBaseClass([RPAAPA_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RPAAPA_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(RPAAPA_SERVICE_CLIENT, "GetPARemoteStatus", {},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("ACU-ServerLv2_ClientLv2_AesKey_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903555(self):
        get_set_salt("aes_key", "c5e00149cc51620e5179693762679600")
        self.partner = S2sBaseClass([RPAAPA_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RPAAPA_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(RPAAPA_SERVICE_CLIENT, "GetPARemoteStatus", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("ACU-ServerLv2_ClientLv2_AesIv_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903554(self):
        get_set_salt("aes_iv", "7b6d98f7b3058a92a1a32dfaecd70183")
        self.partner = S2sBaseClass([RPAAPA_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RPAAPA_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(RPAAPA_SERVICE_CLIENT, "GetPARemoteStatus", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("ACU-ServerLv2_ClientLv2_CmacKey_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903553(self):
        get_set_salt("cmac_key", __import__("os").environ['XAT_CREDENTIAL_SCAN_E0AB787D69982DC50C2D'])
        self.partner = S2sBaseClass([RPAAPA_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RPAAPA_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(RPAAPA_SERVICE_CLIENT, "GetPARemoteStatus", {},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("ACU-ServerLv2_ClientLv3_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903552(self):
        backup_service("RPAAPAService.jidl")
        update_security_level("RPAAPAService.jidl", "GetPARemoteStatus", 3)
        rebuild_soa_partner("RPAAPAService.jidl")
        self.partner = S2sBaseClass([RPAAPA_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(RPAAPA_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(RPAAPA_SERVICE_CLIENT, "GetPARemoteStatus", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("ACU-ServerLv1_ClientLv0_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903551(self):
        update_security_level("AVP.jidl", "GetAVPParkingInfo", 0)
        self.partner = S2sBaseClass([AVP_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(AVP_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(AVP_SERVICE_CLIENT, "GetAVPParkingInfo", {},
                                                  FailType.FAILTYPE_TIMEOUT,
                                                  timeout=6)

    @allure.title("ACU-ServerLv1_ClientLv1_Method成功")
    @pytest.mark.smoke
    @pytest.mark.cdcq
    def test_caseid_1903550(self):
        self.partner = S2sBaseClass([ANPMRC_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(ANPMRC_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ANPMRC_SERVICE_CLIENT, "GetMRCSts", {},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("ACU-ServerLv1_ClientLv1_AesKey_Method成功")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903549(self):
        get_set_salt("aes_key", "c5e00149cc51620e5179693762679600")
        self.partner = S2sBaseClass([ACC_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(ACC_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACC_SERVICE_CLIENT, "GetFollowDistanceLevel", {},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("ACU-ServerLv1_ClientLv1_AesIv_Method成功")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903548(self):
        get_set_salt("aes_iv", "7b6d98f7b3058a92a1a32dfaecd70183")
        self.partner = S2sBaseClass([ACC_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(ACC_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACC_SERVICE_CLIENT, "GetFollowDistanceLevel", {},
                                                  FailType.FAILTYPE_SUCCESS, timeout=6)

    @allure.title("ACU-ServerLv1_ClientLv1_CmacKey_Method成功")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903547(self):
        get_set_salt("cmac_key", __import__("os").environ['XAT_CREDENTIAL_SCAN_45DF31CBA83FD34EA4DE'])
        self.partner = S2sBaseClass([ACC_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(ACC_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACC_SERVICE_CLIENT, "GetFollowDistanceLevel", {},
                                                  FailType.FAILTYPE_SUCCESS)

    @allure.title("ACU-ServerLv1_ClientLv2_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903546(self):
        backup_service("ACCService.jidl")
        update_security_level("ACCService.jidl", "GetFollowDistanceLevel", 3)
        rebuild_soa_partner("ACCService.jidl")
        self.partner = S2sBaseClass([ACC_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(ACC_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACC_SERVICE_CLIENT, "GetFollowDistanceLevel", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)

    @allure.title("ACU-ServerLv1_ClientLv3_Method失败")
    @pytest.mark.full
    @pytest.mark.cdcq
    def test_caseid_1903545(self):
        backup_service("ACCService.jidl")
        update_security_level("ACCService.jidl", "GetFollowDistanceLevel", 3)
        rebuild_soa_partner("ACCService.jidl")
        self.partner = S2sBaseClass([ACC_SERVICE_CLIENT], domin='cdcq')
        self.partner.wait_for_service_reconnect(ACC_SERVICE_CLIENT)
        self.partner.send_request_and_ck_failtype(ACC_SERVICE_CLIENT, "GetFollowDistanceLevel", {},
                                                  FailType.FAILTYPE_TIMEOUT, timeout=6)