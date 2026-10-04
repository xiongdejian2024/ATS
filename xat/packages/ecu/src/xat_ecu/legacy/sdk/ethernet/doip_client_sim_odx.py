#!/usr/bin/python3
"""
@File        : doip_client_sim_odx.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-11-30 11:28
@Description : simulate diagnostic client behavior using doip
"""


import os

# from ..driver.ethernet_lib.logger import main
import sys, getopt

from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.error_code import StatusCode
from xat_ecu.legacy.common.exception_error import error_check
from xat_ecu.legacy.utils.utils import struct_pretty

current_path = os.path.dirname(os.path.realpath(__file__))
import time
import threading
from threading import Thread
from copy import deepcopy
from xat_ecu.legacy.common.logger import logger
from time import sleep
from enum import IntEnum
from xat_ecu.legacy.sdk.diagnosis.uds_client_odx import Uds_Client_Odx
from xat_ecu.legacy.sdk.tp.doiptp import DoipTp
from xat_ecu.legacy.sdk.ethernet.doip_payload import doip_payload
from xat_ecu.legacy.sdk.driver.ethernet_lib.tcp_socket import tcp_socket_client
from xat_ecu.legacy.sdk.driver.ethernet_lib.udp_brocaster_socket import UdpBroadcast
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.sdk import get_obd_ip

response_received = False  # Used to perform unit test for DoIP


GENERIC_TYPE = 0x0000
VEHICLE_ID_REQ_TYPE = 0x0001
VEHICLE_ID_REQ_EID_TYPE = 0x0002
VEHICLE_ID_REQ_VIN_TYPE = 0x0003
VEHICLE_ANN_TYPE = 0x0004
VEHICLE_ID_RESP_TYPE = 0x0004
ROUTING_ACT_REQ_TYPE = 0x0005
ROUTING_ACT_RESP_TYPE = 0x0006
ALIVE_CHK_REQ_TYPE = 0x0007
ALIVE_CHK_RESP_TYPE = 0x0008
DOIP_ENTITY_STATE_REQ_TYPE = 0x4001
DOIP_ENTITY_STATE_RESP_TYPE = 0x4002
DIAG_POWER_MODE_INFO_REQ_TYPE = 0x4003
DIAG_POWER_MODE_INFO_RESP_TYPE = 0x4004
DIAG_MSG_TYPE = 0x8001
DIAG_MSG_POS_ACK_TYPE = 0x8002
DIAG_MSG_NEG_ACK_TYPE = 0x8003

P6_CLIENT_ENHANCED_TIMEOUT = 10
P6_CLIENT_TIMEOUT = 2
P3_CLIENT_MIN = 0.15
A_DoIP_Diagnostic_Message = (
    2  #  client timeout           Performance(server) time: <50ms
)
S3_CLIENT = 2

# Self definition
TESTER_CLIENT_TIMEOUT = 6000  # Maximum waiting time(pending)


global obd_doip_tcp_client
obd_doip_tcp_client = {}
global rx_diags_msgs_dict
rx_diags_msgs_dict = {}


def get_obdip(retries=20):
    retries = retries
    while retries > 0:
        try:
            obd_ip = get_obd_ip.get_announcement_ip()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/ethernet/doip_client_sim_odx.py")
            logger.warning(f"get obd ip error: {e}")
            sleep(1)
            retries -= 1
            continue
        if obd_ip:
            return obd_ip
        else:
            sleep(1)
            retries -= 1
            logger.info(f"获取obdip失败，剩余重试次数 {retries}")


