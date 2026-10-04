# -*- coding: utf-8 -*-
"""
@File        : test_tpms.py
@Author      : jiabin.zhu@jiduatuo.com
@Time        : 2022/11/15 18:00 PM
@Description : description about this file
@Examples    : example of how to use it
"""
import math
import threading
import time
from time import sleep
from typing import List
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding, logger
from xat_ecu.legacy.sdk.digital_key.digital_key_class import print_msg_info


def crc8(datas: List[int]):
    """
    计算数据的CRC8校验码，
    :param datas:
    :return:
    """
    length = len(datas)
    crc = 0xAA
    for i in range(length):
        crc = (crc ^ datas[i]) & 0xFF  # 其余的均将上次的CRC8结果与本次数据异或
        poly = 0x07  # 多项式x^8 + x^2 + x^1 + 1，即0x107，（根据原理）省略了最高位1而得0x07
        for _ in range(8):
            if ((crc & 0x80) >> 7) == 1:  # 判断最高位是否为1，如果是需要异或，否则仅左移
                crc = (crc << 1) ^ poly
            else:
                crc = (crc << 1)
        crc = crc & 0xFF  # 再计算CRC8
    return crc & 0xFF


class TyreSensor:
    def __init__(self, tire_id: list):
        self.tire_id = tire_id
        self.pressure = 260  # 实际kpa, hex值 = pressure/1.373
        self.calculated_pressure = math.ceil(self.pressure / 1.373) * 1.373  # BGM计算后的胎压
        self.temp = 52  # 实际℃, hex值 = temp + 50
        self.acc = 36  # hex即加速度
        self.factory = 0x02  # 实际值，造低电量故障0x12
        self.function = 0x85  # 正常用0x85即可
        self.send_rf = False
        self.cycle_time = 3
        self.counter_per_pkg = 1


