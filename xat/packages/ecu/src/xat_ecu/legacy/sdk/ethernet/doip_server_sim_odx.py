#!/usr/bin/python3
"""
@File        : doip_server_sim_odx.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022-04-27 11:28
@Description : simulate diagnostic client behavior using doip
"""


import os
import sys, getopt

import time
import threading
from xat_ecu.legacy.common.logger import logger
from time import sleep
from xat_ecu.legacy.sdk.tp.doiptp import DoipTp
from xat_ecu.legacy.sdk.ethernet.doip_payload import doip_payload
from xat_ecu.legacy.sdk.driver.ethernet_lib.tcp_server_socket import TcpSocketServer
from xat_ecu.legacy.sdk.driver.ethernet_lib.udp_brocaster_socket import UdpBroadcast
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.sdk.diagnosis.uds_server_odx import Uds_Server_Odx
from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.error_code import StatusCode
from xat_ecu.legacy.common.exception_error import error_check
response_received = False  # Used to perform unit test for DoIP


GENERIC_TYPE=0x0000
VEHICLE_ID_REQ_TYPE=0x0001
VEHICLE_ID_REQ_EID_TYPE=0x0002
VEHICLE_ID_REQ_VIN_TYPE=0x0003
VEHICLE_ANN_TYPE=0x0004
VEHICLE_ID_RESP_TYPE=0x0004
ROUTING_ACT_REQ_TYPE=0x0005
ROUTING_ACT_RESP_TYPE=0x0006
ALIVE_CHK_REQ_TYPE=0x0007
ALIVE_CHK_RESP_TYPE=0x0008
DOIP_ENTITY_STATE_REQ_TYPE=0x4001
DOIP_ENTITY_STATE_RESP_TYPE=0x4002
DIAG_POWER_MODE_INFO_REQ_TYPE=0x4003
DIAG_POWER_MODE_INFO_RESP_TYPE=0x4004
DIAG_MSG_TYPE=0x8001
DIAG_MSG_POS_ACK_TYPE=0x8002
DIAG_MSG_NEG_ACK_TYPE=0x8003

P6_CLIENT_ENHANCED_TIMEOUT = 10
P6_CLIENT_TIMEOUT = 2
P3_CLIENT_MIN = 0.15
A_DoIP_Diagnostic_Message = 2     #  client timeout           Performance(server) time: <50ms
S3_CLIENT = 2

# Self definition
TESTER_CLIENT_TIMEOUT = 1200     # Maximum waiting time(pending)


