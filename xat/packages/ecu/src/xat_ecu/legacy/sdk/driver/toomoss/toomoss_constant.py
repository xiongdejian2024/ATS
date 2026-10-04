# -*- coding: utf-8 -*-
"""
@File        : toomoss_constant.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022-12-03 09:06
@Description : 
@Examples    :
"""

is_scaned_toomoss_devices = [None]
opened_toomoss_devices = []

class CANConfig_CONSTANT:
    class UTA05XX:
        bt_500k = {"CAN_BRP_CFG3": 1, "CAN_BS1_CFG1": 59, "CAN_BS2_CFG2": 20, "CAN_SJW": 2}
        nbt_500k = {"NBT_BRP": 1, "NBT_SEG1": 59, "NBT_SEG2": 20, "NBT_SJW": 2}
        dbt_2m = {"DBT_BRP": 1, "DBT_SEG1": 14, "DBT_SEG2": 5, "DBT_SJW": 2}

