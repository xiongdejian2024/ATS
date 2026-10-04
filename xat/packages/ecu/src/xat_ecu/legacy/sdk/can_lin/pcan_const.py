# -*- coding: utf-8 -*-
"""
@File        : pcan_const.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021/03/31 3:36 AM
@Description : description about this file
@Examples    : example of how to use it
"""

from enum import Enum, IntEnum


class PcanConst:
    LIN_BUS_NUMS = ["1", "2", "3", "4", "5", "6", "7", "8", "11"]
    CAN_BUS_LIST = ['adas', 'adc1', 'adc2', 'adc3', 'bodycan', 'cdc',
                    'chassis', 'ept', 'nomi', 'info', 'obd', 'pd', 'rf']
    LIN_BUS_LIST = ['lin1', 'lin2', 'lin3', 'lin4', 'lin5', 'lin6', 'lin7', 'lin8', 'lin9', 'lin11']
    BGM_CAN_BUS_LIST = ['adas', 'bodycan', 'bta', 'ept', 'ccu', 'obd', 'chassis2', 'flm', 'pd',  'chassis1', 'info', 'cdc']
    # 'ccu', 'cdc' not in BGM
    BGM_LIN_BUS_LIST = ['rear_seat', 'door', 'rlm', 'ad', 'roof', 'ip', 'front_vent','storage', 'rear_vent', 'footwell', 'front_seat']
    TIMEOUT_MIRROR_HEATING = (15 * 60)
    TIMEOUT_COMFENA = (((4 * 60) + 5) * 60)
    TIMEOUT_GUEST_MODE = 60 + 5
    TIMEOUT_REAR_DEFROST = (15 * 60)  # DSYSL-2563.
    TIMEOUT_TOLERANCE = 3.0  # DSYSL-2563.  Hopefully we pcan ultimately return it to its original 0.02 value.
    TIMEOUT_FOOTWELL_DOORS_OPEN = 600
    TIMEOUT_FOOTWELL_DOORS_CLOSED = 180
    TIMEOUT_DOOR_PUDDLE_LAMP = 600
    TIMEOUT_REAR_GROUND_ILLUMINATION = 600
    TIMEOUT_CABIN_LIGHT_DOOR_CLOSED = 15
    TIMEOUT_CABIN_LIGHT_DOOR_OPENED = 600
    TIMEOUT_SAFE_BOX = 30
    TIMEOUT_KL15_OFF = 2  # EDMS-2166 CGW
    DELAY_DRIVER_PRESENT_TO_PARK_UNOCCUPY = 5
    DELAY_DRIVER_PRESENT_TO_PARK_DOORAJAR_AND_UNOCCUPY = 2
    DELAY_NOWASHER_TO_FRONTWASH = 12
    DELAY_NOWASHER_TO_REARWASH = 12
    DELAY_EXTRAWIPE_FRONT = 4
    DELAY_EXTRAWIPE_REAR = 4
    DELAY_FRNTWIPRINTERSPD_1 = 22
    DELAY_FRNTWIPRINTERSPD_2 = 8
    DELAY_FRNTWIPRINTERSPD_3 = 4
    DELAY_FRNTWIPRINTERSPD_4 = 2
    DELAY_REMANWIPER = 10
    DELAY_DOORHNDLSTS_TRANSISTION = 20  # DSYSL-2287 Changed from 60->20
    BUS_DELAY_NODELAY = 0
    BUS_TIMEOUT = 5
    CAN_LISTENER_SIGNAL_MAX_LOOP_TIME = 60.0
    CAN_LISTENER_EXPECTED_COUNT = 3

    VEHSPD_CORNERING_LIGHTS = 37  # kph. See NEV-FDS-0031-ExteriorLighting, <ID:450350>.
    VEHSPD_CORNERING_LIGHTS_REVERSING = 8  # kph.
    FACTOR_VEHSPD_CONVERSION = 0.05625
    FACTOR_WDWVEHSPD_CONVERSION = 0.05
    FACTOR_LIN_VEHICLESPEED = 0.05
    FACTOR_LGTA_CONVERSION = 0.001
    FACTOR_AMBTEMP = 0.5
    OFFSET_LGTA_CONVERSION = 2
    OFFSET_AMBTEMP = -40
    ANGLE_STEERING_WHEEL_FOR_CORNERING_LIGHTS = 90
    FACTOR_ANGLE_CONVERSION = 0.1

    # Invalid Values
    VEHSPD_MIN_INVALID_VALUE = 361
    VEHSPD_MAX_INVALID_VALUE = 460
    STEERWHLAG_MIN_INVALID_VALUE = 801
    STEERWHLAG_MAX_INVALID_VALUE = 819

    # Network Management
    NM_MSG_REPEATMSG_CYCLE1_MS = 50
    NUM_REPEATMSG_CYCLE1 = 5
    NM_MSG_REPEATMSG_CYCLE2_MS = 640
    NM_MSG_NORMAL_CYCLE_MS = 640
    NM_TIMEOUT_TIMER_MS = 2000
    NM_REPEAT_MSG_TIMER_MS = 3200
    NM_WAIT_BUS_SLEEP_TIMER_MS = 2000
    NM_MAX_ADDITIONAL_WAKEUP_DELAY_MS = 110
    NM_MSG_LENGTH_BYTES = 8

    # BULB_OUTAGE: DSYSL-212
    CGW_BULB_NO_OUTAGE = 0x0
    CGW_BULB_OUTAGE = 0x1

    # Approach Lights
    APPROACH_LIGHTS_TIMEOUT = 30
    APPROACH_LIGHTS_TIMEOUT_BUFFER = 2
    unlocking_options_list = [
        'approach_unlock',
        'remote_unlock'
    ]

    # FOD Misc constants
    VEHICLE_SPEED_0 = 0
    VEHICLE_SPEED_1 = 1
    VEHICLE_SPEED_2 = 2
    VEHICLE_SPEED_2_5 = 2.5
    VEHICLE_SPEED_2_9 = 2.9
    VEHICLE_SPEED_3 = 3
    FOD_ALLOWED_VEHSPD_LIST = [VEHICLE_SPEED_0, VEHICLE_SPEED_1, VEHICLE_SPEED_2, VEHICLE_SPEED_2_5, VEHICLE_SPEED_2_9]
    VEHICLE_SPEED_30 = 30
    BATTERY_LV_MIN = 11
    BATTERY_LV_MAX = 16

    # NVOS CAN & LIN constants
    ALLOWED_PERCENTAGE_MSG_ARRIVAL_TIME_DEVIATION = 10
    NUM_CAN_CHECK_REPETITIONS = 5

    # Added for Ambient Lights: DSYSL_4997
    MAX_NO_OF_ILMS = 14
    ILM_ID_NOT_IN_DBC = 5

    BCM_AES_KEY = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    PEUF_AES_KEY = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    PEUR_AES_KEY = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    KEY_DATA = b'\x01\x00\x00\x00\x00\x00\x00\x00'

    # Vehicle State
    class VehState(Enum):
        PARKED = "parked"
        PARKED_COMFENA_COMFORT_ENABLED = "parked_comfena_comfort_enabled"
        PARKED_COMFENA_COMFORT_NOT_ENABLED = "parked_comfena_comfort_not_enabled"
        DRIVER_PRESENT = "driver_present"
        DRIVING = "driving"
        SW_UPDATE = "sw_update"

    # IMX Service
    class Service(Enum):
        CAN_RELAY = "can-relay"
        NFC_AGENT = 'nfc-agent'
        M4_AGENT = 'm4-agent'
        UDS_STACK = 'uds-stack'
        
    # Vehicle moving direction
    class MovgDir(Enum):
        STANDSTILL = 0
        FORWARD = 1
        BACKWARD = 2
        INVALID = 3

    class Count(IntEnum):
        LE = -2
        LT = -1
        EQ = 0
        GT = 1
        GE = 2
        EQ_W_CONV = 3
        IN_RANGE = 4

    class EcuType(IntEnum):
        DEMO = 0
        CGW = 1
        BGM = 2

    class BusType(Enum):
        CAN = "can"
        LIN = "lin"

    class CarPlatform(Enum):
        ES6 = "es6"
        ES8 = "es8"
        FORCE = "force"

    class Lin2CanCol(Enum):
        EPT_CAN = 7
        BODY_CAN = 12
        CHASSIS_CAN = 17
        ADAS_CAN = 22
        INFO_CAN = 27
        CDC_CAN = 32
        OBD_CAN = 37

    class Can2LinCol(Enum):
        pass