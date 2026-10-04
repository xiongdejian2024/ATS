#!/usr/bin/python3
import time
import serial
from xat_ecu.legacy.common.logger import logger


class PowerRemoteController(object):

    def __init__(self, channel, baudrate=9600) -> None:
        self.handler = serial.Serial(channel, baudrate)
        # 设置远程模式
        self.set_remote_mode()
        # 初始化
        self.initialize()
        # 打开输出模式
        self.set_output_on()

    def __handle_data(self, data) -> str:
        try:
            self.handler.flushInput()
            self.handler.write(data)
            time.sleep(1)
            data = self.handler.read(self.handler.inWaiting())
            data = data.decode('utf-8', 'ignore').strip()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/program_controll_power_supply.py")
            logger.error("程控电源异常：", str(e))
            self.close()
            data = ''

        return data

    # 初始化设备,清除寄存器
    def initialize(self):
        '''
        初始化
        :return:
        '''
        cmd_data = b'*CLS\r\n'
        self.__handle_data(cmd_data)
        time.sleep(1)
        logger.info(f"电源初始化")


    def set_vol(self, vol, **kwargs):
        '''
        设置电压
        :param vol: 电压值 根据型号不同设置的最大电压不一样，超过最大电压则会异常
        :param kwargs:
        :return:
        '''

        data = f'VOLT {vol}\r\n'
        data = data.encode('utf-8')
        self.__handle_data(data)
        logger.info(f"设置的电压为：{vol}")

    def get_vol(self, **kwargs):
        '''
        获取电压
        :param kwargs:
        :return:
        '''
        cmd_data = f'MEASure:VOLTage?\r\n'
        cmd_data = cmd_data.encode('utf-8')
        vol = self.__handle_data(cmd_data)
        logger.info(f"获取的电压为：{vol}")
        if vol:
            vol = float(vol)
        return vol

    def set_current(self, current, **kwargs):
        '''
         设置电压
        :param current: 电流值 根据型号不同设置的最大电流不一样，超过最大电流则会异常
        :param kwargs:
        :return:
        '''
        data = f'CURR {current}\r\n'
        data = data.encode('utf-8')
        self.__handle_data(data)
        logger.info(f"设置电流为：{current}")

    def get_current(self, **kwargs):
        '''
        获取电压
        :param kwargs:
        :return:
        '''
        cmd_data = f'MEASure:CURRent?\r\n'
        cmd_data = cmd_data.encode('utf-8')
        current = self.__handle_data(cmd_data)
        logger.info(f"获取的电流为：{current}")
        if current:
            current = float(current)
        return current

    def get_power(self, **kwargs):
        '''
        获取功率
        :param kwargs:
        :return:
        '''
        cmd_data = f'MEASure:POWer?\r\n'
        cmd_data = cmd_data.encode('utf-8')
        power = self.__handle_data(cmd_data)
        logger.info(f"获取的功率为：{power}")
        if power:
            power = float(power)
        return power

    def set_output_on(self, **kwargs):
        '''
        打开输出
        :param kwargs:
        :return:
        '''
        data = f'OUTPut ON\r\n'
        data = data.encode('utf-8')
        self.__handle_data(data)
        logger.info(f"打开输出")

    def set_output_off(self, **kwargs):
        '''
        关闭输出
        :param kwargs:
        :return:
        '''
        data = f'OUTPut OFF\r\n'
        data = data.encode('utf-8')
        self.__handle_data(data)
        logger.info(f"关闭输出")

    def set_remote_mode(self, **kwargs):
        '''
        设置为远程模式
        :param kwargs:
        :return:
        '''
        cmd_data = b'SYSTem:REM\r\n'
        self.__handle_data(cmd_data)
        logger.info(f"设置为远程模式")

    def set_local_mode(self, **kwargs):
        '''
        设置为本地模式
        :param kwargs:
        :return:
        '''
        cmd_data = b'SYSTem:LOCal\r\n'
        self.__handle_data(cmd_data)
        logger.info(f"设置为本地模式")

    def get_status(self, **kwargs):
        '''
        获取电源模式
        :param kwargs:
        :return:
        '''
        data = b'OUTPut?\r\n'
        res = self.__handle_data(data)
        logger.info(f"获取电源状态为:{res}")
        return res

    def close(self):
        '''
        关闭串口
        :return:
        '''
        if self.handler:
            self.handler.close()
            self.handler = None
        logger.info(f"关闭串口")


if __name__ == "__main__":
    # 接口文档 路径
    # https://wiki.jiduauto.com/pages/viewpage.action?pageId=423483836

    # linux 系统实例化
    # power_controller = PowerRemoteController("/dev/ttyUSB1", 9600)
    # windows 系统实例化
    power_controller = PowerRemoteController("com3", 9600)
    # 设置电压为12 v
    power_controller.set_vol(11)
    # 设置电流为2.02A
    power_controller.set_current(4)
    # 获取电压
    vol = power_controller.get_vol()
    # 获取电流
    curr = power_controller.get_current()
    # 获取功率
    power = power_controller.get_power()
    # 关闭串口
    power_controller.close()
