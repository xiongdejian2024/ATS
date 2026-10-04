# -*- coding: utf-8 -*-
"""
@File        : io_system.py
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/04/26 15:25
@Update Time :
@Description : 根据配置文件 决定实例化NI板卡还是继电器模拟的板卡

"""

from xat_ecu.legacy.sdk.driver.jidutest_io.ni_io.ni_io_board import *
from xat_ecu.legacy.sdk.driver.jidutest_io.relay_io.relay_board import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.sdk.driver.jidutest_io.constant.io_const import (
    DOOR,
    HOOD,
    TRUNK,
    BRAKE_PEDAL,
    SEAT,
    SWITCH,
    WiperWashing
)
from xat_ecu.legacy.sdk.driver.jidutest_io.usbrealy_io.usbrelay import *


class IOSystem(object):
    def __init__(self, io_config: dict, auto_start=True):
        self.io_config = io_config
        self.ip_addr = self.io_config.get('dev', {}).get('ip_addr')
        self.io_signal_dict = self.io_config.get('signal')
        self.io_task = {}
        self.system = None
        # 默认是 NI 板卡
        if auto_start:
            self.io_obj = self.start_io()
        self.config_data = self.io_config.get('signal')

    def start_io(self):
        logger.info(f"开始初始化板卡，等待初始化完成。。。。需要几秒时间 ")
        try:
            if self.ip_addr is None:
                logger.warning(f"未配置板卡信息，清配置板卡信息！！！")
                self.io_obj = None
            elif self.ip_addr.lower() == "com":
                logger.info(f"使用继电器板卡")
                self.io_obj = RelayIOSystem(self.io_config)
            elif self.ip_addr.lower() == "usbrelay":
                logger.info(f"使用 usbrelay ")
                self.io_obj = USBrelay(self.io_config)
            else:
                logger.info(f"使用NI板卡")
                self.io_obj = NIIOSystem(self.io_config)
            logger.info(f"板卡初始化完成！！！ ")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/jidutest_io/io/io_system.py")
            self.io_obj=None
            logger.error(f"板卡初始化失败：{str(e)},会影响板卡使用")
        return self.io_obj

    def set_pwm(self, io_signal: str, freq: int, duty: int):
        return self.io_obj.set_pwm(io_signal, freq, duty)

    def get_pwm(self, io_signal: str):
        return self.io_obj.get_pwm(io_signal)

    def set_do_level(self, io_signal: str, value):
        '''
        设置 do 输出
        @param io_signal:
        @param value:
        @return:
        '''
        logger.info(f"设为io_signal={io_signal} value={value}")
        return self.io_obj.set_do_level(io_signal, value)

    def get_di_level(self, io_signal: str):
        '''
        采集信号
        @param io_signal:
        @return:
        '''
        value =self.io_obj.get_di_level(io_signal)
        logger.info(f"获取io_signal={io_signal} value={value}")
        return value
    
    def close(self):
        if self.io_obj:
            self.io_obj.close()

    # ----------------------------  Door and Door Switch Status ----------------------------------------
    def drvr_door_open(self, **kwargs):
        '''
        打开左前门   J3-21	左前门状态开关	driver_door_ajar
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "driver_door_ajar")
        value = kwargs.get("value", DOOR.OPEN.value)
        return self.set_do_level(name, value)

    def drvr_door_close(self, **kwargs):
        '''
        关闭左前门  J3-21	左前门状态开关	driver_door_ajar
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "driver_door_ajar")
        value = kwargs.get("value", DOOR.CLOSE.value)
        return self.set_do_level(name, value)

    def pass_door_open(self, **kwargs):
        '''
        打开 J3-08	右前门状态开关	passenger_door_ajar
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "passenger_door_ajar")
        value = kwargs.get("value", DOOR.OPEN.value)
        return self.set_do_level(name, value)

    def pass_door_close(self, **kwargs):
        '''
        关闭  J3-08	右前门状态开关	passenger_door_ajar
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "passenger_door_ajar")
        value = kwargs.get("value", DOOR.CLOSE.value)
        return self.set_do_level(name, value)

    def lere_door_open(self, **kwargs):
        '''
        打开  J3-12	左后门状态开关	left_rear_door_ajar

        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "left_rear_door_ajar")
        value = kwargs.get("value", DOOR.OPEN.value)
        return self.set_do_level(name, value)

    def lere_door_close(self, **kwargs):
        '''
        关闭J3-12	左后门状态开关	left_rear_door_ajar
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "left_rear_door_ajar")
        value = kwargs.get("value", DOOR.CLOSE.value)
        return self.set_do_level(name, value)

    def rire_door_open(self, **kwargs):
        '''
        打开J3-09	右后门状态开关	right_rear_door_ajar
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "right_rear_door_ajar")
        value = kwargs.get("value", DOOR.OPEN.value)
        return self.set_do_level(name, value)

    def rire_door_close(self, **kwargs):
        '''
        关闭 J3-09	右后门状态开关	right_rear_door_ajar
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "right_rear_door_ajar")
        value = kwargs.get("value", DOOR.CLOSE.value)
        return self.set_do_level(name, value)

    def trunk_door_open(self, **kwargs):
        '''
        打开 J3-34	行李箱状态开关	trunk_ajar
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "trunk_ajar")
        value = kwargs.get("value", TRUNK.OPEN.value)
        return self.set_do_level(name, value)

    def trunk_door_close(self, **kwargs):
        '''
        关闭 J3-34	行李箱状态开关	trunk_ajar
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "trunk_ajar")
        value = kwargs.get("value", TRUNK.CLOSE.value)
        return self.set_do_level(name, value)

    def set_four_door_close(self):
        self.drvr_door_close()
        self.pass_door_close()
        self.lere_door_close()
        self.rire_door_close()

    def drvr_door_outswitch_pressed(self, **kwargs):
        '''
        J3-39	左前门把手开关	driver_door_handle
        @return:
        '''
        name = kwargs.get("name", "driver_door_handle")
        value = kwargs.get("value", SWITCH.PRESS.value)
        return self.set_do_level(name, value)

    def drvr_door_outswitch_unpressed(self, **kwargs):
        '''
            J3-39	左前门把手开关	driver_door_handle
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "driver_door_handle")
        value = kwargs.get("value", SWITCH.RELEASE.value)
        return self.set_do_level(name, value)

    def pass_door_outswitch_pressed(self, **kwargs):
        '''
        J3-38	右前门把手开关	passenger_door_handle
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "passenger_door_handle")
        value = kwargs.get("value", SWITCH.PRESS.value)
        return self.set_do_level(name, value)

    def pass_door_outswitch_unpressed(self, **kwargs):
        '''
        J3-38	右前门把手开关	passenger_door_handle
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "passenger_door_handle")
        value = kwargs.get("value", SWITCH.RELEASE.value)
        return self.set_do_level(name, value)

    def lere_door_outswitch_pressed(self, **kwargs):
        '''
        J3-41	左后门把手开关	left_rear_door_handle
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "left_rear_door_handle")
        value = kwargs.get("value", SWITCH.PRESS.value)
        return self.set_do_level(name, value)

    def lere_door_outswitch_unpressed(self, **kwargs):
        '''
        J3-41	左后门把手开关	left_rear_door_handle
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "left_rear_door_handle")
        value = kwargs.get("value", SWITCH.RELEASE.value)
        return self.set_do_level(name, value)

    def rire_door_outswitch_pressed(self, **kwargs):
        '''
        J3-40	右后门把手开关	right_rear_door_handle
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "right_rear_door_handle")
        value = kwargs.get("value", SWITCH.PRESS.value)
        return self.set_do_level(name, value)

    def rire_door_outswitch_unpressed(self, **kwargs):
        '''
        J3-40	右后门把手开关	right_rear_door_handle
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "right_rear_door_handle")
        value = kwargs.get("value", SWITCH.RELEASE.value)
        return self.set_do_level(name, value)

    def trunk_door_outswitch_pressed(self, **kwargs):
        '''
        J3-31	外部尾门解锁开关
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "trunk_unlock_ext_button")
        value = kwargs.get("value", SWITCH.PRESS.value)
        return self.set_do_level(name, value)

    def trunk_door_outswitch_unpressed(self, **kwargs):
        '''
        J3-31	外部尾门解锁开关
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "trunk_unlock_ext_button")
        value = kwargs.get("value", SWITCH.RELEASE.value)
        return self.set_do_level(name, value)

    def driver_seat_present(self, **kwargs):
        '''
        J3-35	驾驶员占位传感器	driver_occupy_sensor
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "driver_occupy_sensor")
        value = kwargs.get("value", SEAT.OCCUPY.value)
        return self.set_do_level(name, value)

    def driver_seat_notpresent(self, **kwargs):
        '''
        J3-35	驾驶员占位传感器	driver_occupy_sensor
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "driver_occupy_sensor")
        value = kwargs.get("value", 0)
        return self.set_do_level(name, SEAT.NOT_OCCUPY.value)

    def brake_down(self, **kwargs):
        '''
        J2-32	刹车踏板开关	brake_pedal_switch
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "brake_pedal_switch")
        value = kwargs.get("value", BRAKE_PEDAL.ON.value)
        return self.set_do_level(name, value)

    def brake_up(self, **kwargs):
        '''
        J2-32	刹车踏板开关	brake_pedal_switch
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "brake_pedal_switch")
        value = kwargs.get("value", BRAKE_PEDAL.OFF.value)
        return self.set_do_level(name, value)

    def bgm_diag_line_up(self, **kwargs):
        '''
        J3-10	诊断激活线	diag_active_switch
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "diag_active_switch")
        value = kwargs.get("value", 1)
        return self.set_do_level(name, value)

    def bgm_diag_line_down(self, **kwargs):
        '''
        J3-10	诊断激活线	diag_active_switch
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "diag_active_switch")
        value = kwargs.get("value", 0)
        return self.set_do_level(name, value)

    def release_door_switch(self):
        self.drvr_door_outswitch_unpressed()
        self.pass_door_outswitch_unpressed()
        self.lere_door_outswitch_unpressed()
        self.rire_door_outswitch_unpressed()

    def init_bgm_HW(self):
        # self.bgm_power_on()
        # self.bgm_diag_line_up()
        self.set_four_door_close()
        self.trunk_door_close()
        self.release_door_switch()
        self.trunk_door_outswitch_unpressed()
        self.driver_seat_notpresent()
        self.brake_up()
    
    def hood_door1_open(self, **kwargs):
        '''
        J3-37	引擎盖状态开关1	hood_ajar_1
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "hood_ajar_1")
        value = kwargs.get("value", HOOD.OPEN.value)
        return self.set_do_level(name, value)

    def hood_door1_close(self, **kwargs):
        '''
        J3-37	引擎盖状态开关1	hood_ajar_1
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "hood_ajar_1")
        value = kwargs.get("value", HOOD.CLOSE.value)
        return self.set_do_level(name, value)

    def wiper_washing_low_open(self, **kwargs):
        """
        雨刮洗涤低液位提醒开
        """
        name = kwargs.get("name", "wiper_washing_switch")
        value = kwargs.get("value", WiperWashing.OPEN.value)
        return self.set_do_level(name, value)

    def wiper_washing_low_close(self, **kwargs):
        """
        雨刮洗涤低液位提醒关
        """
        name = kwargs.get("name", "wiper_washing_switch")
        value = kwargs.get("value", WiperWashing.CLOSE.value)
        return self.set_do_level(name, value)

    def hood_door2_open(self, **kwargs):
        '''
        J3-36	引擎盖状态开关2	hood_ajar_2
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "hood_ajar_2")
        value = kwargs.get("value", HOOD.OPEN.value)
        return self.set_do_level(name, value)

    def hood_door2_close(self, **kwargs):
        '''
        J3-36	引擎盖状态开关2	hood_ajar_2
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "hood_ajar_2")
        value = kwargs.get("value", HOOD.CLOSE.value)
        return self.set_do_level(name, value)
    
  
    def charge_lid_open(self, **kwargs):
        '''
        打开充电口 盖， J3-26
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "charge_lid_switch")
        value = kwargs.get("value", SWITCH.PRESS.value)
        return self.set_do_level(name, value)

    def charge_lid_close(self, **kwargs):
        '''
        打开充电口 盖， J3-26
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "charge_lid_switch")
        value = kwargs.get("value", SWITCH.RELEASE.value)
        return self.set_do_level(name, value)

    def hazard_light_open(self, **kwargs):
        '''
        打开危险灯， J3-07
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "hazard_switch")
        value = kwargs.get("value", SWITCH.PRESS.value)
        return self.set_do_level(name, value)

    def hazard_light_close(self, **kwargs):
        '''
        关闭危险灯， J3-07
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "hazard_switch")
        value = kwargs.get("value", SWITCH.RELEASE.value)
        return self.set_do_level(name, value)

    def horn_switch_open(self, **kwargs):
        '''
        打开喇叭， J3-20
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "horn_switch")
        value = kwargs.get("value", SWITCH.PRESS.value)
        return self.set_do_level(name, value)

    def horn_switch_close(self, **kwargs):
        '''
        关闭喇叭， J3-20
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "horn_switch")
        value = kwargs.get("value", SWITCH.RELEASE.value)
        return self.set_do_level(name, value)

    def chrglid_open(self, **kwargs):
        """
        充电口盖按键开
        """
        name = kwargs.get("name", "chrglid_switch")
        value = kwargs.get("value", SWITCH.PRESS.value)
        return self.set_do_level(name, value)

    def chrglid_close(self, **kwargs):
        """
        充电口盖按键关
        """
        name = kwargs.get("name", "chrglid_switch")
        value = kwargs.get("value", SWITCH.RELEASE.value)
        return self.set_do_level(name, value)
    
    # 采集低电平信号

    def get_and_check_blower_relay_output_level(self, expect_value=0, do_assert=True, **kwargs):
        '''
        校验 鼓风机继电器 输出
        J2-05	鼓风机继电器
        @param expect_value: 0 期望为低电平，1期望不是低电平
        @param do_assert: 为True，获取的值不是电平 则报错
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "blower_relay")
        level = self.get_di_level(name)
        if do_assert and level != expect_value:
            assert 0, f"期望 鼓风机 继电器 {'输出低电平，实际不是'if expect_value==0 else '输出不是低电平，实际是电平' }"
        return level

    def get_and_check_horn_relay_output_level(self, expect_value=0, do_assert=True, **kwargs):
        '''
        校验 喇叭继电器 输出
        J2-08	喇叭继电器
        @param expect_value: 0 期望为低电平，1期望不是低电平
        @param do_assert: 为True，获取的值不是电平 则报错
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "horn_relay")
        level = self.get_di_level(name)
        if do_assert and level != expect_value:
            assert 0, f"期望 喇叭继电器 {'输出低电平，实际不是'if expect_value==0 else '输出不是低电平，实际是电平' }"
        return level

    def get_and_check_crash_relay_output_level(self, expect_value=0, do_assert=True, **kwargs):
        '''
        校验 碰撞继电器 输出
        J2-09	碰撞继电器
        @param expect_value: 0 期望为低电平，1期望不是低电平
        @param do_assert: 为True，获取的值不是电平 则报错
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "crash_relay")
        level = self.get_di_level(name)
        if do_assert and level != expect_value:
            assert 0, f"期望 碰撞继电器 {'输出低电平，实际不是'if expect_value==0 else '输出不是低电平，实际是电平' }"
        return level

    def get_and_check_hcm_relay_output_level(self, expect_value=0, do_assert=True, **kwargs):
        '''
        校验 HCM继电器 输出
        J2-11	HCM继电器
        @param expect_value: 0 期望为低电平，1期望不是低电平
        @param do_assert: 为True，获取的值不是电平 则报错
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "hcm_relay")
        level = self.get_di_level(name)
        if do_assert and level != expect_value:
            assert 0, f"期望 HCM继电器 {'输出低电平，实际不是'if expect_value==0 else '输出不是低电平，实际是电平' }"
        return level

    def get_and_check_rear_defrost_relay_output_level(self, expect_value=0, do_assert=True, **kwargs):
        '''
        校验 后除雾继电器 输出
        J2-20	后除雾继电器
        @param expect_value: 0 期望为低电平，1期望不是低电平
        @param do_assert: 为True，获取的值不是电平 则报错
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "rear_defrost_relay")
        level = self.get_di_level(name)
        if do_assert and level != expect_value:
            assert 0, f"期望 后除雾继电器 {'输出低电平，实际不是' if expect_value == 0 else '输出不是低电平，实际是电平'}"
        return level

    def get_and_check_front_wash_relay_output_level(self, expect_value=0, do_assert=True, **kwargs):
        '''
        校验 前喷水继电器 输出
        J2-23	前喷水继电器
        @param expect_value: 0 期望为低电平，1期望不是低电平
        @param do_assert: 为True，获取的值不是电平 则报错
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "front_wash_relay")
        level = self.get_di_level(name)
        if do_assert and level != expect_value:
            assert 0, f"期望 前喷水继电器 {'输出低电平，实际不是' if expect_value == 0 else '输出不是低电平，实际是电平'}"
        return level

    def get_and_check_rcm_relay_output_level(self, expect_value=0, do_assert=True, **kwargs):
        '''
        校验 RCM继电器 输出
        J2-26	RCM继电器
        @param expect_value: 0 期望为低电平，1期望不是低电平
        @param do_assert: 为True，获取的值不是电平 则报错
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "rcm_relay")
        level = self.get_di_level(name)
        if do_assert and level != expect_value:
            assert 0, f"期望 RCM继电器 {'输出低电平，实际不是' if expect_value == 0 else '输出不是低电平，实际是电平'}"
        return level

    def dtc_relay_ch_switch(self, **kwargs):
        '''
        DTC测试台架继电器程控接口
        @param kwargs:
        @return:
        '''
        name = kwargs.get("name", "dtc_relay0_ch0_switch")
        value = kwargs.get("value", 0)
        return self.set_do_level(name, value)
