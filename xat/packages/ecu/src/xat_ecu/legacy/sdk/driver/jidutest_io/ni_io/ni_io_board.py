# -*- coding: utf-8 -*-
"""
@File        : ni_io_board.py
@Author      : yuandi.fan@jiduauto.com
@Time        : 2022/11/25 15:25
@Update Time :
@Description : Nfc card test case script

"""
import time
from nidaqmx.system import System, Device
from nidaqmx import Task
from xat_ecu.legacy.sdk.driver.jidutest_io.utils.config_parser import IoConfigParser
from xat_ecu.legacy.common.logger import logger
from threading import RLock


class NIIOSystem(object):
    single_lock = RLock()

    def __new__(cls, *args, **kwargs):
        with NIIOSystem.single_lock:
            if not hasattr(NIIOSystem, "_instance"):
                NIIOSystem._instance = object.__new__(cls)
        return NIIOSystem._instance

    def __init__(self, io_config: dict):
        # 保证只调用一次初始化
        if not hasattr(self, "io_task"):
            self.ip_addr = io_config.get('dev', {}).get('ip_addr')
            self.io_signal_dict = io_config.get('signal')
            self.io_task = {}
            self.system = None
            logger.info(f'NI 板卡初始化开始，等待完成,....')
            self._initialize_device()
            self._initialize_task()
            logger.info(f'NI 板卡初始完成！！！')

    def _initialize_device(self):
        self.system = System()

        device_names = self.system.devices.device_names
        logger.info(f'NI 板卡device_names={device_names}')
        if self.system.devices.device_names == []:
            Device.add_network_device(self.ip_addr)

        logger.info(f'NI 板卡device_names={device_names}')
        self.device_name = device_names[0]
        try:
            logger.info(f'NI 板卡 unreserve_network_device')
            self.system.devices[self.device_name].unreserve_network_device()
            logger.info(f'NI 板卡 reserve_network_device')
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/jidutest_io/ni_io/ni_io_board.py")
            logger.warning(f"ni 板卡 unreserve_network_device 失败：{str(e)}")
        self.system.devices[self.device_name].reserve_network_device(True)
        logger.info(f'NI 板卡 initialize_device end')

    def _initialize_task(self):
        for io_signal, signal_config in self.io_signal_dict.items():
            if signal_config.get('type') == 'DO':
                self.io_task[io_signal] = Task(io_signal)
                self.io_task[io_signal].do_channels.add_do_chan(self.device_name + signal_config.get('channel'))
            elif signal_config.get('type') == 'DI':
                self.io_task[io_signal] = Task(io_signal)
                self.io_task[io_signal].di_channels.add_di_chan(self.device_name + signal_config.get('channel'))
            elif signal_config.get('type') == 'AO':
                self.io_task[io_signal] = Task(io_signal)
                self.io_task[io_signal].ao_channels.add_ao_voltage_chan(self.device_name + signal_config.get('channel'))
            elif signal_config.get('type') == 'AI':
                self.io_task[io_signal] = Task(io_signal)
                self.io_task[io_signal].ai_channels.add_ai_voltage_chan(self.device_name + signal_config.get('channel'))
            else:
                logger.warning("SignalType is not supported.")

    @property
    def io_devices(self):
        return self.system.devices.device_names

    @property
    def io_tasks(self):
        return list(self.io_task.keys())

    def self_test_device(self):
        self.system.devices[self.device_name].self_test_device()

    def reset_device(self):
        self.system.devices[self.device_name].reset_device()

    def set_value(self, io_signal: str, value: bool):
        try:
            self.io_task[io_signal].write(value)
        except KeyError:
            logger.warning(f'{io_signal} is not in current io list.')
            return None

    def get_value(self, io_signal: str):
        try:
            return self.io_task[io_signal].read()
        except KeyError:
            logger.warning(f'{io_signal} is not in current io list.')
            return None

    def set_do_level(self, io_signal: str, value):
        '''
        设置输出电平
        @param io_signal:
        @param value:
        @return:
        '''
        if value:
            value = True
        else:
            value = False
        self.set_value(io_signal, value)
        return 1

    def get_di_level(self, io_signal: str):
        '''
        获取 电平信号
        @param io_signal:
        @return:
        '''
        return self.get_value(io_signal)

    def start_task(self, io_signal: str):
        try:
            self.io_task[io_signal].start()
        except KeyError:
            logger.warning(f'{io_signal} is not in current io list.')

    def stop_task(self, io_signal: str):
        try:
            self.io_task[io_signal].stop()
        except KeyError:
            logger.warning(f'{io_signal} is not in current io list.')

    def remove_task(self, io_signal: str):
        try:
            self.io_task[io_signal].close()
            del self.io_task[io_signal]
        except KeyError:
            logger.warning(f'{io_signal} is not in current io list.')

    def close(self):
        if hasattr(self, "io_task"):
            if self.io_task:
                logger.info(f'close NI 板卡')
                for task in self.io_task.values():
                    task.stop()
                    task.close()
                self.io_task.clear()
                del self.io_task
                self.reset_device()
                self.system.devices[self.device_name].unreserve_network_device()
            else:
                logger.info(f'NI 板卡 已经关闭')
            # 删除这个属性


