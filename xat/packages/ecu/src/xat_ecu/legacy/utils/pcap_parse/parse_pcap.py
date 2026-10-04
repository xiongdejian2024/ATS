# -*- coding: utf-8 -*-

"""
@Time    : 2024/9/26 14:26 下午
@Author  : songjian.lin
@Email   : songjian.lin@jiduauto.com
@Description : 解析pcap报文: PTPv2、tcp
@Examples    :
"""

from scapy.all import *

from xat_ecu.legacy.common.logger import Logger

message_type_dict = {0: "Sync", 2: "Peer_Delay_Req", 8: "Follow_Up", 10: 'Peer_Delay_Resp_Follow_Up'}


class PcapParseInfo:
    """解析pcap中bgm内部以太网信号的值"""

    def __init__(self):
        self.last_frame_dict = {}
        self.sync_time_gt_250ms = []  # SYNC间隔125ms；
        self.peer_delay_req_sequence_err = []  # Peer_Delay_Req头中的sequenceId依次+1累加；
        self.peer_delay_resp_follow_up_sequence_err = []  # Peer_Delay_Resp_Follow_Up 头中的sequenceId应当与Peer_Delay_Resp头中的sequenceId相同
        self.follow_up_sequence_err1 = []  # FOLLOW_UP头中的sequenceId应当与SYNC头中的sequenceId相同
        self.follow_up_sequence_err2 = []  # FOLLOW_UP头中的sequenceId依次+1累加
        self.correction_gt_10s = []  # correction 字段值不超过10s
        self.tcp_keyword_hex_epoch_time = []

    def parse_ptp_pcap_file(self, pcap_file, filter_date_list=None, exclude_year_list=None, follow_up_time=125):
        """
        解析PTPv2协议的以太网报文
        @param pcap_file : 待解析的pcap文件
        @param filter_date_list : correction 字段值不超过10s的前提是 preciseOriginTimestamp的日期字符串必须在其内
        @param exclude_year_list: correction 字段值不超过10s的前提是 preciseOriginTimestamp的四位年份不能在其内
        @param follow_up_time: 连续的 Sync Message 允许的最大毫秒时间
        """
        pkt = rdpcap(pcap_file)

        i = 0
        for data in pkt:
            i = i + 1
            # logger.info(data.src)
            # logger.info(f'{i} {bytes(data).hex()}')
            # logger.info(f'{i} {bytes(data["Raw"].load).hex()}')
            # logger.info(data.fields['type'])
            ptp_current = ptp_parse(bytes(data["Raw"].load).hex(), i, data.time)
            if ptp_current.message_type == "Follow_Up":
                if filter_date_list:
                    if ptp_current.precise in filter_date_list:
                        if exclude_year_list:
                            if ptp_current.precise.split('-')[0] not in exclude_year_list:
                                if ptp_current.correction > 10:
                                    self.correction_gt_10s.append((ptp_current.idx, ptp_current.correction))
                        else:
                            if ptp_current.correction > 10:
                                self.correction_gt_10s.append((ptp_current.idx, ptp_current.correction))
                else:
                    if exclude_year_list:
                        if ptp_current.precise.split('-')[0] not in exclude_year_list:
                            if ptp_current.correction > 10:
                                self.correction_gt_10s.append((ptp_current.idx, ptp_current.correction))
                    else:
                        if ptp_current.correction > 10:
                            self.correction_gt_10s.append((ptp_current.idx, ptp_current.correction))

            if ptp_current.message_type not in self.last_frame_dict:
                self.last_frame_dict[ptp_current.message_type] = ptp_current
            else:
                if ptp_current.message_type == "Sync":
                    if (ptp_current.time_ms - self.last_frame_dict["Sync"].time_ms) > follow_up_time:
                        self.sync_time_gt_250ms.append((self.last_frame_dict["Sync"].idx, ptp_current.idx,
                                                        ptp_current.time_ms - self.last_frame_dict["Sync"].time_ms))
                if ptp_current.message_type == "Peer_Delay_Req":
                    if not ((ptp_current.sequenceId - self.last_frame_dict["Peer_Delay_Req"].sequenceId) == 1):
                        self.peer_delay_req_sequence_err.append(
                            (self.last_frame_dict["Peer_Delay_Req"].idx, ptp_current.idx))

                if ptp_current.message_type == 'Peer_Delay_Resp_Follow_Up':
                    if "Peer_Delay_Req" in self.last_frame_dict:
                        if not (ptp_current.sequenceId == self.last_frame_dict["Peer_Delay_Req"].sequenceId):
                            self.peer_delay_resp_follow_up_sequence_err.append(
                                (self.last_frame_dict["Peer_Delay_Req"].idx, ptp_current.idx))

                if ptp_current.message_type == "Follow_Up":
                    if "Sync" in self.last_frame_dict:
                        if not (ptp_current.sequenceId == self.last_frame_dict["Sync"].sequenceId):
                            self.follow_up_sequence_err1.append(
                                (self.last_frame_dict["Sync"].idx, ptp_current.idx))
                    if not ((ptp_current.sequenceId - self.last_frame_dict["Follow_Up"].sequenceId) == 1):
                        self.follow_up_sequence_err2.append(
                            (self.last_frame_dict["Follow_Up"].idx, self.last_frame_dict["Follow_Up"].sequenceId,
                             ptp_current.idx, ptp_current.sequenceId))

                self.last_frame_dict[ptp_current.message_type] = ptp_current

    def parse_tcp_pcap_file(self, pcap_file, ip_src, tcp_keyword_hex):
        """
        解析pcap文件，过滤其中的TCP报文，并过滤TCP的payload中包含tcp_keyword_hex的报文
        @param pcap_file: 待解析的pcap文件
        @param ip_src：tcp报文的发送方IP地址
        @param tcp_keyword_hex：tcp的payload中包含的16进制字符串
        """
        pkt = rdpcap(pcap_file)
        i = 0
        for data in pkt:
            i = i + 1
            if "Raw" not in data:
                continue
            if 'TCP' in data:
                hex_string = ''.join(hex(b)[2:].zfill(2) for b in data["Raw"].load)
                if data["IP"].src == ip_src:
                    if tcp_keyword_hex in hex_string:
                        self.tcp_keyword_hex_epoch_time.append((i, float(data.time)))
        else:
            logger.info(self.tcp_keyword_hex_epoch_time)


class ptp_parse:
    def __init__(self, hex_data_str, idx, time_s):
        self.time_ms = int(time_s * 1000)
        self.idx = idx
        self.message_type = ""
        self.sequenceId = 0
        self.correction = 0  # 单位是ns
        self.parse_ptp_frame(hex_data_str)
        self.precise = ""

    def parse_ptp_frame(self, hex_data_str):
        self.message_type = message_type_dict.get(int(hex_data_str[1], 16))
        self.sequenceId = int(hex_data_str[60:64], 16)
        self.correction = int(hex_data_str[16:28], 16) / 1000000000
        self.precise = datetime.fromtimestamp(int(hex_data_str[64:70], 16)).strftime("%Y-%m-%d")

    def to_string(self):
        logger.info(vars(self))


if __name__ == '__main__':
    logger = Logger().get_logger("test")
    test = PcapParseInfo()
    date_list = ['2024-09-20', '2024-09-21']
    # test.parse_pcap_file("TCAM_20240920_10_40_16.pcap_parse", date_list)
    test.parse_tcp_pcap_file("2024-09-27.pcap_parse", "172.16.5.2", "4e33")
