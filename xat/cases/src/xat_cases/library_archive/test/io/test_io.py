# -*- coding: utf-8 -*-
"""
@File        : test_io.py
@Author      : yuandi.fan@jiduauto.com
@Time        : 2022/11/23 14:57
@Update Time :
@Description : 

"""

import sys
import os

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))
sys.path.append(os.path.join(current_path, "../.."))
sys.path.append(os.path.join(current_path, "../../.."))
import time
from xat_ecu.legacy.sdk.driver.jidutest_io.utils.config_parser import IoConfigParser
from xat_ecu.legacy.sdk.driver.jidutest_io.io.io_system import IOSystem
from xat_ecu.legacy.sdk.driver.jidutest_io.constant.io_const import (
    DOOR,
    HOOD,
    TRUNK,
    BRAKE_PEDAL,
    SEAT,
    SWITCH,
)

if __name__ == '__main__':
    # work dir: test/io
    # cmd: python3 test_io.py

    io_config = IoConfigParser('./pyproject.toml')
    io_system = IOSystem(io_config.io_info)
    # io_system.reset_device()
    io_system.set_value('driver_door_ajar', DOOR.CLOSE.value)
    io_system.set_value('passenger_door_ajar', DOOR.CLOSE.value)
    io_system.set_value('left_rear_door_ajar', DOOR.OPEN.value)
    io_system.set_value('right_rear_door_ajar', DOOR.OPEN.value)
    io_system.set_value('hood_ajar_1', HOOD.CLOSE.value)
    io_system.set_value('trunk_ajar', TRUNK.CLOSE.value)
    io_system.set_value('charge_lid_switch', DOOR.CLOSE.value)

    io_system.set_value('hazard_switch', SWITCH.PRESS.value)
    time.sleep(3)
    io_system.set_value('hazard_switch', SWITCH.RELEASE.value)
    io_system.set_value('horn_switch', DOOR.OPEN.value)
    io_system.set_value('driver_occupy_sensor', SEAT.NOT_OCCUPY.value)
    io_system.set_value('brake_pedal_switch', BRAKE_PEDAL.OFF.value)
    # chsml_status = io_system.get_value('chsml')
    # print(chsml_status)
    # time.sleep(10)
    io_system.close()
