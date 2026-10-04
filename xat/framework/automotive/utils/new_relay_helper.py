import sys
import os
import time




from xat_ecu.legacy.common.logger import *
from scapy.all import *
import serial
import serial.tools.list_ports
from serial import SerialException

os.environ["LOGGER"] = "logger"  # 防止 ecu sim logger 多打印


def get_jy_dam_port():
    jy_dam_port = None
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) == 0:
        logger.info('无可用串口')
    else:
        for i in range(0, len(port_list)):
            port = str(port_list[i]).split(" - ")
            if "CP2102" in port[1]:
                jy_dam_port = port[0]
                break
        else:
            logger.info("没有可以的jy dam继电器")
    return jy_dam_port


def convert_data(my_string):
    my_int = int(my_string, 16)
    my_data = my_int.to_bytes((len(my_string) + 1) // 2, byteorder='big')
    return my_data


def jy_dam0800_operation(operation_type, operation_target=None):
    port = get_jy_dam_port()
    if port is None:
        logger.error("没有找到可用的Jy DAM 继电器，继电器控制失败。")
        return
    try:
        bps = 9600
        # 超时时间,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
        time = 5
        data_dict = {"COM1": {"open": "FE050000FF009835", "close": "FE0500000000D9C5", "query": "FE0100000001E9C5"},
                     "COM2": {"open": "FE050001FF00C9F5", "close": "FE05000100008805", "query": "FE0100010001B805"},
                     "COM3": {"open": "FE050002FF0039F5", "close": "FE05000200007805", "query": "FE01000200014805"},
                     "COM4": {"open": "FE050003FF006835", "close": "FE050003000029C5", "query": "FE010003000119C5"},
                     "COM5": {"open": "FE050004FF00D9F4", "close": "FE05000400009804", "query": "FE0100040001A804"},
                     "COM6": {"open": "FE050005FF008834", "close": "FE0500050000C9C4", "query": "FE0100050001F9C4"},
                     "COM7": {"open": "FE050006FF007834", "close": "FE050006000039C4", "query": "FE010006000109C4"},
                     "COM8": {"open": "FE050007FF0029F4", "close": "FE05000700006804", "query": "FE01000700015804"}}
        # 打开串口，并返回串口对象
        uart = serial.Serial(port, bps, timeout=time)

        if operation_type == 'query':
            result = {}
            for key in data_dict:
                # 串口接收一个字符串
                receive_data = b''
                byte_data = convert_data(data_dict.get(key).get(operation_type))
                # 串口发送一个字符串
                data_len = uart.write(byte_data)

                for i in range(6):
                    receive_data += uart.read()
                if len(receive_data) != 6:
                    logger.info("指令发送失败")
                    return result
                else:
                    data = list(receive_data)
                    if data[3] == 1:
                        result[key] = 1
                        # logger.info(f"{key} 当前的状态为 1")
                    else:
                        result[key] = 0
                        # logger.info(f"{key} 当前的状态为 0")
            else:
                return result
        else:
            # logger.info(f"端口：{operation_target}, 动作：{operation_type}, port:{port}")
            # 串口接收一个字符串
            receive_data = b''
            byte_data = convert_data(data_dict.get(operation_target).get(operation_type))

            # 串口发送一个字符串
            data_len = uart.write(byte_data)
            # logger.info("send len: ", data_len)
            for i in range(data_len):
                receive_data += uart.read()
            if receive_data == byte_data:
                pass
            else:
                logger.info("指令发送失败")
    except SerialException as e1:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/new_relay_helper.py")
        logger.info("指令发送成功")
    except Exception as result:
        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/utils/new_relay_helper.py")
        logger.info("******error******：", result)
    finally:
        # 关闭串口
        uart.close()


def jy_dam0800_check_and_repair():
    """
    检测并修复继电器的异常状态
    """
    expected_status = {"COM1": 0, "COM2": 0, "COM3": 1, "COM4": 0, "COM5": 0, "COM6": 0, "COM7": 0, "COM8": 1}
    real_status = jy_dam0800_operation("query")
    for key in real_status:
        if real_status[key] != expected_status[key]:
            action = "open" if expected_status[key] == 1 else "close"
            jy_dam0800_operation(action, key)
            if key == "COM1":
                logger.warning("检测到BGM下电，重新上电....")
                time.sleep(30)
            elif key == "COM2":
                logger.warning("检测到TCAM下电，重新上电....")
                time.sleep(180)
            else:
                logger.warning(f"检测到{key}异常，修复中....")
                time.sleep(10)
        # else:
        #     logger.info(f"{key} 当前状态检测正常！")
def jy_dam0800_check_and_repair_new(domain):
    """
    依赖域控检测并修复继电器的异常状态
    """
    expected_status = {"COM1": 0, "COM2": 0, "COM3": 1, "COM4": 0, "COM5": 0, "COM6": 0, "COM7": 0, "COM8": 1}
    real_status = jy_dam0800_operation("query")
    for key in real_status:
        if (domain.single_tcam or domain.bgm_cdc_acu) and key in ("COM1", "COM3"):
            continue
        elif domain.single_bgm and key in ("COM2", "COM8"):
            continue
        if real_status[key] != expected_status[key]:
            action = "open" if expected_status[key] == 1 else "close"
            jy_dam0800_operation(action, key)
            if key == "COM1":
                logger.warning("检测到BGM下电，重新上电....")
                time.sleep(30)
            elif key == "COM2":
                logger.warning("检测到TCAM下电，重新上电....")
                time.sleep(180)
            else:
                logger.warning(f"检测到{key}异常，修复中....")
                time.sleep(10)
