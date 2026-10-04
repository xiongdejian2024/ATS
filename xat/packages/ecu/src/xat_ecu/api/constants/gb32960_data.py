#!/usr/bin/env python
# -*- coding: utf-8 -*-
# GB32960默认数据

gb32960_data = {
    'VehStatus': {
            "InfoTyp": 1, # 'VEH_STATUS',
            'VehSts': 2, # 'POWER_ON'
            'ChrgnStsInfo': 3, # 'UNCHARGED'
            'PrpnMode': 1, # 'ELECTRIC'
            'VehSpeed': 0, # range(min=0, max=2200)
            'AccumMilg': 3450, # range(min=0, max=9999999)
            'HvBattSocToltalU': 480, # range(min=0, max=10000)
            'HvBattSocToltalI': 1025, # range(min=0, max=20000)
            'HvBattSocInfo': 90, # range(min=0, max=100)
            'DcDcSts': 1, # 'WORKING'
            'GearSts': 15, # 00101110
            'InsulationR': 20000, # range(min=0, max=60000)
            'AccPedlTrvlVal': 50, # range(min=0, max=100)
            'BrkPedlStsInfo': 0x02, # range(min=0, max=101)
            },
    'DriveMotorData': {
            'InfoTyp': 2, # 'DRIVE_MOTOR_DATA'
            'DrvMotQnty': 2, # range(min=1, max=253) default 1
            'DrvMotList': [
                        {
                            'DrvMotSeqNr': 1, # range(min=1, max=253), default 1
                            'DrvMotSts': 1, # 'POWER_CONSUMPTION'
                            'DrvMotCtrlrT': 64, # @range(min=0, max=250)
                            'DrvMotSpeed': 2333, # range(min=0, max=65531)
                            "DrvMotTorque": 2013,#range(min=0, max=65531)
                            'DrvMotT': 58, # range(min=0, max=250)
                            'MotCtrlrInpUDc': 468, # range(min=0, max=60000)
                            'MotCtrlrIDc': 39, # range(min=0, max=20000)
                        },
                        {
                            'DrvMotSeqNr': 2, # range(min=1, max=253), default 1
                            'DrvMotSts': 1, # 'POWER_CONSUMPTION'
                            'DrvMotCtrlrT': 64, # @range(min=0, max=250)
                            'DrvMotSpeed': 2333, # range(min=0, max=65531)
                            "DrvMotTorque": 2000,#range(min=0, max=65531)
                            'DrvMotT': 58, # range(min=0, max=250)
                            'MotCtrlrInpUDc': 472, # range(min=0, max=60000)
                            'MotCtrlrIDc': 41, # range(min=0, max=20000)
                        }],

        },
    'VehPositionData': {
            'InfoTyp': 5, # 'VEH_POSITION_DATA'
            'LocationSts': 0, # 00000000, 东经, 北纬, 有效定位
            'Longitude': 39.916527,
            'Latitude': 116.397128
        },
    'ExtremeData': {
            'InfoTyp': 6, # 'EXTREME_DATA'
            'MaxHvBattUSubSysNr': 1,
            'MaxHvBattCellUCod': 39,
            'MaxHvBattCellUVal': 4.02,
            'MinHvBattUSubSysNr': 1,
            'MinHvBattCellUCod': 23,
            'MinHvBattCellUVal': 3.90,

            'MaxHvBattTSubSysNr': 1,
            'MaxHvBattCellTCod': 21, # 最高温度探针序号
            'MaxHvBattCellTVal': 80,
            'MinHvBattTSubSysNr': 1,
            'MinHvBattCellTCod': 31, # 最低温度探针序号
            'MinHvBattCellTVal': 89
        },
    'WarningData': {
            'InfoTyp': 7,  # 'WARNING_DATA'
            'HvCellTDifFltPrm': 0, # NO_FAULT  0~3  /3
            'HvCellTOverFltPrm': 0, # NO_FAULT  0~3 /3
            'HvPackUOverFltPrm': 0, # NO_FAULT  0~3 /3
            'HvPackUUnderFltPrm': 0, # NO_FAULT 0~3 /3
            'HvSocLoFltPrm': 0, # NO_FAULT  0~3 /3
            'HvCellUOverFltPrm': 0, # NO_FAULT  0~3 /3
            'HvCellUUnderFltPrm': 0, # NO_FAULT  0~3 /3
            'HvSocHiFltPrm': 0, # NO_FAULT  0~3 /3
            'HvSocHopFltPrm': 0, # FAULT_LEVELI  0~3 /3
            'HvBattMismatchFltPrm': 0, # NO_FAULT  0~1 /2
            'HvCellUDifFltPrm': 0, # NO_FAULT  0~3 /3
            'HvlsoFltPrm': 0, # NO_FAULT  0~3 /3
            'FltTDcDcPrm': 0, # NO_FAULT  0~1 /1
            'EscWarnIndcnReqPrm': 1, # NO_FAULT 0~3 0/1
            'BrkWarnIndcnReqPrm': 1, # NO_FAULT 0~1 0/3
            'AbsWarnIndcnReqPrm': 1, # NO_FAULT 0~3 0/2
            'BrkSysWarnIndcnReqPrm': 1, # FAULT_LEVELII  0~1 0/2
            'BrkSysWarnIndcnReqSecPrm': 1, # NO_FAULT 0~1 0/2
            'BrkFldLvlPrm': 0,
            'FltElecDcDcPrm': 0, # NO_FAULT 0~1 1/2
            'IemGenericInvrtTAlrmStPrm': 0, # NO_FAULT  0~1 1/2
            'IgmGenericInvrtTAlrmStPrm': 0, # NO_FAULT  0~1 1/2
            'HvilFltPrm': 0, # NO_FAULT  usage mode=driving, HvilFlt=0x01, level 1. usage mode !=driving, HvilFlt=0x01, level 2.
            'IemGenericMotTAlrmStPrm': 0, # NO_FAULT 0~1 1/2
            'IgmGenericMotTAlrmStPrm': 0, # NO_FAULT 0~1 1/2
            'HvPackOverChrgFltPrm': 0 # FAULT_LEVELIII  0~3 /3
        },
    'HVBatteryVoltageData': {
            'InfoTyp': 8, # 'HV_BATTERY_VOLTAGE_DATA'
            'ReChrglEgyStorgSubSysQnty': 1, # range(min=1, max=250)
            'ReChrglEgyStorgSubSysList': [{"ReChrglEgyStorgSubSysSeqNr":1, 'ReChrglEgyStorgU':220, \
                                         'ReChrglEgyStorgI':5, 'BattCellesTotNr':64, \
                                          'BgngCellSeqNrofThisFrm':1, 'TotCellNrofThisFrm':64,
                                          'CellUVal':[4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                                                      4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                                                      4000, 4000, 4000, 4000, 4000, 4000, 3900, 4000,
                                                      4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                                                      4000, 4000, 4000, 4000, 4000, 4000, 4020, 4000,
                                                      4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                                                      4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,
                                                      4000, 4000, 4000, 4000, 4000, 4000, 4000, 4000,]}]
        },
    'HVBatteryTemperatureData': {
            'InfoTyp': 9, # 'HV_BATTERY_TEMPERATURE_DATA'
            'ReChrglEgyStorgSubSysQnty': 1,
            'ReChrglEgyStorgSubSysList': [{"ReChrglEgyStorgSubSysSeqNr":1, 'TotTProbeNr':32, \
                                          "ProbeTVal":[85, 80, 86, 85, 81, 81, 83, 81,
                                                      81, 81, 81, 84, 84, 83, 81, 82,
                                                      85, 86, 86, 83, 89, 83, 82, 81,
                                                      80, 85, 81, 83, 85, 82, 80, 85]}]
        }
}
