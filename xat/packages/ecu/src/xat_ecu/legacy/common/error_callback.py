# -*- coding: utf-8 -*-
"""
@File        : error_callback.py
@Author      : lei.hong@jiduauto.com
@Time        : 2024/7/2 14:49
@Description : 根据错误码信息，做相应的处理，例如：抓取log，查询状态等
@Examples    :
"""
import time
from datetime import datetime
from typing import Union
from xat_ecu.legacy.common.error_code import StatusCode
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.nuc_app import exec_shell

# 定义处理每个错误码的函数

## bus异常         01
# TOSUNCAN_INIT_ERR = ('10401', '同星can初始化异常')
def handle_tosuncan_init_err(*args, **kwargs):
    a = args[0]
    print(f"**********************************{args},{a}")
    error_message = kwargs.get('error_message')
    cmd = kwargs.get('cmd')
    time.sleep(5)
    logger.info(f"#############{error_message}")
    logger.info(f"#############{cmd}")
    pass
    # TODO: 抓取log
# TOSUN_MINI_PROGRAM_START_ERR = ('10802', '同星小程序启动失败，请确认环境是否正常')
def handle_tosuncan_mini_program_start_err(*args, **kwargs):
    # 检查进程是否存在
    logger.info("#######检查进程是否存在########")
    result = exec_shell("ps aux")
    output = result["output"]
    if 'IniMap' in output:
        logger.info("IniMap运行中")
    else:
        logger.error("IniMap没有在运行")
    
# TOSUN_MINI_PROGRAM_CONNECT_ERR = ('10803', 'UDP连接同星小程序失败，请确认同星小程序已启动')
def handle_tosun_mini_program_connect_err(*args, **kwargs):
    # 检查进程是否存在
    logger.info("#######检查同星小程序是否启动########")
    result = exec_shell("ps aux")
    output = result["output"]
    if 'IniMap' in output:
        logger.info("同星小程序已启动")
    else:
        logger.error("同星小程序未启动")
    
# TOSUNFR_INIT_ERR = ('10301', '同星FR初始化异常')

# TOMOSSLIN_INIT_ERR = ('10501', '图莫斯LIN初始化异常')
# TOMOSSLIN_LIN_EX_USB_WRITE_FAIL_ERR = ('10502', '图莫斯LIN写数据失败,一般是由于LIN线程未释放导致,请检查前后case是否有操作lin未释放')
def handle_tomoslin_ex_usb_write_fail_err(*args, **kwargs):
    # dmesg log中获取当前持有lin的pytest信息
    msg = []
    count = 1
    error_str = "(pytest) did not claim interface 0 before use"
    boot_time_s = exec_shell(f'uptime -s')["output"].split("\n")[0]
    boot_time = datetime.strptime(boot_time_s, "%Y-%m-%d %H:%M:%S").timestamp()
    current_time = int(time.time())
    lines = exec_shell("dmesg")["output"].split("\n")
    for line in lines:
        if line.strip() == "":
            continue
        parts = line.split(None, 5)  # 按空格分割，但只分割一次以保留消息部分
        if len(parts) > 1:
            for p in parts:
                if any(p.startswith(str(i)) for i in range(10)):
                    p_time = p
                    break
            # timestamp_s = p_time[:-1].split('.')
            timestamp = int(p_time[:-1].split('.')[0]) 
            # 取5秒内的打印
            if current_time - (timestamp + boot_time) <= 5:
                msg.append(line)
                if error_str in line:
                    count += 1
    if count > 2:
        log_print("出现多个pytest进程异常占用LIN，请处理！！！！")
    for i in msg:
        logger.info(i)
# TOMOSSLIN_LIN_EX_CMD_FAIL_ERR = ('10503', '图莫斯LIN命令执行失败，请重新插拔lin')
# TOMOSSLIN_LIN_EX_CH_NO_INIT_ERR = ('10504', '图莫斯LIN通道未初始化，请确认设备通道已初始化')
# TOMOSSLIN_LIN_RUN_ERR = ('10505', '图莫斯LIN线程运行执行报错，请排查相关线程代码')
# TOMOSSLIN_LIN_LOG_WRITE_ERR = ('10506', '图莫斯LIN线程写入日志报错，可能是内存不足或数据格式错误')

# IPDU_DATABASE_ERR = ('10601', '获取到的BGM版本对应的数据库中信号属性错误，解决方法两种：第一种：升级域控台架; 第二种：临时将运行命令后面加上指定版本，如：--bl_ver=v_2_0_0')
# IPDU_DATA_NONE_ERR = ('10602', '总线上获取到的数据为None，可能是同星收发线程因脏数据异常退出')
def handle_ipdu_data_none_err(*args, **kwargs):
    # 打印的ipdu的数据
    obj = kwargs.get('obj', None)
    bus_name = kwargs.get('bus_name', None)
    logger.info(f"#######打印的ipdu {bus_name}的数据########")
    timeout = 0.1
    start_time = time.time()
    while time.time() - start_time < timeout:
        if obj is None:
            return
        else:
            logger.info(obj.bus_pdu_dict.get(bus_name))
    