class Doip_Server_Sim_Odx(Uds_Server_Odx):
    def __init__(self, ecu="BGM", server_doip_id=0x1001, server_ip="169.254.1.200", server_port=13400,
                 p_n_res=True, data_info=[],
                 nrc_code=0x22, ecu_map_id={},
                 dtc_code=[], routine_control_p_data={},
                 sec_con={}, mock_uds_data=None):
        self.mock_uds_data = mock_uds_data
        self.original_ecu = ecu
        self.server_doip_id = server_doip_id
        self.sa_list = self.get_sa_list()
        self.server_ip = server_ip
        self.server_port = server_port
        self.payload = None
        self.current_payload_data=[]
        self._exitFlag = False
        self.client_doip_id = [0x0E, 0x80]
        self.func_doip_id = [0x1F, 0xFF]
        self.cb = None
        self.sid = None
        self.get_sub_data = None
        self.msg_ack_received = True
        self.msg_ack_type = None
        self.func_cycle = True
        self.positive_ack = None 
        self.timeout = None
        self.i_ct = 0
        self.message_automatic_sent = None
        self.userdata = []
        self.userdata_print = None
        self.lock = threading.Lock()
        self.automatic_send_data = []
        self.slice_data = []
        self.routine_control_p_datas = routine_control_p_data
        self.mock_uds_data = mock_uds_data
        self.data_infos = data_info
        self.p_n_res = p_n_res
        self.nrc_code = nrc_code
        self.dtc_codes = dtc_code
        self.ecu_map_id = ecu_map_id
        self.set_config_data(ecu)
        super().__init__(ecu, sec_con=sec_con, mock_uds_data=self.mock_uds_data)

    def set_config_data(self, ecu):
        self.routine_control_p_data = self.routine_control_p_datas.get(ecu) if self.routine_control_p_datas else None
        self.data_info = self.data_infos.get(ecu) if self.data_infos else None
        self.dtc_code = self.dtc_codes.get(ecu) if self.dtc_codes else None

    def get_ecuname_from_doip_id(self, doip_id):
        # doip_id     0x1001
        if self.ecu_map_id:
            for ecu in self.ecu_map_id:
                if self.ecu_map_id.get(ecu)[0] == doip_id:
                    self.ecu = ecu
                    return self.ecu
            self.ecu = self.original_ecu
            return self.ecu
        else:
            self.ecu = self.original_ecu
            return self.ecu


    def is_complete(self, data):
        # Further improvement is needed to judge the doip data
        if len(data) >= 8:
            # logger.info(data[:8])
            # if data[0] == 0x02 and data[1] == 0xFD and data[2] == 0x80 and data[3] == 0x01:
            if data[0] == 0x02 and data[1] == 0xFD:
                self.slice_data = []
                length = (data[4] << 24) + (data[5] << 16) + (data[6] << 8) + data[7]
                if (len(data) - 8) >= length:
                    return True
                # logger.info(data[:8])
                logger.warning(f"接收的数据不完整，期望得到字节数：{length}，实际得到字节数：{len(data)}")
                # logger.info("incomplete payload, expected: %d, received: %d" % (length, len(data)))
        # logger.info("====== Actually Received: %d  =====" % (len(data)))
        logger.debug(f"实际得到字节数：{len(data)}。")
        return False

    def get_payload_from_data(self, data):
        if self.is_complete(data) == False:
            return ([], [])
        length = (data[4] << 24) + (data[5] << 16) + (data[6] << 8) + data[7]
        if len(data) == (8 + length):
            return (data[0:8], data[8:(8 + length)])
        elif len(data) > (8 + length):
            message = []
            while len(data) >= 8:
                if self.is_complete(data) == False:
                    return ([], [])
                length = (data[4] << 24) + (data[5] << 16) + (data[6] << 8) + data[7]
                message.append((data[0:8], data[8:(8 + length)]))
                data = data[(8 + length):]
            return message
        # return(data[0:8],data[8:])

    def diagnostic_parameter_reset(self):
        self.positive_ack = None
        self.timeout = P6_CLIENT_TIMEOUT

    def close(self):
        self.doip_tcp_server.close()

    def run(self):
        """
        @function new_connection(self)
        @brief This function is used to create a new connection to send data
        @return tcp_socket_client reference to a TCP socket
        """
        self.doip_tcp_server = TcpSocketServer("DoIP TCP Server Socket", ip=self.server_ip, port=self.server_port)
        self.doip_tcp_server.setup_response_callback(self.rx_diags_msgs)

        if self.server_doip_id == 0x1001:
            vehicle_announcement_data = DoipTp.construct_tx_signal_frames(payload_type=[0x00, 0x04],
                                                                          doip_entity_logical_address=[0x10, 0x01],
                                                                          vin=[0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30,
                                                                               0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30,
                                                                               0x30, 0x30, 0x30],
                                                                          eid=[0x02, 0, 0, 0, 0x10, 0x01],
                                                                          gid=[0, 0, 0, 0, 0, 0x01],
                                                                          further_action_required=[0x20])
            self.doip_udp_broadcast = UdpBroadcast("DoIP Udp Broadcast Socket", data=vehicle_announcement_data,
                                                   server_ip=self.server_ip)
            self.doip_udp_broadcast.start()
        try:
            self.doip_tcp_server.start()

        except OSError as e:
            logger.error(str(e) + ' : %s:%d' % (self.server_ip, self.server_port))
            return None

        if self.server_doip_id == 0x1001:
            i = 0
            while (not self.doip_tcp_server.connected_flag) and i < 10:
                i += 0.01
                time.sleep(0.01)
            self.doip_udp_broadcast.close()

    def get_sa_list(self):
        self.sa_list = [self.server_doip_id >> 8, self.server_doip_id & 0xFF]
        return self.sa_list

    def update_server_doip_id(self, doip_id):
        # doip_id     0x1001  or 0x1002
        self.server_doip_id = doip_id
        self.get_sa_list()

    # def send_data(self, data):
    #     # DIAG_MSG_TYPE
    #     self.diagnostic_parameter_reset()
    #     server_doip_id = [0x10, self.server_doip_id]
    #     diag_msg_data = DoipTp.construct_tx_signal_frames(payload_type=[0x80, 0x01], userdata=data,
    #                                                       sa=self.client_doip_id, ta=server_doip_id)

    def send_data_functional_addressing(self, data, interval_time=P3_CLIENT_MIN):
        # functional addressing
        server_doip_id = self.func_doip_id
        diag_msg_data = DoipTp.construct_tx_signal_frames(payload_type=[0x80, 0x01], userdata=data,
                                                          sa=self.client_doip_id, ta=server_doip_id)
        self.lock.acquire()
        self.msg_ack_received = None
        self.doip_tcp_server.send(diag_msg_data)
        userdata_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(data)
        logger.info("Functional Addressing UDS Data (Doip) : [Tx] {}".format(userdata_print))
        if not self.msg_ack_received_cycle_assert():
            self.msg_ack_received = None
            self.doip_tcp_server.send(diag_msg_data)
            if not self.msg_ack_received_cycle_assert():
                self.lock.release()
                raise RuntimeError("send_data_functional_addressing  msg_ack_received retry  ------  Timeout")
        self.lock.release()
        sleep(interval_time)

    # ****************************************
    def setup_data_callback(self, callBack, response_id):
        """
        @function setup_data_callback(self, callBack, response_id)
        @brief This function must be called before sending a diagnostics request to setup the 
               callback for the diagnostics response
        @param callBack Function callback for the message received
        @param response_id Can id of the intended recepient
        """
        #logger.info("Setup DoIP data callback to ")
        #logger.info(callBack)
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
                    logger.info("data is {}".format(messages))
                    for (doip_header, payload) in messages:
                        logger.info("Rx doip_header is {}".format(doip_header))
                        logger.info("Rx payload is {}".format(payload))
                        self.rx_data_handing(doip_header, payload)
                else:
                    doip_header, payload = self.get_payload_from_data(data)
                    logger.debug("Rx doip_header is {}".format(doip_header))
                    logger.debug("Rx payload is {}".format(payload))
                    self.rx_data_handing(doip_header, payload)
            else:
                # Temporary processing slice data UDS(TCP)
                if self.slice_data:
                    self.slice_data += data
                    slice_data = self.slice_data
                    if self.is_complete(slice_data):
                        self.rx_diags_msgs(slice_data)
                        self.slice_data = []
                else:
                    self.slice_data = data

    def rx_data_handing(self, doip_header, payload):
        protocol_version = doip_header[0]
        inverse_protocol_version = doip_header[1]
        payload_type = (doip_header[2] << 8) + doip_header[3]     # such as 0x8001
        reserved = doip_header[4:]
        if payload_type == DIAG_MSG_TYPE:


            # self.message_automatic_sent = None
            # sa = (payload[0] << 8) + payload[1]
            # ta = (payload[2] << 8) + payload[3]
            sa = payload[0:2]
            ta = payload[2:4]
            sa_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(sa)
            ta_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(ta)

            diagnostic_message_positive_acknowledgement = DoipTp.construct_tx_signal_frames(payload_type=[0x80, 0x02],
                                                                                            sa=ta, ta=sa)
            self.doip_tcp_server.send(diagnostic_message_positive_acknowledgement)

            self.userdata = payload[4:]
            self.sid = self.userdata[0]
            self.get_sub_data = self.userdata[1:]
            if self.sid not in [0x36]:
                self.userdata_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(self.userdata)
                # logger.info("UDS Data (Doip) : [Rx] {}".format(self.userdata_print))
                logger.info("[ {}]-->[ {}] | 数据：{}".format(sa_print, ta_print, self.userdata_print))
            elif self.sid in [0x36]:
                logger.info("RX sa is [ {}], ta is [ {}]".format(sa_print, ta_print))
                logger.info("Considering the performance, the 0x36 service is not displayed and sleep 3ms")
                sleep(0.003)   # Considering DUT performance , sleep 15ms

            if ta == self.func_doip_id:
                if self.get_sub_data:
                    if self.get_sub_data[0] >> 7 == 1:
                        self.diagnostic_services_p_data(self.sid, self.get_sub_data)
                    else:
                        if self.server_doip_id in [0x1001, 0x1002]:  # Determine whether it is a gateway
                            if self.ecu_map_id:
                                for ecu in self.ecu_map_id:
                                    id_int = self.ecu_map_id.get(ecu)[0]
                                    id_list = DataTypeHanding.int_to_int2list(id_int)
                                    self.ecu = ecu
                                    self.set_config_data(self.ecu)
                                    self.diagnostic_services_p_data(self.sid, self.get_sub_data)
                                    userdata = self.p_data
                                    send_data = DoipTp.construct_tx_signal_frames(payload_type=[0x80, 0x01], sa=id_list, ta=sa,
                                                                          userdata=userdata)
                                    self.doip_tcp_server.send(send_data)
                                    self.userdata_tx_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(
                                        userdata)
                                    logger.info("UDS Data (Doip) : [Tx] {}".format(self.userdata_tx_print))
                            else:
                                self.diagnostic_services_p_data(self.sid, self.get_sub_data)
                                userdata = self.p_data
                                send_data = DoipTp.construct_tx_signal_frames(payload_type=[0x80, 0x01], sa=self.sa_list, ta=sa,
                                                                              userdata=userdata)
                                self.doip_tcp_server.send(send_data)
                                self.userdata_tx_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(
                                    userdata)
                                logger.info("UDS Data (Doip) : [Tx] {}".format(self.userdata_tx_print))
                        else:
                            ta_int = DataTypeHanding.intlist_to_int(ta)
                            self.get_ecuname_from_doip_id(ta_int)
                            self.set_config_data(self.ecu)
                            self.diagnostic_services_p_data(self.sid, self.get_sub_data)
                            userdata = self.p_data
                            send_data = DoipTp.construct_tx_signal_frames(payload_type=[0x80, 0x01],
                                                                          sa=self.sa_list, ta=sa,
                                                                          userdata=userdata)

                            self.doip_tcp_server.send(send_data)
                            self.userdata_tx_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(userdata)
                            logger.info("UDS Data (Doip) : [Tx] {}".format(self.userdata_tx_print))
                else:
                    # Do not judge whether it is a gateway
                    self.diagnostic_services_p_data(self.sid, self.get_sub_data)
                    userdata = self.p_data
                    send_data = DoipTp.construct_tx_signal_frames(payload_type=[0x80, 0x01], sa=self.sa_list, ta=sa,
                                                                  userdata=userdata)
                    self.doip_tcp_server.send(send_data)
                    self.userdata_tx_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(userdata)
                    logger.info("UDS Data (Doip) : [Tx] {}".format(self.userdata_tx_print))
            else:
                if self.sid in [0x3E, 0x10, 0x11] and self.get_sub_data and self.get_sub_data[0] >> 7 == 1:
                    self.diagnostic_services_p_data(self.sid, self.get_sub_data)
                else:
                    if self.p_n_res:
                        if self.server_doip_id in [0x1001, 0x1002]:  # Determine whether it is a gateway
                            ta_int = DataTypeHanding.intlist_to_int(ta)
                            self.get_ecuname_from_doip_id(ta_int)
                            self.set_config_data(self.ecu)
                            self.diagnostic_services_p_data(self.sid, self.get_sub_data)
                            userdata = self.p_data
                            send_data = DoipTp.construct_tx_signal_frames(payload_type=[0x80, 0x01], sa=ta, ta=sa,
                                                                          userdata=userdata)
                        else:
                            ta_int = DataTypeHanding.intlist_to_int(ta)
                            self.get_ecuname_from_doip_id(ta_int)
                            self.set_config_data(self.ecu)
                            self.diagnostic_services_p_data(self.sid, self.get_sub_data)
                            userdata = self.p_data
                            # send_data = DoipTp.construct_tx_signal_frames(payload_type=[0x80, 0x01], sa=ta,
                            #                                               ta=sa,
                            #                                               userdata=userdata)

                            if ta == self.sa_list:
                                send_data = DoipTp.construct_tx_signal_frames(payload_type=[0x80, 0x01], sa=self.sa_list, ta=sa,
                                                                              userdata=userdata)
                            else:
                                with error_check(None, exception_error.DOIPError):
                                    raise AssertionError(
                                        f"当前mock的ecu地址：{bytes(self.sa_list).hex()} 于，远端发送过来的目标地址：{bytes(ta).hex()}，不匹配")
                                logger.error("ECU MOCK Config does not match the received doip_id")

                        self.doip_tcp_server.send(send_data)
                        self.userdata_tx_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(userdata)
                        logger.info("UDS Data (Doip) : [Tx] {}".format(self.userdata_tx_print))
                    else:
                        self.diagnostic_services_n_data()
                        userdata = self.n_data

                        # Do not judge whether it is a gateway
                        send_data = DoipTp.construct_tx_signal_frames(payload_type=[0x80, 0x01], sa=ta, ta=sa,
                                                                      userdata=userdata)
                        self.doip_tcp_server.send(send_data)
                        self.userdata_tx_print = DataTypeHanding.intlist_to_hexstr_capitalize_and_spaces(userdata)
                        logger.info("UDS Data (Doip) : [Tx] {}".format(self.userdata_tx_print))

        elif payload_type == DIAG_MSG_POS_ACK_TYPE:
            self.msg_ack_received = True
        elif payload_type == DIAG_MSG_NEG_ACK_TYPE:
            self.msg_ack_received = True
        elif payload_type == ROUTING_ACT_REQ_TYPE:
            routing_act_response_data = DoipTp.construct_tx_signal_frames(payload_type=[0x00, 0x06],
                                                                     doip_entity_logical_address=self.sa_list,
                                                                     routing_activation_response_code=[0x10])
            self.doip_tcp_server.send(routing_act_response_data)
        elif payload_type == ROUTING_ACT_RESP_TYPE:
            # self.msg_ack_received = True
            pass
        else:
            logger.info("Unexpected DoIP payload: [{}]".format(', '.join(hex(x) for x in doip_header)))


    # ****************************************
    def waiting_vehicle_announcement(self, req):
        """
        @todo Finish implement this function
        """
        self.log.info("Rx payload type:%s" % (req.get_payload_type()))
        self.log.info("Rx payload size:%s" % (req.get_payload_size()))
        self.log.info("Payload:%s" % (req.get_payload()))
        self.log.info.response_received = True
        return

    def waiting_vehicle_id(self, req):
        """
        @todo Finish implement this function
        """
        self.log.info("Rx payload type:%s" % (req.get_payload_type()))
        self.log.info("Rx payload size:%s" % (req.get_payload_size()))
        self.log.info("Payload:%s" % (req.get_payload()))
        self.response_received = True
        return

    # ****************************************
    def doVehicleDiscovery(self,UDP_IP="localhost", UDP_PORT=13400):
        """
        This function implements vehicle discovery.
        1. Waits for "Vehicle Announcement Message" received from DoIP Gateway in UDP port 13400
        2. Tester will send a "Vehicle Identification Request" in UDP port 13400
        3. Tester wait to receive a "Vehicle Identification Response" in UDP port 13400
        This test pass if:
            Annoucement message is received in time
            Vehicle Identification Response is received in time
        """
        global response_received
        #Setup
        #udp_socket_client
        #self.init_socket("UDP")
        #self.setup_rx(UDP_IP, UDP_PORT)
        self.setup_data_callback(self.waiting_vehicle_announcement,doip_payload.VEHICLE_ANN_TYPE)
        self.start()
        self.log.info("Waiting vehicle announcement")
        self.response_received = False
        self.timeout=0
        while True:
            try:
                if self.response_received:
                    self.log.info("Vehicle announcement received")
                    break
                time.sleep(.1)
            except KeyboardInterrupt:
                self.log.info("Exiting now...")
                self.shutdown()
                time.sleep(1)
                return
            time.sleep(.1)
            self.timeout += 1
            if self.timeout == 600: #1min
                self.log.info("Timeout to receive Vehicle announcement...")
                self.shutdown()
                time.sleep(1)
                return
        #transmit Vehicle ID request
        self.log.info("Sending Vehicle ID Request")
        payload=[0x02,0xFD,0x00,0x01,0x00,0x00,0x00,0x00]
        self.connect(UDP_IP, UDP_PORT)
        self.send(payload, UDP_IP, UDP_PORT)
        #Wait for Vehicle ID response
        self.setup_data_callback(self.waiting_vehicle_id, doip_payload.VEHICLE_ID_RESP_TYPE)
        self.response_received = False
        while True:
            try:
                if self.response_received:
                    self.log.info("Vehicle ID Response received")
                    self.log.info("Test PASS")
                    self.shutdown()
                    time.sleep(1)
                    return
                time.sleep(.1)
            except KeyboardInterrupt:
                self.log.info("Exiting now...")
                self.shutdown()
                time.sleep(1)
                return

