#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :error_code.py
@Time         :2024/6/21 15:21
@Author       :dejian.xiong@jiduauto.com
@Description  :记录全局异常的错误码
"""
from enum import Enum

"""
错误码格式:一共5位
1. 前一位表示是10大对象
    bus异常         1
    diagmock异常    2
    io异常          3
    log异常         4
    sdtest异常      5
    serial异常      6
    soa异常         7
    ssh异常         8
    tsp异常         9
2. 中间两位表示十大对象下每个分类的异常，不可重复
    doip            01
    docan           02
    tosunfr         03
    tosuncan        04
    tomosslin       05
    ipdu            06
    tcp             07
    udp             08
    none            00           
3. 后两位表示具体异常描述，可重复
"""


class StatusCode(Enum):
    """错误码枚举类"""
    # bus异常         01
    TOSUNCAN_INIT_ERR = ('10401', '同星can初始化异常')
    TOSUN_MINI_PROGRAM_START_ERR = ('10802', '同星小程序启动失败，请确认环境是否正常')
    TOSUN_MINI_PROGRAM_CONNECT_ERR = ('10803', 'UDP连接同星小程序失败，请确认同星小程序已启动')

    TOSUNFR_INIT_ERR = ('10301', '同星FR初始化异常')

    TOMOSSLIN_INIT_ERR = ('10501', '图莫斯LIN初始化异常')
    TOMOSSLIN_LIN_EX_USB_WRITE_FAIL_ERR = ('10502', '图莫斯LIN写数据失败,一般是由于LIN线程未释放导致,请检查前后case是否有操作lin未释放')
    TOMOSSLIN_LIN_EX_CMD_FAIL_ERR = ('10503', '图莫斯LIN命令执行失败，请重新插拔lin')
    TOMOSSLIN_LIN_EX_CH_NO_INIT_ERR = ('10504', '图莫斯LIN通道未初始化，请确认设备通道已初始化')
    TOMOSSLIN_LIN_RUN_ERR = ('10505', '图莫斯LIN线程运行执行报错，请排查相关线程代码')
    TOMOSSLIN_LIN_LOG_WRITE_ERR = ('10506', '图莫斯LIN线程写入日志报错，可能是内存不足或数据格式错误')
    TOMOSSLIN_LIN_POWER_ERR = ('10507', '图莫斯LIN电源异常，请检查LIN电源HUB接口是否松动，重新插拔进行恢复')

    IPDU_DATABASE_ERR = ('10601', 'BGM对应的数据库中获取不到该信号，解决思路如下：1.检查信号名称是否错误 2.如果是新版本的数据库，联系测开适配新的数据库 3.检查加载的数据库版本与BGM依赖的数据库版本是否一致，包括车型电池类型等')
    IPDU_DATA_NONE_ERR = ('10602', '总线上获取到的数据为None，可能是同星收发线程因脏数据异常退出')

    # diagmock异常    02

    # io异常          03

    # log异常         04

    # sdtest异常      05
    DOIP_INIT_ERR = ('50101', 'doip初始化异常')
    DOIP_CONNECT_ERR = ('50102', 'doip连接失败，原因可能是obd ip获取不到')
    DOIP_DISCONNECT_ERR = ('50103', 'doip断开异常')
    DOIP_SEND_ERR = ('50104', 'doip发送异常')
    DOIP_RECV_ERR = ('50105', 'doip接收异常')
    DOIP_TIMEOUT_ERR = ('50106', 'doip超时异常')
    DOIP_RETRANSMISSION_ERR = ('50107', 'doip重传消息异常')
    DOIP_OBD_ERR = ('50108', 'doip获取台架OBD的IP失败，原因可能是没有配置OBD网络')
    DOIP_ADDR_OR_PORT_MULTIPLEX_ERR = ('50109', 'doip连接地址端口复用异常')
    DOIP_SEND_DATA_TYPE_ERR = ('50110', 'doip发送的数据类型异常')
    DOIP_MOCK_DATA_TYPE_ERR = ('50111', 'doip回复的mock数据类型错误，请仔细核对')
    DOIP_SESSION_ERR = ('50112', 'doip当前会话等级错误')
    DOIP_INSTANCE_ERR = ('50113', 'doip实例化多个client sim，请确保同一个ip只连接一个诊断客户端')
    DOCAN_LEN_ERR = ('50201', 'docan数据帧最大长度小于当前有帧有效长度')
    DOCAN_SINGLE_FRAME_LEN_ERR = ('50202', 'docan单帧数据长度错误')
    DOCAN_ECU_NOT_FOUND_ERR = ('50203', 'docan当前设置的ecu没有启动，请仔细检查ecu输入是否写对')

    # serial异常      06

    # soa异常         07

    # ssh异常         08

    # tsp异常         09

    @property
    def code(self):
        """获取状态码"""
        return self.value[0]

    @property
    def errmsg(self):
        """获取状态码信息"""
        return self.value[1]

    @property
    def format_err_msg(self):
        """格式化错误信息"""
        return f'错误码:[{self.code}] 错误描述:{self.errmsg}'
