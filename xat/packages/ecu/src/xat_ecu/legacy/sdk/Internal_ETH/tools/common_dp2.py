# -*- coding: utf-8 -*-

"""
@File        : common_dp20.py
@Author      : jiabin.zhu@jiduatuo.com
@Time        : 2024/10/22 16:51 PM
@Description : DP2.0服务
@Examples    : example of how to use it
"""


class UdpChannel:
    # 仿真用到
    CCUMCUAD_Multicast = 'AdMcuSoAdUDP_Multicast'
    CCUMCUCD_Multicast = 'CdMcuSoAdUDP_Multicast'
    LcuL_Multicast = 'LcuLSoAdUDP_Multicast'
    LcuR_Multicast = 'LcuRSoAdUDP_Multicast'
    LcuL_CCUSOCCD = 'LcuLSoAdUDP_CdSocSoAdUDP'
    LcuR_CCUSOCCD = 'LcuRSoAdUDP_CdSocSoAdUDP'
    CCUMCUAD_CCUSOCCD = 'AdMcuSoAdUDP_CdSocSoAdUDP'
    CCUMCUCD_CCUSOCCD = 'CdMcuSoAdUDP_CdSocSoAdUDP'
    # 仿真可能用到
    # CCUMCUCD_CdSocLogCdMcuSoAdUDP = 'CdMcuSoAdUDP_CdSocLogCdMcuSoAdUDP'
    # LcuL_CdSocLogLcuLSoAdUDP = 'LcuLSoAdUDP_CdSocLogLcuLSoAdUDP'
    # LcuR_CdSocLogLcuRSoAdUDP = 'LcuRSoAdUDP_CdSocLogLcuRSoAdUDP'
    # # 仿真用不到
    # CCUMCUCD_CCUSOCAD = 'CdMcuSoAdUDP_AdSocSoAdUDP'
    # CCUMCUAD_CCUSOCAD = 'AdMcuSoAdUDP_AdSocSoAdUDP'
    # CCUMCUCD_CCUMCUAD = 'CdMcuSoAdUDP_AdMcuSoAdUDP'
    # CdNadSoAdUDP_CCUMCUCD = 'CdNadSoAdUDP_CdMcuSoAdUDP'
    # LcuL_CCUMCUAD = 'LcuLSoAdUDP_AdMcuSoAdUDP'
    # LcuL_CCUMCUCD = 'LcuLSoAdUDP_CdMcuSoAdUDP'
    # LcuR_LcuL = 'LcuRSoAdUDP_LcuLSoAdUDP'
    # LcuR_CCUMCUCD = 'LcuRSoAdUDP_CdMcuSoAdUDP'


class TcpChannel:
    CdMcuTCPServer_CdNadTCPClient1 = 'CdMcuTCPServer_CdNadTCPClient1'
    CdMcuTCPServer_CdSocPMTCPClient = 'CdMcuTCPServer_CdSocPMTCPClient'
    CdMcuTCPServer_CdSocTCPClient1 = 'CdMcuTCPServer_CdSocTCPClient1'
    AdMcuTCPServer_AdSocTCPClient = 'AdMcuTCPServer_AdSocTCPClient'
    AdMcuTCPServer_CdSocTCPClient2 = 'AdMcuTCPServer_CdSocTCPClient2'
    LcuLTCPServer_CdSocTCPClient3 = 'LcuLTCPServer_CdSocTCPClient3'
    LcuRTCPServer_CdSocTCPClient4 = 'LcuRTCPServer_CdSocTCPClient4'


# JET2.0 以太网拓扑
SOCKET_IP_PORT = {
    'CdMcuTCPServer': ('172.20.5.12', 30503),
    'AdMcuTCPServer': ('172.20.5.22', 30503),
    'LcuLTCPServer': ('172.20.5.1', 30503),
    'LcuRTCPServer': ('172.20.5.2', 30503),
    'CdSocTCPClient1': ('172.20.5.11', 30513),
    'CdSocTCPClient2': ('172.20.5.11', 30523),
    'CdSocTCPClient3': ('172.20.5.11', 30533),
    'CdSocTCPClient4': ('172.20.5.11', 30543),
    'AdSocTCPClient2': ('172.20.5.21', 30523),
    'CdNadTCPClient1': ('172.20.5.31', 30513),
    'CdSocPMTCPClient': ('172.20.5.11', 30504),

    'AdMcuSoAdUDP': ('172.20.5.22', 30501),
    'AdSocSoAdUDP': ('172.20.5.21', 30501),
    'Multicast': ('172.20.5.11', 30501),
    'CdMcuSoAdUDP': ('172.20.5.12', 30501),
    'CdSocSoAdUDP': ('172.20.5.11', 30501),
    'LcuLSoAdUDP': ('172.20.5.1', 30501),
    'LcuRSoAdUDP': ('172.20.5.2', 30501),
    'CdNadSoAdUDP': ('172.20.5.31', 30501),
    'CdSocLogCdMcuSoAdUDP': ('172.20.5.11', 30506),
    'CdSocLogLcuLSoAdUDP': ('172.20.5.11', 30507),
    'CdSocLogLcuRSoAdUDP': ('172.20.5.11', 30508)
}

# JET2.0 服务端和客户端拓扑
TCP_SC_CONFIGS = {
    'CdMcuTCPServer': ['CdSocTCPClient1', 'CdNadTCPClient1', 'CdSocPMTCPClient'],
    'AdMcuTCPServer': ['CdSocTCPClient2', 'AdSocTCPClient2'],
    'LcuLTCPServer': ['CdSocTCPClient3'],
    'LcuRTCPServer': ['CdSocTCPClient4'],
}

# 服务端
SERVER_SENDER_MAP = {
    'AdMcuSoAdUDP': 'CCUMCUAD',
    'CdMcuSoAdUDP': 'CCUMCUCD',
    'LcuLSoAdUDP': 'LCUL',
    'LcuRSoAdUDP': 'LCUR',
    'CdMcuTCPServer': 'CCUMCUCD',
    'AdMcuTCPServer': 'CCUMCUAD',
    'LcuLTCPServer': 'LCUL',
    'LcuRTCPServer': 'LCUR',
}


if __name__ == '__main__':
    for x in vars(TcpChannel):
        print(x)
