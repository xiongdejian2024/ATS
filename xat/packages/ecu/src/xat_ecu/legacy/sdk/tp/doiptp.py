# -*- coding: utf-8 -*-
"""
@File        : doiptp.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-03-13 10:02
@Description : doiptp ---- Assemble the data according to the requirements of doip diagnosis
"""
from xat_ecu.legacy.common.logger import logger


class DoipTp:

    @staticmethod
    def construct_tx_signal_frames(payload_type=None, userdata=[], nack_code=[0x02], sa=[0x0E, 0x80],
                                   ta=[0x00, 0x5F], protocol_version=0x02, tester_logical_address=[0x0E, 0x80],
                                   doip_entity_logical_address=[0x10, 0x01], routing_activation_response_code=[0x10],
                                   activation_type=[0x00], vin=[0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30,
                                                              0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30],
                                   eid=[0x02, 0, 0, 0, 0x10, 0x01], gid=[0, 0, 0, 0, 0, 0x01],
                                   further_action_required=[0x20]):
        # :parameter payload_type     type: list                list must be [0x00,0x01] ,  [0x80,0x01]  
        # :parameter payload          type: list or byte        list must be [0x10,0x20,0x12,0xED,...]
        # :parameter activation_type             RAREQC_LOCAL 0xE2             RAREQC_REMOTE 0xE3

        if payload_type is None:
            payload_type = [0x80, 0x01]
        payload = []
        logger.debug("Tx payload_type is {}".format(payload_type))
        if payload_type == [0x80, 0x01]:
            diagnostic_message = sa + ta + userdata
            payload = diagnostic_message
        elif payload_type == [0x80, 0x02]:
            ack_code = [0x00]
            diagnostic_message_positive_acknowledgement = sa + ta + ack_code
            payload = diagnostic_message_positive_acknowledgement
        elif payload_type == [0x80, 0x03]:
            diagnostic_message_negative_acknowledgement = sa + ta + nack_code
            payload = diagnostic_message_negative_acknowledgement
        elif payload_type == [0x00, 0x04]:
            vehicle_announcement = vin + doip_entity_logical_address + eid + gid + further_action_required
            payload = vehicle_announcement
        elif payload_type == [0x00, 0x05]:
            source_address = [0x0E, 0x80]
            reserved = [0x00, 0x00, 0x00, 0x00]
            routing_activation_request = source_address + activation_type + reserved
            payload = routing_activation_request
        elif payload_type == [0x00, 0x06]:
            reserved = [0x00, 0x00, 0x00, 0x00]
            routing_activation_response = tester_logical_address + doip_entity_logical_address + \
                                          routing_activation_response_code + reserved
            payload = routing_activation_response
        elif payload_type == [0x00, 0x07]:
            alive_chk_req = []
            payload = alive_chk_req
        elif payload_type == [0x00, 0x08]:
            alive_chk_resp = sa
            payload = alive_chk_resp
        else:
            payload_type = [0x80, 0x01]
            logger.info("error..........")

        inverse_protocol_version = protocol_version ^ 0xFF
        payload_length = [len(payload) >> 24] + [(len(payload) >> 16) & 0xFF] + [(len(payload) >> 8) & 0xFF] + [
            len(payload) & 0xFF]
        # ignore Payload type specific message content

        doip_header = [protocol_version] + [inverse_protocol_version] + payload_type + payload_length
        doip_data = doip_header + payload
        return doip_data

    @staticmethod
    def construct_tx_multi_frames(data):
        pass

    @staticmethod
    def deconstruct_rx_signal_frames(msg):
        pass