# ****************************************************************************************
#                                UNIT TESTING FOR DoIP
# ****************************************************************************************
def test_cb(req):
    global response_received
    logger.info("Rx payload type:%s" % (req.get_payload_type()))
    logger.info("Rx payload size:%s" % (req.get_payload_size()))
    logger.info("Payload:%s" % (req.get_payload()))
    response_received = True
    return

# ****************************************************************************************
def test_send_callBack(req):
    logger.info("Diagnostics msg received")
    logger.info("Response:0x%X" % (req.get_response_code()))
    logger.info('Data: [{}]'.format(', '.join(hex(x) for x in req.get_data())))
    return

def testSend(IP, PORT, SERVER_IP, SERVER_PORT, payload, count):
    global response_received
    #Setup
    doipTester = doip(IP, PORT,"172.16.141.130", 13400)
    doipTester.setup_data_callback(test_send_callBack, 0x685)
    #Run unit test
    while count > 0:
        logger.info('Tx Data: [{}]'.format(', '.join(hex(x) for x in payload)))
        doipTester.send_data(0x605,payload)
        try:
            time.sleep(.1)
        except KeyboardInterrupt:
            doipTester.shutdown()
            time.sleep(1)
            return
        count -= 1

# ****************************************************************************************
def testReceive(IP="localhost", PORT=13400, SERVER="localhost"):
    global response_received
    #Setup
    doipTester = doip(IP, PORT, SERVER, PORT)
    #doipTester.init_socket(socketType)
    #doipTester.setup_rx(UDP_IP, UDP_PORT)
    doipTester.setup_data_callback(test_cb)
    doipTester.start()
    logger.info("Reception enabled")
    while(True):
        response_received = False
        while True:
            try:
                if response_received:
                    logger.info("-------------------------------------")
                    break
                time.sleep(.1)
            except KeyboardInterrupt:
                logger.info("Exiting now...")
                doipTester.shutdown()
                time.sleep(1)
                return

