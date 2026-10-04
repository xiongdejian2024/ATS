#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_
"""
@File: test_BlueToothService.py
@Time: 2023/02/04 08:00
@Author: jingjing.wang
@Description: Test SOA service about BlueToothService
"""
import pytest

from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.common.logmanagment.logmanager import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester


@allure.feature("SOA服务接口")
@allure.story("互联服务/BlueToothService")
@pytest.mark.tcam
class TestBlueToothService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.sd_tester.tester_present()
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        # 启动partner operator
        self.partner = S2sBaseClass([("BlueToothService", "client")])
        self.partner.method_default_timeout = 0.1

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.sd_tester.change_car_mode(0, do_assert=1)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        sleep(1)
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        # self.nucapp.bgm_power_on()
        super().after_class(self, ecu)

    def func(self, data):
        rev_msg_0x31A_data = ()
        logger.info("rec_data is {}".format(data))
        self.rev_msg_0x31A_data = data

    @allure.title("设置蓝牙传输整车数据_4095字节")
    @pytest.mark.full
    def test_caseid_108871(self):
        send_data = []
        for i in range(4094):
            send_data.append(random.randint(0, 9))

        with allure.step(
                f"Step:模拟BluetoothService client调用SetBLEVehData接口发送4095bytes数据"
        ):
            self.partner.send_method_request(
                'BlueToothService_client',
                'SetBLEVehData',
                {"data": send_data},
            )

        with allure.step(f"查看ConnectivityCANFD上message 0x31A报文接收情况"):
            recv_data = self.ipdu.recv_pdu("connectivitycanfd", 0x31A)
            logger.info("接收到的ConnectivityCANFD上message 0x31A报文是{}".format(recv_data))
            if recv_data == None:
                assert False
            else:
                if recv_data[3][1] + ((recv_data[3][0] & 0x0F) << 8) == len(send_data):
                    assert True
                else:
                    assert False
            recv_data = recv_data[3]
            recv_data.pop(0)
            recv_data.pop(0)
            logger.info("接收到的ConnectivityCANFD上message 0x31A报文是{}".format(recv_data))

            self.ipdu.send_pdu(
                "connectivitycanfd",
                0x33A,
                [0x30, 0x00, 0x14, 0x00, 0x00, 0x00, 0x00, 0x00],
            )
            recv_data1_list = []
            for i in range(64):
                recv_data1 = self.ipdu.recv_pdu("connectivitycanfd", 0x31A)
                recv_data1 = recv_data1[3]
                recv_data1 = list(recv_data1)
                recv_data1.pop(0)
                recv_data1_list += recv_data1

            recv_data1_list = recv_data + recv_data1_list
            logger.info("接收到的ConnectivityCANFD上message 0x31A报文是{}".format(recv_data1_list))

            if send_data == recv_data1_list:
                logger.info("蓝牙传输整车数据完全")
            else:
                logger.info("蓝牙传输整车数据有误")
            sleep(5)

    @allure.title("获取/通知AVP蓝牙连接状态_连接/通信故障")
    @pytest.mark.sanity
    def test_caseid_110850(self):
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEConStsForAVP', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEConStsForAVP', 1)
        self.partner.ck_s2s_event(BLUETOOTH_SERVICE_CLIENT, "ConStsForAVP", {"sts": True})
        self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetConStsForAVP", {}, {"out": True})
        self.ipdu.pause_bus_send("connectivitycanfd")
        logger.info(time.time())
        self.partner.ck_s2s_event(BLUETOOTH_SERVICE_CLIENT, "ConStsForAVP", {"sts": False},timeout=2.2)
        self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetConStsForAVP", {}, {"out": False})
        self.ipdu.resume_bus_send("connectivitycanfd")
        logger.info(time.time())
        self.partner.ck_s2s_event(BLUETOOTH_SERVICE_CLIENT, "ConStsForAVP", {"sts": True})
        self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetConStsForAVP", {}, {"out": True})

    @allure.title("设置蓝牙传输整车数据_65字节")
    @pytest.mark.smoke
    def test_caseid_1979766(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(5)
        try:
            send_data = [random.randint(0, 255) for _ in range(65)]  # 随机数+65帧有效数据
            logger.info(f"发送数据>>> {bytes(send_data).hex()}")
            with allure.step(f"Step:模拟BluetoothService client调用SetBLEVehData接口发送65bytes数据"):
                self.partner.send_method_request(BLUETOOTH_SERVICE_CLIENT, 'SetBLEVehData', {"data": send_data})
            with allure.step(f"查看ConnectivityCANFD上message 0x31A报文接收情况"):
                recv_data_info = self.ipdu.recv_pdu("connectivitycanfd", 0x31A)
                
                logger.info(
                    f"接收到的ConnectivityCANFD首帧上message len={len(recv_data_info)}  0x31A报文是{recv_data_info}")
                recv_data0 = recv_data_info[3]  # 接收0x31A报文数据,0canid,1时间戳,2长度,3数据内容[]

                logger.info(f"接收到的ConnectivityCANFD第4帧上message len={len(recv_data0)}  0x31A报文是{recv_data0}")
                self.ipdu.send_pdu("connectivitycanfd", 0x33A, data=[0x30, 0, 5, 0, 0, 0, 0, 0])  # 模拟bncm的发送流控帧

                recv_data_list = self.ipdu.recv_pdu("connectivitycanfd", 0x31A)
                recv_data1 = recv_data_list[3]  # 接收0x31A报文数据,0canid,1时间戳,2长度,3数据内容[]
                logger.info(f"接收到的ConnectivityCANFD上message len={len(recv_data1)} 0x31A报文是{recv_data1}")

                recv_data = recv_data0[2:] + recv_data1[1:4]  # 拿出recv_data0后面的63个字节, 拿出recv_data1剩余的3个字节
                logger.info(f"接收到的ConnectivityCANFD上message len={len(recv_data)} 0x31A报文是{recv_data}")
                assert send_data == recv_data
        except Exception as e:
            logger.error(f" eroor{str(e)}")
            sleep(5)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            assert 0,str(e)
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.get_signal_values("BLEVehDataUpdEth")

    @allure.title("获取/通知蓝牙移动设备状态_正常/通话/重启event")
    @pytest.mark.sanity
    def test_caseid_1979749(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEMobDevSts', 1)
        self.partner.empty_all(0.5)
        for i in range(2):
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEMobDevSts', i)
            self.partner.ck_s2s_event(BLUETOOTH_SERVICE_CLIENT, "MobDevSts", {"sts": i})
            self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetMobDevSts", {}, {"out": i})
        self.restart_bgm_and_connect_service(BLUETOOTH_SERVICE_CLIENT)
        self.partner.ck_s2s_event(BLUETOOTH_SERVICE_CLIENT, "MobDevSts", {"sts": 1})
        self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetMobDevSts", {}, {"out": 1})

    @allure.title("获取/通知AVP蓝牙连接状态_未连接/通信故障")
    @pytest.mark.sanity
    def test_caseid_1979771(self):
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEConStsForAVP', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEConStsForAVP', 0)
        self.partner.ck_s2s_event(BLUETOOTH_SERVICE_CLIENT, "ConStsForAVP", {"sts": False})
        self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetConStsForAVP", {}, {"out": False})
        self.ipdu.pause_bus_send("connectivitycanfd")
        sleep(2)
        self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetConStsForAVP", {}, {"out": False})
        self.ipdu.resume_bus_send("connectivitycanfd")
        sleep(2)
        self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetConStsForAVP", {}, {"out": False})

    @allure.title("获取/通知蓝牙移动设备状态_正常/通话/other保持last value")
    @pytest.mark.full
    def test_caseid_1979790(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEMobDevSts', 1)
        self.partner.empty_all(0.5)
        for i in range(2):
            logger.info(f"信号{i}")
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEMobDevSts', i)
            self.partner.ck_s2s_event(BLUETOOTH_SERVICE_CLIENT, "MobDevSts", {"sts": i})
            self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetMobDevSts", {}, {"out": i})
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEMobDevSts', 2)
            self.partner.ck_no_event(BLUETOOTH_SERVICE_CLIENT, "MobDevSts")
            self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetMobDevSts", {}, {"out": i})

    @allure.title("获取/通知蓝牙移动设备状态_正常0/通话1/默认值")
    @pytest.mark.sanity
    def test_caseid_1979777(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEMobDevSts', 1)
        self.partner.empty_all(0.5)
        for i in range(2):
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEMobDevSts', i)
            self.partner.ck_s2s_event(BLUETOOTH_SERVICE_CLIENT, "MobDevSts", {"sts": i})
            self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetMobDevSts", {}, {"out": i})
            self.restart_bgm_and_connect_service(BLUETOOTH_SERVICE_CLIENT, resume_all_bus=False)
            sleep(2)
            self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetMobDevSts", {}, {"out": 0})
            self.ipdu.resume_all_bus_send()
            self.partner.ck_s2s_event(BLUETOOTH_SERVICE_CLIENT, "MobDevSts", {"sts":i})
            self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetMobDevSts", {}, {"out": i})

    @allure.title("获取/通知蓝牙移动设备状态_正常0/通话1/重启event")
    @pytest.mark.full
    def test_caseid_1984542(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEMobDevSts', 1)
        self.partner.empty_all(0.5)
        for i in range(2):
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEMobDevSts', i)
            self.partner.ck_s2s_event(BLUETOOTH_SERVICE_CLIENT, "MobDevSts", {"sts": i})
            self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetMobDevSts", {}, {"out": i})
            self.restart_bgm_and_connect_service(BLUETOOTH_SERVICE_CLIENT)
            self.partner.ck_s2s_event(BLUETOOTH_SERVICE_CLIENT, "MobDevSts", {"sts":i})
            self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetMobDevSts", {}, {"out": i})

    @allure.title("获取/通知蓝牙移动设备状态_正常0/通话1/默认值")
    @pytest.mark.full
    def test_caseid_1979789(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEMobDevSts', 1)
        self.partner.empty_all(0.5)
        for i in range(2):
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEMobDevSts', i)
            self.partner.ck_s2s_event(BLUETOOTH_SERVICE_CLIENT, "MobDevSts", {"sts": i})
            self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetMobDevSts", {}, {"out": i})
            self.ipdu.pause_all_bus_send()
            sleep(2)
            self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetMobDevSts", {}, {"out": i})
            self.ipdu.resume_all_bus_send()
            self.partner.send_request_and_ck_resp(BLUETOOTH_SERVICE_CLIENT, "GetMobDevSts", {}, {"out": i})

    @allure.title("设置蓝牙传输整车数据_1字节")
    @pytest.mark.full
    def test_caseid_108882(self):
        self.rev_msg_0x31A_data = ()

        with allure.step(f"S查看ConnectivityCANFD上message 0x31A报文接收情况"):
            result = self.ipdu.recv_pdu_thread_start(
                "connectivitycanfd", 794, self.func
            )

        with allure.step(f"Step:模拟BluetoothService client调用SetBLEVehData接口发送1bytes数据"):
            self.partner.send_method_request(
                'BlueToothService_client',
                'SetBLEVehData',
                {"data": [1]},
            )
        sleep(2)
        logger.info(
            "接收到的ConnectivityCANFD上message 0x31A报文是{}".format(self.rev_msg_0x31A_data)
        )
        if self.rev_msg_0x31A_data == ():
            assert False
        else:
            if self.rev_msg_0x31A_data[3][1] == 1:
                assert True
            else:
                assert False
        sleep(5)