class Tpms:
    def __init__(self, ipdu, id1='11111111', id2='02628643', id3='026284F4', id4='22222222'):
        self.ipdu = ipdu
        self.ipdu.preheat_msg("connectivitycanfd", "TcamConnectivityFr36")  # 0xA
        self.ipdu.preheat_msg("connectivitycanfd", "TcamConnectivityFr37")  # 0xB
        sleep(2)
        self.running = True
        self.rolling_counter = 0
        self.sensor1 = TyreSensor(DataTypeHanding.hexstr_to_inlist(id1))  # 左前
        self.sensor2 = TyreSensor(DataTypeHanding.hexstr_to_inlist(id2))  # 右前
        self.sensor3 = TyreSensor(DataTypeHanding.hexstr_to_inlist(id3))  # 右后
        self.sensor4 = TyreSensor(DataTypeHanding.hexstr_to_inlist(id4))  # 左后
        for index in range(1, 5):
            threading.Thread(target=self.send_rf_data, args=(index,), daemon=True).start()
            sleep(.5)
        self.ipdu.recv_pdu_thread_start('connectivitycanfd', 0x100, self._rf_control)

    def _rf_control(self, msg):
        """
        监控BGM发送的0x100报文，来控制0xA和0xB报文的发送
        :param msg: (msg_id, timestamp(报文时间戳), msg_length, msg_data(intlist类型的pdu数据))
        :return:
        """
        if msg[0] != 0x100:
            return
        print_msg_info(msg)
        try:
            if msg[3][0] not in [0x5, 0x14, 0xC]:  # 测试框架异常时会出现
                return
        except Exception as e:
            return
        # if msg[3][0] != 0x5:
        #     self.sensor1.send_rf = True
        #     self.sensor2.send_rf = True
        #     self.sensor3.send_rf = True
        #     self.sensor4.send_rf = True
        # else:
        #     self.sensor1.send_rf = False
        #     self.sensor2.send_rf = False
        #     self.sensor3.send_rf = False
        #     self.sensor4.send_rf = False

    def init_sensor_info(self):
        """恢复胎压传感器状态，在每个用例执行前调用"""
        self.sensor1 = TyreSensor(self.sensor1.tire_id)
        self.sensor2 = TyreSensor(self.sensor2.tire_id)
        self.sensor3 = TyreSensor(self.sensor3.tire_id)
        self.sensor4 = TyreSensor(self.sensor4.tire_id)

    def set_pressure(self, tyre_id, pressure):
        """设置胎压，1:左前，2右前，3:右后，4：左后"""
        logger.info(f"设置tyre{tyre_id}={pressure}kpa")
        calculated_pressure = math.ceil(pressure / 1.373) * 1.373
        if tyre_id == 1:
            self.sensor1.pressure = pressure
            self.sensor1.calculated_pressure = calculated_pressure
        elif tyre_id == 2:
            self.sensor2.pressure = pressure
            self.sensor2.calculated_pressure = calculated_pressure
        elif tyre_id == 3:
            self.sensor3.pressure = pressure
            self.sensor3.calculated_pressure = calculated_pressure
        elif tyre_id == 4:
            self.sensor4.pressure = pressure
            self.sensor4.calculated_pressure = calculated_pressure
        print(self.sensor1.pressure, self.sensor2.pressure, self.sensor3.pressure, self.sensor4.pressure)

    def set_factory(self, tyre_id, factory):
        '''设置传感器电压，1:左前，2右前，3:右后，4：左后'''
        logger.info(f"设置tyre{tyre_id}={factory}电压")
        if tyre_id == 1:
            self.sensor1.factory = factory
        elif tyre_id == 2:
            self.sensor2.factory = factory
        elif tyre_id == 3:
            self.sensor3.factory = factory
        elif tyre_id == 4:
            self.sensor4.factory = factory
        print(self.sensor1.factory, self.sensor2.factory, self.sensor3.factory, self.sensor4.factory)

    def set_temperature(self, tyre_id, temperature):
        """设置胎温，1:左前，2右前，3:右后，4：左后"""
        logger.info(f"设置tyre{tyre_id}={temperature}摄氏度")
        if tyre_id == 1:
            self.sensor1.temp = temperature
        elif tyre_id == 2:
            self.sensor2.temp = temperature
        elif tyre_id == 3:
            self.sensor3.temp = temperature
        elif tyre_id == 4:
            self.sensor4.temp = temperature
        print(self.sensor1.temp, self.sensor2.temp, self.sensor3.temp, self.sensor4.temp)

    def tpms_id(self) -> list:
        """返回四个胎压id，用于写did 0x281F"""
        return self.sensor1.tire_id + self.sensor2.tire_id + self.sensor3.tire_id + self.sensor4.tire_id

    def stop(self):
        """结束TPMS发送，子线程退出"""
        self.running = False

    def control_send_rf(self, sts):
        """
        控制胎压数据的发送
        :param sts: True/False
        :return:
        """
        self.sensor1.send_rf = sts
        self.sensor2.send_rf = sts
        self.sensor3.send_rf = sts
        self.sensor4.send_rf = sts

    def send_rf_data(self, index: [1, 2, 3, 4]):
        """
        发送胎压数据
        :param index: 1：左前；2：右前；3：右后；4左后
        :return:
        """
        st = time.time()
        while self.running:
            sensor = [self.sensor1, self.sensor2, self.sensor3, self.sensor4][index - 1]
            while time.time() - st < sensor.cycle_time:
                time.sleep(0.1)
            if sensor.send_rf:
                for _ in range(sensor.counter_per_pkg):
                    rf_data = sensor.tire_id + [math.ceil(sensor.pressure / 1.373), int(sensor.temp + 50),
                                                sensor.acc, sensor.factory, sensor.function]
                    self.ipdu.send_pdu("connectivitycanfd", 0xA,
                                       rf_data + [crc8(rf_data), 0x5E, self.rolling_counter])
                    sleep(0.005)
                    self.ipdu.send_pdu("connectivitycanfd", 0xB,
                                       [0x00, 0x35, 0x7E, self.rolling_counter, 0x00, 0x00, 0x00, 0x00])
                    self.rolling_counter = (self.rolling_counter + 1) & 0xFF
                    sleep(0.12)
            st = time.time()


if __name__ == '__main__':
    tpms1 = Tpms(1)
    tpms1.set_pressure(3, 20)
    print(tpms1.sensor3.pressure)