# ****************************************************************************************
def waiting_payload_type(req):
    global response_received
    logger.info("Rx:%s" % (req.get_payload_type()))
    logger.info("Rx payload size:%s" % (req.get_payload_size()))
    logger.info("Payload:%s" % (req.get_payload()))
    response_received = True
    return

# ****************************************************************************************
def testVehicleDiscovery(UDP_IP="localhost", UDP_PORT=13400):
    doipTester = doip(21, "DoIP Rx Thread")
    doipTester.doVehicleDiscovery(UDP_IP, UDP_PORT)
    return

# ****************************************************************************************
def read_file(filename):
    # Open a file
    fo = open(filename, "r+")
    sim_str = fo.read()
    data = list(sim_str)
    new_data = []
    byte_counter = 0
    new_byte = 0x00
    for letter in data:
        byte_counter = byte_counter + 1
        if byte_counter == 1:
            new_byte = letter
        else:
            new_byte = new_byte + letter
            # logger.info("%s",new_byte)
            new_data.append(new_byte)
            byte_counter = 0
    val = [int(x, base=16) for x in new_data]
    val = bytes(val)
    val = list(val)
    # logger.info(val[0:100])

    # Close opend file
    fo.close()
    return val

# ****************************************************************************************
def printHelp():
    print('test.py -t <test name> -i <IP address> -p <port> -d <data> -c <repeat>')

