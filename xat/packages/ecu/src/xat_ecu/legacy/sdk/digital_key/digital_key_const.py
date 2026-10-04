#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :digital_key_const.py
@Time         :2022/11/17 16:05:05
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
from enum import Enum, auto
from typing import Union

# BNCM_KEY = bytes([0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16,
#                   0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F])
BNCM_KEY = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
BNCM_IV = bytes([0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27,
                 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F])

key_id0 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
key_id1 = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F]
key_id2 = [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F]
key_id3 = [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x2F]
key_id4 = [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x3F]
key_id5 = [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x4F]
key_id6 = [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x5F]


door_desc = {0x1: '左前门', 0x2: '右前门', 0x3: '左后门', 0x4: '右后门', 0x5: "尾门"}

cenlock_sts_desc = {0x0: 'LockSts3_LockUndefd', 0x1: 'LockSt3_LockUnlckd',
                    0x2: 'LockSt3_LockTrUnlckd', 0x3: "LockSt3_LockLockd"}

cenlock_sts_trigsrc_desc = {0x0: 'LockTrigSrc2_NoTrigSrc', 0x1: 'LockTrigSrc2_KeyRem',
                            0x2: 'LockTrigSrc2_Keyls', 0x3: "LockTrigSrc2_IntrSwt",
                            0x4: 'LockTrigSrc2_SpdAut', 0x5: "LockTrigSrc2_TmrAut",
                            0x6: 'LockTrigSrc2_Slam', 0x7: "LockTrigSrc2_Telm",
                            0x8: 'LockTrigSrc2_Crash', 0x9: "LockTrigSrc2_Apprch",
                            0xA: 'LockTrigSrc2_OutsOth', 0xB: "LockTrigSrc2_InsOth",
                            0xC: 'Locktrigsrc2_NFC'
                            }

door_lock_cmd_desc = {0x0: 'Idle Command', 0x1: 'Unlock door',
                      0x2: 'Lock door', 0x3: "Double lock door",
                      0x4: "Crash Unlock door", 0x8: "Crash Unlock door",
                      0xC: "Crash Unlock door", 0xD: "Crash Unlock door",
                      0xE: "Crash Unlock door"}

door_opener_cmd_desc = {0x0: 'DoorOpenerIdle', 0x1: 'DoorOpenerOpen',
                        0x2: 'DoorOpenerCls', 0x3: "DoorOpenerIStop",
                        0x4: "DoorOpenerIOpenMinang"}

door_opener_trigsrc_desc = {0x0: 'NoTrigSrc', 0x1: 'KeyRem',
                            0x2: 'HMI', 0x3: 'Telm', 0x4: 'OutdSwt', 0x5: 'InsdSwt'}

tr_opener_trigsrc_desc = {0x0: 'TrNoTrigSrc', 0x1: 'TrKeyRem', 0x2: 'TrSwtIntr', 0x3: 'TrByFootOper', 0x4: 'TrByFootOper', 0x5: 'TrShutFarc',
                          0x6: 'TrHmi', 0x7: 'TrByAppch'}

usage_mode_desc = {0x0: 'ABANDONED', 0x1: 'INACTIVE', 0x2: 'CONVENIENCE', 0xB: 'ACTIVE', 0xD: 'DRIVING'}

car_mode_desc = {0x0: 'NORMAL', 0x1: 'TRANSPORT', 0x2: 'FACTORY', 0x3: 'CRASH', 0x5: 'DYNO'}


class Location(Enum):
    """寻钥匙区域"""
    Idle = 0
    ALL = auto()
    AllExt = auto()
    DrvrExt = auto()
    PassExt = auto()
    TrExt = auto()
    AllInt = auto()
    DrvrInt = auto()
    PassInt = auto()
    ResvInt = auto()
    ResvIntSimple = auto()


class Trigger(Enum):
    """寻钥匙触发源"""
    Idle = 0
    VMM = auto()
    Locking = auto()
    KeyRmn = auto()
    KeyWrn = auto()
    DigKeyMgr = auto()
    Service = auto()


class KeyType(Enum):
    """钥匙类型"""
    NoKeyConnected = 0
    NFC_Card = auto()
    BLE_Key = auto()
    BLE_UWB_KeyFob = auto()
    Temp_BLE_Key = auto()
    ICCE_BLE_Key = auto()
    ICCE_NFC_Key = auto()
    CCC_NFC_BLE_UWB_Key = auto()
    CCC_NFC_Key = auto()
    CCC_NFC_BLE_Key = auto()


class InternalExternalStatus(Enum):
    """钥匙所在区域"""
    SearchSts_Idle = 1
    ExternalSearchSts_FrntFound = auto()
    ExternalSearchSts_LeftFnd = auto()
    ExternalSearchSts_RightFnd = auto()
    ExternalSearchSts_RearFnd = auto()
    ExternalSearchSts_Found = auto()
    Reserved = auto()
    InternalSearchSts_Found = auto() # 8
    SearchSts_NotFound = auto()
    ExternalSearchSts_LeftFnd_RearFnd = auto()
    ExternalSearchSts_RightFnd_RearFnd = auto()


class KeyInfo:
    def __init__(self, key_type: Union[KeyType, int], key_id: list, key_status: Union[InternalExternalStatus, int]) -> None:
        self.keyType = key_type if isinstance(key_type, int) else key_type.value
        self.keyID = key_id
        self.key_status = key_status if isinstance(key_status, int) else key_status.value

    def format_key_info(self):
        """将该钥匙信息格式化为列表形式返回"""
        return [self.keyType] + self.keyID + [self.key_status]