## diagmock异常    02

## io异常          03

## log异常         04

## sdtest异常      05
# DOIP_INIT_ERR = ('50101', 'doip初始化异常')
# DOIP_CONNECT_ERR = ('50102', 'doip连接失败，原因可能是obd ip获取不到')
# DOIP_DISCONNECT_ERR = ('50103', 'doip断开异常')
# DOIP_SEND_ERR = ('50104', 'doip发送异常')
# DOIP_RECV_ERR = ('50105', 'doip接收异常')
# DOIP_TIMEOUT_ERR = ('50106', 'doip超时异常')
# DOIP_RETRANSMISSION_ERR = ('50107', 'doip重传消息异常')
# DOIP_OBD_ERR = ('50108', 'doip获取台架OBD的IP失败，原因可能是没有配置OBD网络')
# DOIP_ADDR_OR_PORT_MULTIPLEX_ERR = ('50109', 'doip连接地址端口复用异常')
# DOIP_SEND_DATA_TYPE_ERR = ('50110', 'doip发送的数据类型异常')
# DOIP_MOCK_DATA_TYPE_ERR = ('50111', 'doip回复的mock数据类型错误，请仔细核对')
# DOIP_SESSION_ERR = ('50112', 'doip当前会话等级错误')
# DOIP_INSTANCE_ERR = ('50113', 'doip实例化多个client sim，请确保同一个ip只连接一个诊断客户端')
# DOCAN_LEN_ERR = ('50201', 'docan数据帧最大长度小于当前有帧有效长度')
# DOCAN_SINGLE_FRAME_LEN_ERR = ('50202', 'docan单帧数据长度错误')
def handle_docan_len_err(*args, **kwargs):
    logger.info("#######检查docan单帧数据长度########")
    data = args[0]
    length = args[1]
    logger.info(f"docan单帧数据: {data}, 长度为: {length}")
    
# DOCAN_ECU_NOT_FOUND_ERR = ('50203', 'docan当前设置的ecu没有启动，请仔细检查ecu输入是否写对')

# 无对应处理时进行默认处理
def handle_unknown_error(**kwargs):
    error_message = kwargs.get('error_message')
    logger.info(f"未配置错误，执行默认处理: {error_message}")


# 映射函数处理
error_handlers = {
    StatusCode.TOSUNCAN_INIT_ERR: handle_tosuncan_init_err,
    StatusCode.TOSUN_MINI_PROGRAM_START_ERR: handle_tosuncan_mini_program_start_err,
    StatusCode.TOSUN_MINI_PROGRAM_CONNECT_ERR: handle_tosun_mini_program_connect_err,
    StatusCode.IPDU_DATA_NONE_ERR: handle_ipdu_data_none_err,
    StatusCode.DOCAN_SINGLE_FRAME_LEN_ERR: handle_docan_len_err,
    StatusCode.TOMOSSLIN_LIN_EX_USB_WRITE_FAIL_ERR: handle_tomoslin_ex_usb_write_fail_err,

}


def error_callback(*args, **kwargs):
    """
    错误处理回调函数。
    
    Args:
        *args: 可变数量的位置参数，传递给错误处理函数。
        **kwargs: 可变数量的关键字参数，包含以下参数：
            error_message (Optional[ErrorMessageType]): 错误消息类型，默认为None。
    
    """
    error_message = kwargs.get('error_message', None)
    if error_message is None:
        return
    # 尝试从字典中获取处理函数并执行它
    handler = error_handlers.get(error_message, handle_unknown_error)
    if handler:
        log_print(f"开始{error_message.name} 错误处理回调函数: {handler.__name__}")
        handler(*args, **kwargs)
        log_print(f"结束{error_message.name} 错误处理回调函数: {handler.__name__}")
    else:
        logger.info(f"获取执行函数异常，错误类型为: {error_message}")


def log_print(message):
    dim = '*' * 60
    logger.info(dim)
    logger.info('    ' + message)
    logger.info(dim)



# 示例使用
if __name__ == "__main__":
    from xat_ecu.legacy.common.logger import logger, Logger
    from xat_ecu.legacy.common import exception_error
    from xat_ecu.legacy.common.exception_error import error_check
    logger = Logger().get_logger("test")
    # error_callback(StatusCode.TOSUNCAN_INIT_ERR)
    with error_check(StatusCode.TOSUN_MINI_PROGRAM_START_ERR, exception_error.DOCANError, error_callback, "67", cmd="test"):
        raise