# ****************************************************************************************
def main(argv):
    global exitFlag
    test = "tx"
    ipAddress = "localhost"
    serverIP = "localhost"
    port = 13400
    payload = [0x10,0x01]
    count = 1
    try:
        opts, args = getopt.getopt(argv,"ht:i:p:d:c:s:",["test=","ipAddress=","port=","data=","count=", "serverAddress="])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            return
        elif opt in ("-t", "--test"):
            test = arg
        elif opt in ("-i", "--ipAddress"):
            ipAddress = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-s", "--serverAddress"):
            serverIP = arg
        elif opt in ("-c", "--count"):
            count = int(arg)
        elif opt in ("-d", "--data"):
            data = arg
            data=data.split(',')
            payload=[]
            for value in data:
                payload.append(int(value,16))


    print("Running %s test" % (test))
    if test == "discover":
        testVehicleDiscovery(ipAddress, port)
    elif test == "file":
        read_file(filename)
    elif test == "tx":
        testSend(ipAddress, port, serverIP, port, payload, count )
    elif test == "rx":
        testReceive(ipAddress, port)
    else:
        print("Invalid test specified: %s" % (test))
    print("Test End")
    return

# ****************************************************************************************
if __name__ == '__main__':
    if len(sys.argv) < 2:
        printHelp()
        sys.exit(0)
    main(sys.argv[1:])