# ****************************************************************************************
class Doip_Client_Sim_Odx(object):
    # ****************************************
    # def __init__(self, server_doip_id=0x05, server_ip="172.20.1.1", server_port=13400, my_ip=None, my_port=None)
    def __init__(
        self,
        ecu="BGM",
        server_doip_id=0x1001,
        server_ip="172.16.5.1",
        server_port=13400,
        my_ip=None,
        my_port=None,
        sec_con={},
        obd_nuc_ip="169.254.1.200",
        auto_flag=True,
    ):
        # self.log = setup_logger(level="warning", name="(DOIP)")
        self.server_doip_id = server_doip_id
        self.get_sa_list()
        self.server_ip = server_ip
        self.server_port = server_port
        self.my_ip = my_ip
        self.my_port = my_port
        self.payload = None
        self.current_payload_data = []
        self._exitFlag = False
        self.client_doip_id = [0x0E, 0x80]
        self.func_doip_id = [0x1F, 0xFF]
        self.cb = None
        self.sid = None
        self.get_sub_data = None
        self.msg_ack_received = True
        self.msg_ack_type = None
        self.func_cycle = False
        self.uds_client = Uds_Client_Odx(ecu, sec_con=sec_con)
        self.positive_ack = None
        self.timeout = None
        self.i_ct = 0
        self.message_automatic_sent = None
        self.userdata = []
        self.userdata_print = None
        self.lock = threading.Lock()
        self.automatic_send_data = []
        self.slice_data = []
        self.response_dict = {}
        self.obd_nuc_ip = obd_nuc_ip
        self.recv_sa_id_list = None
        self.auto_flag = auto_flag

    def msg_ack_received_cycle_assert(self):
        i = 0
        while i < A_DoIP_Diagnostic_Message:
            if self.msg_ack_received:
                return True
            i += 0.001
            sleep(0.001)
            self.msg_ack_received = True  #  临时

        logger.warning(f"2秒内没有接收到doip的ack回复。")
        # logger.warning(
        #     "--------------  DOIP msg_ack_received  Timeoout 2s    -------------- "
        # )
        return False

    def is_retransmission_and_retransmission(self, diag_msg_data):
        # only doip ack/nack check
        if not self.msg_ack_received_cycle_assert():
            self.msg_ack_received = None
            self.doip_tcp_client_send(diag_msg_data)
            # logger.warning(
            #     "Retransmission Doip Message Up to 50 : {}".format(diag_msg_data[:50])
            # )
            if len(diag_msg_data) > 50:
                diag_msg_data_part = diag_msg_data[:50]
                logger.warning(f"重传doip消息：{bytes(diag_msg_data_part).hex()}")
            else:
                diag_msg_data_part = diag_msg_data
                logger.warning(f"重传doip消息：{bytes(diag_msg_data_part).hex()}")
            if not self.msg_ack_received_cycle_assert():
                # self.lock.release()
                with error_check(StatusCode.DOIP_RETRANSMISSION_ERR, exception_error.DOIPError):
                    raise AssertionError(f"重传消息：{bytes(diag_msg_data_part).hex()} 后，任然没有获取到回复。")
                # raise RuntimeError("send_data  msg_ack_received retry  ------  Timeout")

    def print_message(self, data):
        if data[0] not in [0x36]:
            userdata_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(
                data
            )
            # self.response_dict[self.server_doip_id]=self.response_print
            # logger.info("UDS Data (Doip) : [Tx] {}".format(userdata_print))
            logger.info("诊断(Doip) : [Tx] {}".format(userdata_print))
        elif data[0] in [0x36]:
            userdata_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(
                data[:2]
            )
            logger.info(f"诊断0x36服务：[Tx] {userdata_print}，仅显示前两个字节。")
            # logger.info(
            #     "UDS Data (Doip) : [Tx] {} ==== Considering the performance, "
            #     "0x36 service only displays the first two bytes".format(userdata_print)
            # )

    def is_complete(self, data):
        # Further improvement is needed to judge the doip data
        if len(data) >= 8:
            if data[0] == 0x02 and data[1] == 0xFD:
                self.slice_data = []
                length = (data[4] << 24) + (data[5] << 16) + (data[6] << 8) + data[7]
                if (len(data) - 8) >= length:
                    return True
                logger.warning(f"接收的数据不完整，期望得到字节数：{length}，实际得到字节数：{len(data)}")
                # logger.info(
                #     "incomplete payload, expected: %d, received: %d"
                #     % (length, len(data))
                # )
        logger.debug(f"实际得到字节数：{len(data)}。")
        # logger.info("====== Actually Received: %d  =====" % (len(data)))
        return False

    def get_payload_from_data(self, data):
        if self.is_complete(data) == False:
            return ([], [])
        length = (data[4] << 24) + (data[5] << 16) + (data[6] << 8) + data[7]
        if len(data) == (8 + length):
            return (data[0:8], data[8 : (8 + length)])
        elif len(data) > (8 + length):
            message = []
            while len(data) >= 8:  # 第二个 doip 报文若是不完整的情况暂未考虑，出现会报错
                if self.is_complete(data) == False:
                    return ([], [])
                length = (data[4] << 24) + (data[5] << 16) + (data[6] << 8) + data[7]
                message.append((data[0:8], data[8 : (8 + length)]))
                data = data[(8 + length) :]
            return message
        # return(data[0:8],data[8:])

    def diagnostic_parameter_reset(self):
        self.positive_ack = None
        self.timeout = P6_CLIENT_TIMEOUT

    def close(self):
        # logger.info("DoIP: Closing connection")
        self.func_cycle = False
        sleep(2)
        self.doip_tcp_client.close()
        global rx_diags_msgs_dict
        rx_diags_msgs_dict.clear()

        sleep(2)
        # logger.info("DoIP: Connection closed")
        # ****************************************

    def run(self):
        """
        @function new_connection(self)
        @brief This function is used to create a new connection to send data
        @return tcp_socket_client reference to a TCP socket
        """
        # 并行诊断暂不考虑IP变掉的情况
        if "169.254." in self.server_ip:
            if "169.254.1.200" == self.server_ip:
                obdip = self.server_ip   # 适配2.0 项目 jetsoa 中间测试
            else:
                obdip = get_obdip()
            if obdip:
                self.server_ip = obdip
            else:
                raise RuntimeError("获取obdip失败，请检查台架环境")
            
        global obd_doip_tcp_client
        logger.debug(f"当前doip tcp连接信息是：\n{obd_doip_tcp_client}")
        if self.server_ip in obd_doip_tcp_client.keys():  # 是否创建socket
            if (obd_doip_tcp_client[self.server_ip].exitFlag != True) and (
                obd_doip_tcp_client[self.server_ip].tcp_connection_error is not True
            ):
                # 正常并行诊断
                self.doip_tcp_client = obd_doip_tcp_client[self.server_ip]
                global rx_diags_msgs_dict
                rx_diags_msgs_dict[self.server_ip].append(self.rx_diags_msgs)
                logger.info(f"{self.server_ip} Doip Socket 已经启动，无需再次启动。")
            elif obd_doip_tcp_client[self.server_ip].exitFlag == True:
                # 关闭后重新启动
                self.to_start(is_save_rxlist=False)
            elif obd_doip_tcp_client[self.server_ip].tcp_connection_error is True:
                # 错误后重连 / 异常时并行诊断
                with error_check(StatusCode.DOIP_CONNECT_ERR, exception_error.DOIPError):
                    self.to_start(is_save_rxlist=True)
                    # logger.exception(StatusCode.DOIP_CONNECT_ERR.format_err_msg)
        else:
            # 第一次启动
            # with error_check(StatusCode.DOIP_CONNECT_ERR, exception_error.DOIPError):
            self.to_start(is_save_rxlist=False)
                # logger.exception(StatusCode.DOIP_CONNECT_ERR.format_err_msg)

    def to_start(self, is_save_rxlist=False):
        # :param is_save_rxlist: bool  是否保留 rx_diags_msgs_dict[self.server_ip] 列表
        # 新建socket对象
        if "169.254." in self.server_ip:
            if "169.254.1.200" == self.server_ip:
                obdip = self.server_ip   # 适配2.0 项目 jetsoa 中间测试
            else:
                obdip = get_obdip()
            if obdip:
                self.server_ip = obdip
            else:
                with error_check(StatusCode.DOIP_OBD_ERR, exception_error.DOIPError):
                    raise RuntimeError("获取obdip失败，请检查台架环境")
    
        self.doip_tcp_client = tcp_socket_client(1, "DoIP TCP Socket")
        global obd_doip_tcp_client
        obd_doip_tcp_client[self.server_ip] = self.doip_tcp_client
        global rx_diags_msgs_dict
        if is_save_rxlist:   
            if self.server_ip in rx_diags_msgs_dict:
                if self.rx_diags_msgs not in rx_diags_msgs_dict[self.server_ip]:
                    rx_diags_msgs_dict[self.server_ip].append(self.rx_diags_msgs)
                    logger.warning(f"当前的诊断回调dict数据是：{rx_diags_msgs_dict}")
                    with error_check(StatusCode.DOIP_INSTANCE_ERR, exception_error.DOIPError):
                        raise
            else:
                rx_diags_msgs_dict[self.server_ip] = [self.rx_diags_msgs]
        else: # 并行诊断暂不考虑IP变掉的情况
            rx_diags_msgs_dict[self.server_ip] = [self.rx_diags_msgs]
        # if "169.254." in self.server_ip:
        #     obdip = get_obdip()
        #     if obdip:
        #         self.server_ip = obdip
        #     else:
        #         raise RuntimeError("获取obdip失败，请检查台架环境")
        with error_check(StatusCode.DOIP_CONNECT_ERR, exception_error.DOIPError):
            self.doip_tcp_client.connect(self.server_ip, self.server_port)
        # try:
        #     self.doip_tcp_client.connect(self.server_ip, self.server_port)
        # except OSError as e:
        #     logger.error(str(e) + " : %s:%d" % (self.server_ip, self.server_port))
        #     return False
        self.doip_tcp_client.setup_response_callback(rx_diags_msgs_dict[self.server_ip])
        logger.info(f"{self.server_ip}:{self.server_port},socket连接成功。")
        # logger.info("TCP client connected")
        self.doip_tcp_client.setDaemon(True)
        self.doip_tcp_client.start()
        if self.auto_flag:
            self.routing_act()

    def routing_act(self):
        sleep(0.5)
        routing_act_res_data = DoipTp.construct_tx_signal_frames(
            payload_type=[0x00, 0x05]
        )
        self.doip_tcp_client_send(routing_act_res_data)
        # logger.info("====== Send Alive check request  =====")
        logger.info(f"诊断路由已发送激活请求...")
        sleep(1)

    def doip_tcp_client_send(self, data):
        if self.doip_tcp_client.exitFlag != True:
            if self.doip_tcp_client.tcp_connection_error is True:  # 注意关闭 主动关闭socke时，不能引起tcp_connection_error，不能会有逻辑问题
                result = self.to_start(is_save_rxlist=True)
                if result is False:
                    # raise RuntimeError("Doip Socket 重连失败，请检查下台架环境")
                    with error_check(None, exception_error.DOIPError):
                        raise RuntimeError("Doip Socket 重连失败，请检查下台架环境")
            self.doip_tcp_client.send(data)
        else:
            logger.warning("已经调用了 close doip socket 关闭，请不要再发数据。。。")

    def vid_request(self):
        # transmit Vehicle ID request
        with error_check(StatusCode.DOIP_INIT_ERR, exception_error.ObdIpError):
            udp_s = UdpBroadcast(name="udp_vid_request", server_ip=self.obd_nuc_ip)
            # logger.exception(StatusCode.DOIP_INIT_ERR.format_err_msg)
        payload = [0x02, 0xFD, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00]
        udp_s.send(payload)
        # logger.info("Sending Vehicle ID Request")
        logger.info("已发送车辆VIN请求...")
        udp_s.close()

    def get_sa_list(self):
        self.sa_list = [self.server_doip_id >> 8, self.server_doip_id & 0xFF]
        return self.sa_list

    def update_server_doip_id(self, doip_id, ecu="BGM"):
        # doip_id     0x1001  or 0x1002
        self.server_doip_id = doip_id
        self.get_sa_list()
        self.uds_client.update_security_constant(ecu)

    def send_data(self, data):
        # DIAG_MSG_TYPE
        self.diagnostic_parameter_reset()
        server_doip_id = self.sa_list
        diag_msg_data = DoipTp.construct_tx_signal_frames(
            payload_type=[0x80, 0x01],
            userdata=data,
            sa=self.client_doip_id,
            ta=server_doip_id,
        )
        with self.lock:
            self.msg_ack_received = None

            # special 先保持以前逻辑
            self.positive_ack = None   # 把此位置提前，防止收到数据后又将此置为None

            self.doip_tcp_client_send(diag_msg_data)
            # self.positive_ack = None  #  Prevent positive response before sending
            self.print_message(data)
            self.is_retransmission_and_retransmission(diag_msg_data)
    
    def reset_positive_ack(self):
        self.positive_ack = None

    def send_data_functional_addressing(self, data, interval_time=P3_CLIENT_MIN):
        # functional addressing
        server_doip_id = self.func_doip_id
        diag_msg_data = DoipTp.construct_tx_signal_frames(
            payload_type=[0x80, 0x01],
            userdata=data,
            sa=self.client_doip_id,
            ta=server_doip_id,
        )
        with self.lock:
            self.msg_ack_received = None
            self.doip_tcp_client_send(diag_msg_data)
            userdata_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(
                data
            )
            # logger.info(
            #     "Functional Addressing UDS Data (Doip) : [Tx] {}".format(userdata_print)
            # )
            logger.info(
                "功能地址发送数据(Doip) : [Tx] {}".format(userdata_print)
            )
            self.is_retransmission_and_retransmission(diag_msg_data)
        if interval_time:
            sleep(interval_time)

    def send_data_func_cycle(self, data, cycle_time=S3_CLIENT):
        # DIAG_MSG_TYPE
        while self.func_cycle:
            diag_msg_data = DoipTp.construct_tx_signal_frames(
                payload_type=[0x80, 0x01],
                userdata=data,
                sa=self.client_doip_id,
                ta=self.func_doip_id,
            )
            with self.lock:
                self.msg_ack_received = None
                self.doip_tcp_client_send(diag_msg_data)
                userdata_print = (
                    DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(data)
                )
                # logger.info(
                #     "Functional Addressing UDS Data (Doip) : [Tx] {}".format(
                #         userdata_print
                #     )
                # )
                logger.debug(
                    "功能诊断数据发送(Doip) : [Tx] {}".format(
                        userdata_print
                    )
                )
                self.is_retransmission_and_retransmission(diag_msg_data)
            # logger.info("Wait {} seconds to func_cycle".format(cycle_time))
            logger.debug("等待 {} 秒 循环发送".format(cycle_time))
            sleep(cycle_time)

    def send_data_func_cycle_thread(self, data, cycle_time=S3_CLIENT):
        func_msg_cycle = Thread(
            target=self.send_data_func_cycle,
            name="Functional_Message_Cycle_Doip",
            args=(data, cycle_time),
            daemon=True,
        )
        func_msg_cycle.start()

    def check_response(self, timeout=P6_CLIENT_TIMEOUT):
        self.timeout = timeout
        self.i_ct = 0
        wait_pending = 0
        while (
            (self.positive_ack is None)
            and (self.i_ct < self.timeout)
            and (wait_pending < TESTER_CLIENT_TIMEOUT)
        ):
            sleep(0.001)
            if self.i_ct == 0:
                wait_pending += 2
            self.i_ct += 0.001
        return self.positive_ack

    def reset_function_userdata(self):
        self.response_dict.clear()

    def return_function_userdata_and_check_response(self, timeout=15):
        self.i_ct = 0
        wait_pending = 0
        while (
                (self.i_ct < timeout)
                and (wait_pending < TESTER_CLIENT_TIMEOUT)
        ):
            sleep(0.001)
            if self.i_ct == 0:
                wait_pending += 2
            self.i_ct += 0.001
        return self.response_dict

    def retrun_udsdata_and_check_response(self, timeout=P6_CLIENT_TIMEOUT):
        self.timeout = timeout
        self.i_ct = 0
        wait_pending = 0
        while (
            (self.positive_ack is None)
            and (self.i_ct < self.timeout)
            and (wait_pending < TESTER_CLIENT_TIMEOUT)
        ):
            sleep(0.001)
            if self.i_ct == 0:
                wait_pending += 2
            self.i_ct += 0.001
        return self.positive_ack, self.userdata

    def get_recv_sa_id_list(self, timeout=10):
        self.recv_sa_id_list = []
        sleep(timeout)
        recv_sa_id_list = self.recv_sa_id_list
        self.recv_sa_id_list = None
        return recv_sa_id_list

    # ****************************************
    def setup_data_callback(self, callBack, response_id):
        """
        @function setup_data_callback(self, callBack, response_id)
        @brief This function must be called before sending a diagnostics request to setup the
               callback for the diagnostics response
        @param callBack Function callback for the message received
        @param response_id Can id of the intended recepient
        """
        # logger.info("Setup DoIP data callback to ")
        # logger.info(callBack)
        self.cb = callBack
        self.response_can_id = response_id

    # ****************************************
    def rx_diags_msgs(self, data):
        """
        @function rx_diags_msgs(self, data)
        @brief This function used to receive doip payloads, it is called from the TCP SOCKET
               after new data arrives in the socket. It calls the callback provided
               after a new uds request is complete. After reading from the socket we need to
               loop in this function looking for doip payloads in the data read from the socket.
        """
        if isinstance(data, list):
            # logger.info("data is {}".format(data))
            if self.is_complete(data):
                if isinstance(self.get_payload_from_data(data), list):
                    messages = self.get_payload_from_data(data)
                    # logger.info("data is {}".format(messages))
                    for doip_header, payload in messages:
                        # logger.info("Rx doip_header is {}".format(doip_header))
                        # logger.info("Rx payload is {}".format(payload))
                        self.rx_data_handing(doip_header, payload)
                else:
                    doip_header, payload = self.get_payload_from_data(data)
                    # logger.debug("Rx doip_header is {}".format(doip_header))
                    # logger.debug("Rx payload is {}".format(payload))
                    self.rx_data_handing(doip_header, payload)
            else:
                # Temporary processing slice data UDS(TCP)
                if self.slice_data:
                    self.slice_data += data
                    slice_data = self.slice_data

                    self.rx_diags_msgs(slice_data)
                else:
                    self.slice_data = data

    def rx_data_handing(self, doip_header, payload):
        if self.sa_list == payload[0:2] or self.sa_list == [0x1f, 0xff]:  # 适配并行
            protocol_version = doip_header[0]
            inverse_protocol_version = doip_header[1]
            payload_type = (doip_header[2] << 8) + doip_header[3]  # such as 0x8001
            reserved = doip_header[4:]
            if payload_type == DIAG_MSG_TYPE:
                # self.message_automatic_sent = None
                # sa = (payload[0] << 8) + payload[1]
                # ta = (payload[2] << 8) + payload[3]
                sa = payload[0:2]
                ta = payload[2:4]
                sa_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(sa)
                ta_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(ta)
                # logger.info("RX sa is [ {}], ta is [ {}]".format(sa_print, ta_print))

                if self.recv_sa_id_list is not None:
                    sa_int = (sa[0] << 8) + sa[1]
                    self.recv_sa_id_list.append(sa_int)

                self.userdata = payload[4:]
                self.sid = self.userdata[0]
                # if self.sid not in [0x36]:
                #     self.userdata_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(self.userdata)
                #     logger.info("UDS Data (Doip) : [Rx] {}".format(self.userdata_print))
                # elif self.sid in [0x36]:
                #     logger.info("Considering the performance, the 0x36 service is not displayed")
                self.userdata_print = (
                    DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(
                        self.userdata
                    )
                )
                logger.info("[ {}]-->[ {}] | 数据：{}".format(sa_print, ta_print, self.userdata_print))
                # logger.info("UDS Data (Doip) : [Rx] {}".format(self.userdata_print))
                if self.response_dict.get(sa_print.strip()):
                    self.response_dict[sa_print.strip()].append(self.userdata_print.strip())
                else:
                    self.response_dict[sa_print.strip()] = [self.userdata_print.strip()]
                # print('self.response_dict[sa_print]=',self.response_dict[sa_print])
                if sa != self.sa_list and self.sa_list != [0x1f, 0xff]:
                    sa_list_print = (
                        DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(
                            self.sa_list
                        )
                    )
                    logger.warning(
                        "Expected address is  {}  ; Received address is  {}".format(
                            sa_list_print, sa_print
                        )
                    )
                    return
                if self.sid == 0x7F:
                    self.sid = self.userdata[1]
                    self.get_sub_data = self.userdata[2]
                    if self.get_sub_data == 0x78:
                        # eth_timeout is 10
                        sleep(
                            0.002
                        )  # The adaptation receives 0x78 after a positive response
                        self.positive_ack = None
                        self.i_ct = 0
                        self.timeout = P6_CLIENT_ENHANCED_TIMEOUT
                    else:
                        self.positive_ack = False
                        self.timeout = P6_CLIENT_TIMEOUT
                else:
                    self.positive_ack = True
                    self.timeout = P6_CLIENT_TIMEOUT
                    self.get_sub_data = self.userdata[1:]
                    # send_data = DoipTp.construct_tx_signal_frames(payload_type = [0x80,0x02],sa= ta, ta = sa)
                    # self.doip_tcp_client_send(send_data)
                    self.uds_client.diagnostic_services_return_p_data(
                        self.sid, self.get_sub_data
                    )
                    if self.uds_client.p_data:
                        self.automatic_send_data = self.uds_client.p_data
                        self.message_automatic_sent = True

            elif payload_type == DIAG_MSG_POS_ACK_TYPE:
                self.msg_ack_received = True
            elif payload_type == DIAG_MSG_NEG_ACK_TYPE:
                self.msg_ack_received = False
                logger.info("==========   Recived doip NACK   =========")
            elif payload_type == ROUTING_ACT_REQ_TYPE:
                pass
            elif payload_type == ROUTING_ACT_RESP_TYPE:
                logger.info("====== Receive ROUTING ACT RESP, Active ECU =======")
            elif payload_type == ALIVE_CHK_REQ_TYPE:
                alive_chk_resp_data = DoipTp.construct_tx_signal_frames(
                    payload_type=[0x00, 0x08], sa=self.client_doip_id
                )
                self.doip_tcp_client_send(alive_chk_resp_data)
                logger.info("====== send alive chk resp  =======")
            elif payload_type == ALIVE_CHK_RESP_TYPE:
                pass
            else:
                # logger.info(
                #     "Unexpected DoIP payload: [{}]".format(
                #         ", ".join(hex(x) for x in doip_header)
                #     )
                # )
                logger.warning(
                    "得到不期望的诊断数据: [{}]".format(
                        ", ".join(hex(x) for x in doip_header)
                    )
                )

    # ============================================ special ===================================================
    def send_data_special(self, data):
        # For the purpose of improving the success rate of Flash, discard some checks
        # DIAG_MSG_TYPE

        # self.diagnostic_parameter_reset()
        self.timeout = P6_CLIENT_ENHANCED_TIMEOUT

        server_doip_id = self.sa_list
        diag_msg_data = DoipTp.construct_tx_signal_frames(
            payload_type=[0x80, 0x01],
            userdata=data,
            sa=self.client_doip_id,
            ta=server_doip_id,
        )
        with self.lock:
            # self.msg_ack_received = None

            self.doip_tcp_client_send(diag_msg_data)
            self.positive_ack = None  #  Prevent positive response before sending
            self.print_message(data)

            # self.is_retransmission_and_retransmission(diag_msg_data)

    def send_data_func_cycle_special(self, data, cycle_time=S3_CLIENT):
        # DIAG_MSG_TYPE
        while self.func_cycle:
            diag_msg_data = DoipTp.construct_tx_signal_frames(
                payload_type=[0x80, 0x01],
                userdata=data,
                sa=self.client_doip_id,
                ta=self.func_doip_id,
            )

            # self.msg_ack_received = None
            with self.lock:
                self.doip_tcp_client_send(diag_msg_data)
                userdata_print = (
                    DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(data)
                )
                # logger.info(
                #     "Functional Addressing UDS Data (Doip) : [Tx] {}".format(
                #         userdata_print
                #     )
                # )
                logger.debug(
                    "功能诊断地址发送(Doip) : [Tx] {}".format(
                        userdata_print
                    )
                )

                # self.is_retransmission_and_retransmission(diag_msg_data)

                # logger.info("Wait {} seconds to func_cycle".format(cycle_time))
                logger.debug("等待 {} 秒 循环发送".format(cycle_time))
                sleep(cycle_time)

    def send_data_func_cycle_special_thread(self, data, cycle_time=S3_CLIENT):
        func_msg_cycle = Thread(
            target=self.send_data_func_cycle_special,
            name="Functional_Message_Cycle_Doip Special",
            args=(data, cycle_time),
            daemon=True,
        )
        func_msg_cycle.start()

    # =============================================================================================================