#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
**********************
@File    : ProtoclKeywords.py

**********************

------------------------------------------------------------------
@Time    : 2024/7/10 10:56
@Author  : jiewen.deng
Language: Python 3.9
------------------------------------------------------------------
Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.
"""
import os
import time
from copy import deepcopy
from threading import Thread

from xat_ecu.legacy.utils.utils import *
from xat_ecu.legacy.socket_client.SocketData import SocketData
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.protocol.ProtocolParser import *
from xat_ecu.legacy.protocol.ProtocolConfigData import *
from xat_ecu.legacy.sdk.diagnosis.uds_securitycal import SecurityAlgorithm
from xat_ecu.legacy.protocol.DoipClientGateway import DoipClientGateway
from xat_ecu.legacy.driver.ssh_interface import command_send, file_upload


class ProtocolClientKeywords(object):

    def __init__(self, protocol_type="doip", uds_host="169.254.19.1", uds_port=13400):
        self.protocol_type = protocol_type
        self.keep_session_flag = False
        self.sec = SecurityAlgorithm('BGM')
        self.mock_relay_0x0008_data = None
        self.doip_sock_obj = DoipClientGateway(uds_host, uds_port)

    def start_udp_connect(self):
        self.doip_sock_obj.new_udp_connect_start()
        time.sleep(2)

    def start_tcp_connect(self, auto_activate_route=True, wait_start_time=0.5, wait_route_activate_time=2, after_connect=False):
        self.doip_sock_obj.new_tcp_connect_start(after_connect)
        time.sleep(wait_start_time)
        if auto_activate_route:
            self.doip_generate_service_0x0005(check_res_code=0x10)
            time.sleep(wait_route_activate_time)
            self.send_3e_80_data()

    def start_udp_broadcast_connect(self):
        self.doip_sock_obj.new_udp_broadcast_connect_start()

    def stop_udp_broadcast_connect(self):
        if hasattr(self.doip_sock_obj.udp_broadcast_client_sock, "stop_broad_cast"):
            self.doip_sock_obj.udp_broadcast_client_sock.stop_broad_cast()

    def stop_udp_connect(self):
        if hasattr(self.doip_sock_obj.udp_client_sock, "stop"):
            self.doip_sock_obj.udp_client_sock.stop()

    def stop_tcp_connect(self):
        if hasattr(self.doip_sock_obj.tcp_client_sock, "stop"):
            self.doip_sock_obj.tcp_client_sock.stop()

    def init_middleware(self):
        p_type = str(self.protocol_type).lower()
        if p_type == "doip":
            pass
        elif p_type == "can":
            pass
        elif p_type == "fr":
            pass

    def check_tcp_client_connect_status(self, status):
        """
        检查tcp client端状态
        :param status: True:连接，False:断开
        """
        if status != self.doip_sock_obj.tcp_client_sock.socket_connect_status:
            raise AssertionError(f"tcp status:{self.doip_sock_obj.tcp_client_sock.socket_connect_status}"
                                 f",expect status:{status}")

    def check_udp_broadcast_host(self, check_host, check_port=None):
        """
        检测车辆广播服务端的Host
        :param check_host: 检查的host:"255.255.255.255"
        :param check_port: 检测的port: 13400
        """
        host_info = self.doip_sock_obj.get_current_broadcast_host()
        if check_host:
            if host_info[0] != check_host:
                raise AssertionError(f"broadcast host is:{host_info[0]}, but expect:{check_host}")
        if check_port:
            if host_info[1] != check_port:
                raise AssertionError(f"broadcast port is:{host_info[1]}, but expect:{check_port}")

    def check_vehicle_broadcast_interval_and_times(self,
                                                   check_time_interval=None,
                                                   check_times=None,
                                                   time_interval_offset=0.1,
                                                   times_offset=2,
                                                   specify_time=5):
        """
        检测车辆广播次数和时间间隔
        :param check_time_interval: 检测接收车辆广播的时间间隔：check_time_interval=1
        :param check_times: 检测接收车辆广播的次数：check_times=5
        :param time_interval_offset: 广播时间间隔允许偏移误差
        :param times_offset: 广播次数允许偏移误差
        :param specify_time: 指定多少秒内的数据
        """
        data_list = self.doip_sock_obj.get_udp_broadcast_data(specify_time)
        if check_times:
            recv_times = len(data_list)
            if abs(recv_times - check_times) > times_offset:
                logger.warning(f"收到次数：{recv_times}，期望次数：{check_times}")
                raise AssertionError(f"收到次数：{recv_times}，期望次数：{check_times}")
        if check_time_interval:
            first_time = data_list.pop(0)
            for ac_time in data_list:
                if abs(round(ac_time - first_time, 1) - check_time_interval) > time_interval_offset:
                    logger.warning(f"Real time interval is:{round(ac_time - first_time, 1)}, "
                                   f"expect times is:{check_time_interval}")
                    raise AssertionError(f"Real time interval is:{round(ac_time - first_time, 1)}, "
                                         f"expect times is:{check_time_interval}")
                first_time = ac_time

    def check_current_udp_broadcast_data(self,
                                         check_vin=None,
                                         check_logical_address=None,
                                         check_eid=None,
                                         check_gid=None,
                                         check_further_action_required=None):
        """
        车辆广播数据校验
        :param check_vin: 检验vin
        :param check_logical_address: 检验check_logical_address，eg:0x0e80
        :param check_eid: 检验check_eid, eg: 000000000001
        :param check_gid: 检验check_gid, eg: 000000000001
        :param check_further_action_required: 检验check_further_action_required,eg:0
        """

        broadcast_data = self.doip_sock_obj.get_current_udp_broadcast_data()
        data_obj = doip_parse(list(broadcast_data.values())[0])
        if check_vin:
            if check_vin != data_obj.DataInfo.Vin:
                logger.warning(f"vin得到：{data_obj.DataInfo.Vin},期望：{check_vin}")
                assert False
        if check_logical_address:
            if check_logical_address != data_obj.DataInfo.LogicalAddress:
                logger.warning(f"LogicalAddress得到：{hex(data_obj.DataInfo.LogicalAddress)},期望：{hex(check_logical_address)}")
                assert False
        if check_eid:
            if check_eid != data_obj.DataInfo.EID.hex():
                logger.warning(
                    f"EID得到：{data_obj.DataInfo.EID.hex()},期望：{check_eid}")
                assert False
        if check_gid:
            if check_gid != data_obj.DataInfo.GID.hex():
                logger.warning(
                    f"GID得到：{data_obj.DataInfo.GID.hex()},期望：{check_gid}")
                assert False
        if check_further_action_required:
            if check_further_action_required != data_obj.DataInfo.FurtherActionRequired:
                logger.warning(
                    f"FurtherActionRequired得到：{data_obj.DataInfo.FurtherActionRequired},期望：{check_further_action_required}")
                assert False

    def send_3e_80_data(self, interval=2):
        if not self.keep_session_flag:
            self.keep_session_flag = True
            Thread(target=self.__send_3e_80_data, args=(interval, ), daemon=True).start()

    def stop_3e_80_data(self):
        """
        停止发送3e80
        """
        self.keep_session_flag = False

    def mock_relay_data_0x0008(self, source_address):
        """
        响应那个逻辑地址是否在线
        :param source_address: 如0e80逻辑地址在线：0x0e80
        """
        data = deepcopy(doip_frame_raw_data_0x0008)
        if source_address:
            data["DataInfo"] = source_address
        self.mock_relay_0x0008_data = doip_build(data)

    def auto_handle_tcp_data(self, interval_time=0.5):
        Thread(target=self._auto_handle_tcp_data, args=(interval_time,), daemon=True).start()

    def _auto_handle_tcp_data(self, interval_time):
        while not self.doip_sock_obj.tcp_client_sock.is_stop:
            iter_data = SocketData.TCP_CLIENT_DATA[self.doip_sock_obj.tcp_client_sock]
            if not iter_data:
                continue
            result = self.doip_sock_obj.split_package_data(reduce(lambda x, y: x + y, iter_data))
            if result is None:
                continue
            for data in result:
                data_obj = doip_parse(data)
                if data_obj.DataType == 0x0007:
                    if self.mock_relay_0x0008_data:
                        self.doip_sock_obj.tcp_client_sock.async_send_message(self.mock_relay_0x0008_data)

            time.sleep(interval_time)
        logger.info(f"exit auto handle tcp data.")

    def __send_3e_80_data(self, interval):
        data = deepcopy(doip_frame_raw_data_0x8001)
        data['DataInfo']['TargetAddress'] = 0x1fff
        data['DataLen'] = 6
        data['DataInfo']['DiagData'] = bytes([0x3e, 0x80])
        raw_data = doip_build(data)
        while not self.doip_sock_obj.tcp_client_sock.is_stop and self.keep_session_flag:
            self.doip_sock_obj.tcp_client_sock.async_send_message(raw_data)
            time.sleep(interval)

    def doip_generate_service_0x0000(self):
        data = deepcopy(doip_frame_raw_data_0x0000)
        doip_data_0x0000 = doip_build(data)
        return doip_data_0x0000

    def reset_tcp_sock_start_time(self):
        self.doip_sock_obj.tcp_client_sock.reset_sock_start_time()

    def check_tcp_sock_start_to_close_time(self, check_time=0, offset=1):
        time_data = self.doip_sock_obj.tcp_client_sock.get_sock_start_to_close_time()
        if abs(round(time_data - check_time, 1)) > offset:
            logger.warning(f"check time failed,get time is:{time_data},bug expect time is:{check_time}")
            raise AssertionError(f"check time failed,get time is:{time_data},bug expect time is:{check_time}")
        logger.info(f"get time sock start to close is:{time_data}, expect time is:{check_time}")

    def doip_generate_service_0x0001(self, check_vin=None,
                                     check_logical_address=None,
                                     check_eid=None,
                                     check_gid=None,
                                     except_relay_none=False,
                                     check_further_action_required=None):
        """
        车辆识别请求
        """
        data = deepcopy(doip_frame_raw_data_0x0001)
        doip_data_0x0001 = doip_build(data)
        doip_type = doip_req_to_res_map.get(data.get("DataType"))
        response_result = self.doip_sock_obj.send_and_get_callback_data(doip_data_0x0001, doip_type, socket_type="udp")
        if not response_result:
            if except_relay_none:
                return
            raise AssertionError(f"发送车辆请求后，未收到回复")

        if response_result.DataType == 0:
            logger.warning(f"发送车辆请求后，收到报文头否定响应，code:{response_result.DataInfo}")
            return
        # logger.info(f"请求0x0001,返回的响应是：\n{response_result}")
        if check_vin:
            assert check_vin == response_result.DataInfo.Vin
        if check_logical_address:
            assert check_logical_address == response_result.DataInfo.LogicalAddress
        if check_eid:
            assert check_eid == response_result.DataInfo.EID.hex()
        if check_gid:
            assert check_gid == response_result.DataInfo.GID.hex()
        if check_further_action_required:
            assert check_further_action_required == response_result.DataInfo.FurtherActionRequired

    def doip_generate_service_0x0002(self, eid,
                                     check_vin=None,
                                     check_logical_address=None,
                                     check_eid=None,
                                     check_gid=None,
                                     except_relay_none=False,
                                     check_further_action_required=None):
        """
        eid : 000000000001 车辆带eid的请求
        """
        data = deepcopy(doip_frame_raw_data_0x0002)
        data["DataInfo"] = bytes.fromhex(eid)
        doip_data_0x0002 = doip_build(data)
        doip_type = doip_req_to_res_map.get(data.get("DataType"))
        response_result = self.doip_sock_obj.send_and_get_callback_data(doip_data_0x0002, doip_type, socket_type="udp")
        if not response_result:
            if except_relay_none:
                return
            raise AssertionError(f"发送车辆请求后，未收到回复")

        if response_result.DataType == 0:
            logger.warning(f"发送车辆请求后，收到报文头否定响应，code:{response_result.DataInfo}")
            return
        # logger.info(f"请求0x0002,返回的响应是：\n{response_result}")
        if check_vin:
            assert check_vin == response_result.DataInfo.Vin
        if check_logical_address:
            assert check_logical_address == response_result.DataInfo.LogicalAddress
        if check_eid:
            assert check_eid == response_result.DataInfo.EID.hex()
        if check_gid:
            assert check_gid == response_result.DataInfo.GID.hex()
        if check_further_action_required:
            assert check_further_action_required == response_result.DataInfo.FurtherActionRequired

    def doip_send_raw_data(self,
                           raw_data,
                           send_type='tcp',
                           except_relay_none=False,
                           check_return_data=None,
                           need_expect_type=None,
                           check_na_code=None
                           ):
        """
        请求路由激活
        :param raw_data: 02fd00000000000104
        :param send_type: tcp: tcp发送数据；udp: udp发送数据
        :param except_relay_none: 期待不回复默认False
        :param check_na_code: 期望返回否定码
        :param check_return_data: 检查返回的数据
                                  如： 02fd8001000610e8010015003
                                  或者：[02fd8002000410e801001, 02fd8001000610e8010015003]
        :param need_expect_type: 类型是：list
                                期待回复数据得所有类型，如期待返回诊断正响应，都会先回复8002,在回复8001:[0x8001, 0x8002];
                                如果希望返回NACK 则是：[0x8003]
                                希望返回协议上的否定响应,则是：[0x0000]
        """
        if not except_relay_none:
            if need_expect_type is None:
                need_expect_type = [0x8001, 0x8002]
        else:
            if need_expect_type is None:
                need_expect_type = [0xFFFF]
        response_result = self.doip_sock_obj.send_and_get_callback_data(
            bytes.fromhex(raw_data),
            [
                0x0000,
                0x8001,
                0x8002,
                0x8003,
                0x0004,
                0x0006,
                0x0008,
                0x4002,
                0x4004
            ],
            socket_type=send_type,
            need_expect_type=need_expect_type
        )
        if except_relay_none:
            if response_result:
                raise AssertionError(f"期待不回复，实际得到：{response_result}")
            else:
                return

        if not isinstance(response_result, list):
            response_result = [response_result]
        for d_result in response_result:
            if d_result.DataType == 0:
                if check_na_code:
                    if check_na_code != d_result.DataInfo:
                        logger.warning(f"got code:{d_result.DataInfo}, expect code:{check_na_code}")
                        raise AssertionError(f"got code:{d_result.DataInfo}, expect code:{check_na_code}")
            if d_result.DataType == 0x8003:
                if check_na_code:
                    if check_na_code != d_result.DataInfo.NRCCode:
                        logger.warning(f"got code:{d_result.DataInfo.NRCCode}, expect code:{check_na_code}")
                        raise AssertionError(f"got code:{d_result.DataInfo.NRCCode}, expect code:{check_na_code}")

        if check_return_data:
            all_return_data = [doip_build(i).hex() for i in response_result]
            for i in check_return_data:
                if i not in all_return_data:
                    logger.error(f"return data not contain {i}")
                    raise AssertionError(f"return data not contain {i}")

    def doip_generate_service_0x0003(self, vin,
                                     check_vin=None,
                                     check_logical_address=None,
                                     check_eid=None,
                                     check_gid=None,
                                     except_relay_none=False,
                                     check_further_action_required=None):
        """
        vin : LSTEST6R9F2086669 车辆带vin的请求
        """
        data = deepcopy(doip_frame_raw_data_0x0003)
        data["DataInfo"] = vin
        doip_data_0x0003 = doip_build(data)
        doip_type = doip_req_to_res_map.get(data.get("DataType"))
        response_result = self.doip_sock_obj.send_and_get_callback_data(doip_data_0x0003, doip_type, socket_type="udp")
        if not response_result:
            if except_relay_none:
                return
            raise AssertionError(f"发送车辆请求后，未收到回复")
        if response_result.DataType == 0:
            logger.warning(f"发送车辆请求后，收到报文头否定响应，code:{response_result.DataInfo}")
            return
        # logger.info(f"请求0x0003,返回的响应是：\n{response_result}")
        if check_vin:
            assert check_vin == response_result.DataInfo.Vin
        if check_logical_address:
            assert check_logical_address == response_result.DataInfo.LogicalAddress
        if check_eid:
            assert check_eid == response_result.DataInfo.EID.hex()
        if check_gid:
            assert check_gid == response_result.DataInfo.GID.hex()
        if check_further_action_required:
            assert check_further_action_required == response_result.DataInfo.FurtherActionRequired

    def doip_generate_service_0x0004(self,
                                     vin=None,
                                     logical_address=None,
                                     eid=None,
                                     gid=None,
                                     further_action_required=None):
        data = deepcopy(doip_frame_raw_data_0x0004)
        if vin:
            data["DataInfo"]["Vin"] = vin
        if logical_address:
            data["DataInfo"]["LogicalAddress"] = logical_address
        if eid:
            data["DataInfo"]["EID"] = bytes.fromhex(eid)
        if gid:
            data["DataInfo"]["GID"] = bytes.fromhex(gid)
        if further_action_required:
            data["DataInfo"]["FurtherActionRequired"] = further_action_required
        return doip_build(data)

    def doip_generate_service_0x0005(self,
                                     source_address=None,
                                     check_targe_address=None,
                                     check_source_address=None,
                                     except_relay_none=False,
                                     check_res_code=None
                                     ):
        """
        请求路由激活
        :param source_address: 那个源地址请求激活，eg: 0x0e80
        :param check_targe_address: 检查0x0006的target_address，eg: 0x0e80
        :param check_source_address: 检查0x0006的source_address，eg: 0x1001
        :param check_res_code: 检查0x0006的返回码
        :param except_relay_none: 期待返回为none
        :return:
        """
        data = deepcopy(doip_frame_raw_data_0x0005)
        if source_address:
            data["DataInfo"]["SourceAddress"] = source_address
        doip_data_0x0005 = doip_build(data)
        doip_type = doip_req_to_res_map.get(data.get("DataType"))
        response_result = self.doip_sock_obj.send_and_get_callback_data(doip_data_0x0005, doip_type)
        if not response_result:
            if except_relay_none:
                return
            logger.warning(f"发送车辆请求后，未收到回复")
            raise
        if response_result.DataType == 0:
            logger.warning(f"发送车辆请求后，收到报文头否定响应，code:{response_result.DataInfo}")
            return

        # logger.info(f"请求0x0005,返回的响应是：\n{response_result}")
        if check_targe_address:
            assert check_targe_address == response_result.DataInfo.TargetAddress
        if check_source_address:
            assert check_source_address == response_result.DataInfo.SourceAddress
        if check_res_code:
            assert check_res_code == response_result.DataInfo.ResCode

    def doip_generate_service_0x0006(self,
                                     target_address=None,
                                     source_address=None,
                                     res_code=None,
                                     ):
        """
        构造0006的响应数据
        """
        data = deepcopy(doip_frame_raw_data_0x0006)
        if target_address:
            data["DataInfo"]["TargetAddress"] = target_address
        if source_address:
            data["DataInfo"]["SourceAddress"] = source_address
        if res_code:
            data["DataInfo"]["ResCode"] = res_code
        return doip_build(data)

    def doip_generate_service_0x0007(self, check_source_address=None, except_relay_none=False):
        """
        检测是否在线，通常是服务端发个客户端，客户端响应是否在线
        """
        data = deepcopy(doip_frame_raw_data_0x0007)
        doip_data_0x0007 = doip_build(data)
        doip_type = doip_req_to_res_map.get(data.get("DataType"))
        response_result = self.doip_sock_obj.send_and_get_callback_data(doip_data_0x0007, doip_type)
        if not response_result:
            if except_relay_none:
                return
            logger.warning(f"发送车辆请求后，未收到回复")
            raise
        if response_result.DataType == 0:
            logger.warning(f"发送车辆请求后，收到报文头否定响应，code:{response_result.DataInfo}")
            return
        # logger.info(f"请求0x0007,返回的响应是：\n{response_result}")
        if check_source_address:
            assert check_source_address == response_result.DataInfo

    def doip_generate_service_0x0008(self, source_address=None):
        """
        响应那个逻辑地址是否在线
        :param source_address: 如0e80逻辑地址在线：0x0e80
        """
        data = deepcopy(doip_frame_raw_data_0x0008)
        if source_address:
            data["DataInfo"] = source_address
        return doip_build(data)

    def doip_generate_service_0x4001(self, check_node_type=None,
                                     check_tcp_data_max_numer=None,
                                     except_relay_none=False,
                                     check_now_tcp_data_open_number=None):
        """
        :param check_node_type: 检查节点类型，0: doip网关；1: doip节点
        :param check_tcp_data_max_numer: 检查tcp连接最大数
        :param check_now_tcp_data_open_number: 检查当前打开的数
        :param except_relay_none: 期待为空
        """
        data = deepcopy(doip_frame_raw_data_0x4001)
        doip_data_0x4001 = doip_build(data)
        doip_type = doip_req_to_res_map.get(data.get("DataType"))
        response_result = self.doip_sock_obj.send_and_get_callback_data(doip_data_0x4001, doip_type, socket_type="udp")
        if not response_result:
            if except_relay_none:
                return
            logger.warning(f"发送车辆请求后，未收到回复")
            raise
        if response_result.DataType == 0:
            logger.warning(f"发送车辆请求后，收到报文头否定响应，code:{response_result.DataInfo}")
            return

        # logger.info(f"请求0x4001,返回的响应是：\n{response_result}")
        if check_node_type:
            assert check_node_type == response_result.DataInfo.NodeType
        if check_tcp_data_max_numer:
            assert check_tcp_data_max_numer == response_result.DataInfo.TCP_DATA_MAX_NUMBER
        if check_now_tcp_data_open_number:
            assert check_now_tcp_data_open_number == response_result.DataInfo.NOW_TCP_DATA_OPEN_NUMBER

    def doip_generate_service_0x4002(self, node_type=None,
                                     tcp_data_max_numer=None,
                                     now_tcp_data_open_number=None):
        """
        :param node_type: 节点类型，0: doip网关；1: doip节点
        :param tcp_data_max_numer: tcp连接最大数
        :param now_tcp_data_open_number: 当前打开的数
        """
        data = deepcopy(doip_frame_raw_data_0x4002)
        if node_type:
            data["DataInfo"]["NodeType"] = node_type
        if tcp_data_max_numer:
            data["DataInfo"]["TCP_DATA_MAX_NUMBER"] = tcp_data_max_numer
        if now_tcp_data_open_number:
            data["DataInfo"]["NOW_TCP_DATA_OPEN_NUMBER"] = now_tcp_data_open_number
        return doip_build(data)

    def doip_generate_service_0x4003(self, check_mode=None, except_relay_none=False):
        """
        :param check_mode: 检查4004返回的mode (0：not ready 1:ready 2:not supported)
        :param except_relay_none: 期待为空
        """
        data = deepcopy(doip_frame_raw_data_0x4003)
        doip_data_0x4003 = doip_build(data)
        doip_type = doip_req_to_res_map.get(data.get("DataType"))
        response_result = self.doip_sock_obj.send_and_get_callback_data(doip_data_0x4003, doip_type, socket_type="udp")
        if not response_result:
            if except_relay_none:
                return
            logger.warning(f"发送车辆请求后，未收到回复")
            raise
        if response_result.DataType == 0:
            logger.warning(f"发送车辆请求后，收到报文头否定响应，code:{response_result.DataInfo}")
            return

        # logger.info(f"请求0x4003,返回的响应是：\n{response_result}")
        if check_mode:
            assert check_mode == response_result.DataInfo

    def doip_generate_service_0x4004(self, mode):
        """
        :param mode: 诊断电源模式请求: 0：not ready 1:ready 2:not supported
        """
        data = deepcopy(doip_frame_raw_data_0x4004)
        data["DataInfo"] = mode
        return doip_build(data)

    def doip_generate_service_0x8001(self,
                                     source_address=None,
                                     target_address=None,
                                     diag_data=None,
                                     need_wait_for_result=True,
                                     check_return_data=None,
                                     check_ack_code=None,
                                     check_nrc_code=None,
                                     except_relay_none=False
                                     ):
        """
        :param source_address: 发送诊断的源地址，如：0x0e80
        :param target_address: 发送诊断的目的地址，如：0x1002
        :param diag_data:  诊断数据，如: [0x10, 0x01]
        :param need_wait_for_result:  需要等到0x8001的诊断回复
        :param except_relay_none:  期望不回复
        :param check_return_data: 需要检查诊断返回8001的数据，如：check_return_data=['5003']
                                                            check_return_data=['7f78', '5003']
                                                            check_return_data=['7f78', '7f31']
        :param check_ack_code: 需要检查积极响应8002的响应码，如：check_ack_code=0
        :param check_nrc_code: 如果期望返回8003否定响应，填期望的否定响应码：
                           #     0x2: "invalid source address",
                           #     0x3: "unknown target address",
                           #     0x4: "diagnostic message too large",
                           #     0x5: "out of memory",
                           #     0x6: "target unreachable",
                           #     0x7: "unknown network",
                           #     0x8: "transport protocl error",
        """
        data = deepcopy(doip_frame_raw_data_0x8001)
        if source_address:
            data["DataInfo"]["SourceAddress"] = source_address
        if target_address:
            data["DataInfo"]["TargetAddress"] = target_address
        if diag_data:
            data["DataInfo"]["DiagData"] = bytes(diag_data)
        data["DataLen"] = 4 + len(diag_data)
        doip_data_0x8001 = doip_build(data)
        doip_type = doip_req_to_res_map.get(data.get("DataType"))
        if check_return_data and check_ack_code:
            response_result = self.doip_sock_obj.send_and_get_callback_data(doip_data_0x8001, doip_type,
                                                                            need_expect_type=[0x8001, 0x8002])
        elif check_nrc_code:
            response_result = self.doip_sock_obj.send_and_get_callback_data(doip_data_0x8001, doip_type,
                                                                            need_expect_type=[0x8003])
        elif need_wait_for_result:
            response_result = self.doip_sock_obj.send_and_get_callback_data(doip_data_0x8001, doip_type,
                                                                            need_expect_type=[0x8001])
        else:
            response_result = self.doip_sock_obj.send_and_get_callback_data(doip_data_0x8001, doip_type)

        if not response_result:
            if except_relay_none:
                return
            raise AssertionError(f"发送8001请求后，没有收到期望的值。")
        if not isinstance(response_result, list):
            response_result_list = [response_result]
        else:
            response_result_list = response_result

        if check_return_data:
            check_return_data = [bytes.fromhex(i) for i in check_return_data]

        return_data = None
        for single_result in response_result_list:
            if single_result.DataType == 0:
                logger.warning(f"发送车辆请求后，收到报文头否定响应，code:{single_result.DataInfo}")
                return
            if hasattr(single_result.DataInfo, 'DiagData'):
                logger.info(
                    f'{hex(data["DataInfo"]["SourceAddress"])}->{hex(data["DataInfo"]["TargetAddress"])}:{bytes(diag_data).hex()}')
                logger.info(
                    f'{hex(single_result.DataInfo.SourceAddress)}->{hex(single_result.DataInfo.TargetAddress)}:{single_result.DataInfo.DiagData.hex()}')
            elif hasattr(single_result.DataInfo, 'ReturnCode'):
                logger.info(
                    f'{hex(data["DataInfo"]["SourceAddress"])}->{hex(data["DataInfo"]["TargetAddress"])}:{bytes(diag_data).hex()}')
                logger.info(
                    f'{hex(single_result.DataInfo.SourceAddress)}->{hex(single_result.DataInfo.TargetAddress)}:{single_result.DataInfo.ReturnCode}')
            elif hasattr(single_result.DataInfo, 'NRCCode'):
                logger.info(
                    f'{hex(data["DataInfo"]["SourceAddress"])}->{hex(data["DataInfo"]["TargetAddress"])}:{bytes(diag_data).hex()}')
                logger.info(
                    f'{hex(single_result.DataInfo.SourceAddress)}->{hex(single_result.DataInfo.TargetAddress)}:{single_result.DataInfo.NRCCode}')
            logger.info(f"====================\n")

            if single_result.DataType == 0x8001:
                if check_return_data:
                    if single_result.DataInfo.DiagData in check_return_data:
                        logger.info(f"found return data:{single_result.DataInfo.DiagData.hex()}")
                        check_return_data.remove(single_result.DataInfo.DiagData)

                if single_result.DataInfo.DiagData[0] == diag_data[0] + 0x40:
                    return_data = single_result.DataInfo.DiagData

            if check_ack_code:
                if single_result.DataType == 0x8002:
                    assert check_ack_code == single_result.DataInfo.ReturnCode
            if check_nrc_code:
                if single_result.DataType == 0x8003:
                    assert check_nrc_code == single_result.DataInfo.NRCCode
        if check_return_data:
            logger.warning(f"No findings were found {[i.hex() for i in check_return_data]} from the returned data")
            raise

        return return_data

    def doip_generate_service_0x8002(self,
                                     source_address=None,
                                     target_address=None,
                                     return_code=None):
        data = deepcopy(doip_frame_raw_data_0x8002)
        if source_address:
            data["DataInfo"]["SourceAddress"] = source_address
        if target_address:
            data["DataInfo"]["TargetAddress"] = target_address
        if return_code:
            data["DataInfo"]["ReturnCode"] = bytes(return_code)
        return doip_build(data)

    def doip_generate_service_0x8003(self,
                                     source_address=None,
                                     target_address=None,
                                     nrc_code=None):
        data = deepcopy(doip_frame_raw_data_0x8003)
        if source_address:
            data["DataInfo"]["SourceAddress"] = source_address
        if target_address:
            data["DataInfo"]["TargetAddress"] = target_address
        if nrc_code:
            data["DataInfo"]["NRCCode"] = bytes(nrc_code)
        return doip_build(data)

    def get_seed_with_27(self, data):
        sub_id = data[0]
        if sub_id in [0x01, 0x03, 0x05, 0x07, 0x09, 0x11, 0x19, 0x5F]:
            if sub_id in [0x07, 0x09]:
                seed = data[1:17]
            else:
                seed = data[1:4]
        else:
            raise AssertionError(f"sub id not match。got:{sub_id}")
        return seed

    @staticmethod
    def get_security_access_level(sub_id):
        if sub_id in [0x01, 0x02]:
            return 0x01
        elif sub_id in [0x03, 0x04]:
            return 0x02
        elif sub_id in [0x05, 0x06]:
            return 0x03
        elif sub_id in [0x07, 0x08]:
            return 0x04
        elif sub_id in [0x09, 0x0A]:
            return 0x05
        elif sub_id in [0x11, 0x12]:
            return 0x06
        elif sub_id in [0x19, 0x1A]:
            return 0x07
        elif sub_id in [0x5F, 0x60]:
            return 0x08

    def generate_27_service_handler(self, session_level=0x03,
                                    source_address=0x0e80,
                                    target_address=0x1002):
        result = self.doip_generate_service_0x8001(diag_data=[0x27, session_level],
                                                   source_address=source_address,
                                                   target_address=target_address,
                                                   check_ack_code=0x0)
        if list(result)[2:] != [0x00, 0x00, 0x00]:
            seed = self.get_seed_with_27(result[1:])
            level = self.get_security_access_level(result[1])
            key = self.sec.get_calculated_key(level, seed)

            self.doip_generate_service_0x8001(diag_data=[0x27, session_level + 1] + list(key),
                                              source_address=source_address,
                                              target_address=target_address,
                                              check_ack_code=0x0)

    def switch_usg_mode(self, mode_type):
        """
        控制 使用模式  mode_type 取值如下：
            0x00=Abandoned
            0x01=Inactive
            0x02=Convenience
            0x0B=Active
            0x0D=Driving
        @param mode_type: 切换类型
        @return:
        """
        result = self.doip_generate_service_0x8001(diag_data=[0x22, 0xDD, 0x0A],
                                                   check_ack_code=0x0)
        if result[-1] == mode_type:
            logger.info(f"current mode ready {mode_type}")
            return

        result = self.doip_generate_service_0x8001(diag_data=[0x22, 0xF1, 0x86], check_ack_code=0x0)
        logger.info(f"current session mode is:{result[-1]}")
        if result[-1] != 0x3:
            self.doip_generate_service_0x8001(diag_data=[0x10, 0x03],
                                              source_address=0x0e80,
                                              target_address=0x1002,
                                              check_ack_code=0x0)

        self.generate_27_service_handler(0x3)

        self.doip_generate_service_0x8001(diag_data=[0x2F, 0xDD, 0x0A, 0x03, mode_type],
                                          check_ack_code=0x0)

    def change_car_mode(self, mode_type):
        """
        切换 car mode
        @param mode_type: 切换的 模式
                    0 : NORMAL
                    1 : TRANSPORT
                    2 : FACTORY
                    3 : CRASH
                    5 : DYNO
        @return:
        """
        result = self.doip_generate_service_0x8001(diag_data=[0x22, 0xD1, 0x34],
                                                   check_ack_code=0x0)
        if result[-1] == mode_type:
            logger.info(f"current car mode ready {mode_type}")
            return

        result = self.doip_generate_service_0x8001(diag_data=[0x22, 0xF1, 0x86], check_ack_code=0x0)
        logger.info(f"current session mode is:{result[-1]}")
        if result[-1] != 0x3:
            self.doip_generate_service_0x8001(diag_data=[0x10, 0x03],
                                              source_address=0x0e80,
                                              target_address=0x1002,
                                              check_ack_code=0x0)

        self.generate_27_service_handler(0x3)

        self.doip_generate_service_0x8001(diag_data=[0x2F, 0xD1, 0x34, 0x03, mode_type],
                                          check_ack_code=0x0)

    def check_sp_0x78_times_by_service_id(self, service_id,
                                          check_times=None,
                                          check_time_interval=None,
                                          offset=0.5):
        """
        检查0x78出现的次数或者0x78出现的间隔时间
        @param service_id: 回0x78的服务，如检查0x22回复的0x78，则：service_id=0x22
        @param check_times: 回0x78的服务的次数检查，如：check_times=5
        @param check_time_interval: 回0x78的服务的时间间隔检查，单位是秒，如：check_time_interval=5
        @param offset: 检查时间间隔允许的误差，单位秒，如：offset=0.5
        """
        for k, v in self.doip_sock_obj.sp_0x78_time_dict.items():
            logger.info(f"{hex(k)}")
            for z, x in v.items():
                logger.info(f"{z}: {x}")
                logger.info(f"=================")
        if check_times:
            if not self.doip_sock_obj.sp_0x78_time_dict.get(service_id):
                raise AssertionError(f"not accept {hex(service_id)} 0x78 replay")
            if not len(self.doip_sock_obj.sp_0x78_time_dict.get(service_id)) == check_times:
                logger.warning(f"{hex(service_id)} accept times "
                               f"is:{len(self.doip_sock_obj.sp_0x78_time_dict.get(service_id))},"
                               f"but expect times is:{check_times}")
                raise AssertionError(f"{hex(service_id)} accept times "
                                     f"is:{len(self.doip_sock_obj.sp_0x78_time_dict.get(service_id))},"
                                     f"but expect times is:{check_times}")
        if check_time_interval:
            if not self.doip_sock_obj.sp_0x78_time_dict.get(service_id):
                raise AssertionError(f"not found {hex(service_id)} replay 0x78 response.")
            if len(self.doip_sock_obj.sp_0x78_time_dict.get(service_id)) == 1:
                raise AssertionError(f"only accept {hex(service_id)} replay 0x78 one times")

            cuc_time_list = [i for i in self.doip_sock_obj.sp_0x78_time_dict[service_id].values()]

            first_time = cuc_time_list.pop(0)
            for ac_time in cuc_time_list:
                if abs(round(ac_time - first_time, 1) - check_time_interval) > offset:
                    logger.warning(f"Real time interval is:{round(ac_time - first_time, 1)}, "
                                   f"expect times is:{check_time_interval}")
                    raise AssertionError(f"Real time interval is:{round(ac_time - first_time, 1)}, "
                                         f"expect times is:{check_time_interval}")
                first_time = ac_time

    def close_fire_real_vehicle(self, close_domain_list=None):
        """
        close_domain_list
        @param close_domain_list: 需要关闭的domain， 如：0x1001
        """
        if not isinstance(close_domain_list, list):
            close_domain_list = [close_domain_list]
        data = self.doip_generate_service_0x8001(target_address=0x1001,
                                                 diag_data=[0x22, 0xb1, 0x65],
                                                 check_ack_code=0x0
                                                 )
        if data[-1] == 0x2:
            logger.info("防火墙已关闭")
            return
        logger.info("防火墙打开状态，关闭防火墙")

        self.doip_generate_service_0x8001(source_address=0x0e80,
                                          target_address=0x1001,
                                          diag_data=[0x10, 0x03])

        l7_key = self.get_l7_key()
        self.sec.constant_lev4 = l7_key
        self.sec.cryptor_aes128.key = bytes.fromhex(l7_key)
        self.generate_27_service_handler(0x7)

        if close_domain_list:
            for close_domain in close_domain_list:
                self.doip_generate_service_0x8001(source_address=0x0e80,
                                                  target_address=close_domain,
                                                  diag_data=[0x31, 0x01, 0xa0, 0x40, 0x02, 0xff])
        else:
            self.doip_generate_service_0x8001(source_address=0x0e80,
                                              target_address=0x1fff,
                                              diag_data=[0x31, 0x01, 0xa0, 0x40, 0x02, 0xff])

    def get_l7_key(self):
        soa_api_test_path = os.path.join(os.path.dirname(__file__), '../interface/bgm/soa_api_test')
        file_upload(device_name="BGM",
                    local_path=soa_api_test_path,
                    remote_path='/tmp/')
        status, ret_str = command_send(device_name="BGM",
                                       cmd="cd /tmp/;chmod +x soa_api_test;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib;./soa_api_test",
                                       connect_type='obd')
        l7_index = ret_str.split('\n').index('L7 key: ')
        l7_key = ret_str.split('\n')[l7_index + 1].replace(" ", "")
        logger.info(f"获取到L7的key是：{l7_key}")
        return l7_key

    def get_l7_key_tcam(self):
        soa_api_test_path = os.path.join(os.path.dirname(__file__), '../interface/tcam/tcam_seco_api_test')
        file_upload(device_name="TCAM",
                    local_path=soa_api_test_path,
                    remote_path='/tmp/')
        status, ret_str = command_send(device_name="TCAM",
                                       cmd="cd /tmp/;chmod +x tcam_seco_api_test;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/oemapp/lib;export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/umdp/lib/;./tcam_seco_api_test",
                                       connect_type='obd')
        l7_index = ret_str.split('\n').index('L7 key: ')
        l7_key = ret_str.split('\n')[l7_index + 1].replace(" ", "")
        logger.info(f"获取到L7的key是：{l7_key}")
        return l7_key
