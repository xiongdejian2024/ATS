from threading import Thread
import time
import socket
import json

DEFAULT_PORT = 16789
BUFFER_SIZE = 1024 * 1000
MESSAGE_LENGTH_BYTES_FMT = '%08x'
MESSAGE_LENGTH_BYTES = 4


def method_GetSuspFailrStatus_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetSuspFailrStatus{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetBrkFldLvlWarnMsgStatus_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetBrkFldLvlWarnMsgStatus{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_getBrkSysWarnIndicateReqSts_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"getBrkSysWarnIndicateReqSts{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_BrkSysWarnMsgDisplayReqSts_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"BrkSysWarnMsgDisplayReqSts{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_getABSActInfo_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"getABSActInfo{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_getABSFailSts_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"getABSFailSts{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_getABSWarnIndicateReqSts_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"getABSWarnIndicateReqSts{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_getDisplayReqSts_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"getDisplayReqSts{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_getIndicatorLightReqSts_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"getIndicatorLightReqSts{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_getWarnChimeReqSts_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"getWarnChimeReqSts{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_getBrkRelsWarnReqSts_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"getBrkRelsWarnReqSts{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_getHdcWorkSts_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"getHdcWorkSts{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetAutoHoldFunctionAvailable_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetAutoHoldFunctionAvailable{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_SetEscSportMode_request(conn, param=[{'id': 0}, {'isOpen': False}], is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"SetEscSportMode{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_getAvhDisplayReqSts_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"getAvhDisplayReqSts{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetEscSportModeStatus_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetEscSportModeStatus{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_getESCWarnIndicateReqSts_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"getESCWarnIndicateReqSts{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_getESCOffIndicateLightSts_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"getESCOffIndicateLightSts{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_getVehReadySts_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"getVehReadySts{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetAccrPedalPosRate_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetAccrPedalPosRate{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetBrakePedlPsdStatus_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetBrakePedlPsdStatus{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_Lock_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"Lock{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_Unlock_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"Unlock{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetLockStatus_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetLockStatus{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetDisplaySpeed_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetDisplaySpeed{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetSpeed_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetSpeed{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_SetTorqueMode_request(conn, param=[{'mode': 0}], is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"SetTorqueMode{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetTorqueMode_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetTorqueMode{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_SetSuspensionLevel_request(conn, param=[{'level': 0}], is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"SetSuspensionLevel{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetSuspensionLevel_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetSuspensionLevel{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_SetAutoHold_request(conn, param=[{'on': False}], is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"SetAutoHold{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetAutoHold_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetAutoHold{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetHDCFunctionAvailable_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetHDCFunctionAvailable{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_SetHDC_request(conn, param=[{'on': False}], is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"SetHDC{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetHDCOn_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetHDCOn{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_SetTowMode_request(conn, param=[{'on': False}], is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"SetTowMode{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_SetCoastEnergyRegenerateMode_request(conn, param=[{'on': False}], is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"SetCoastEnergyRegenerateMode{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_SetCreepMode_request(conn, param=[{'on': False}], is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"SetCreepMode{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_SetESC_request(conn, param=[{'on': False}], is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"SetESC{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetESC_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetESC{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetEPBOperationStatus_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetEPBOperationStatus{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_EPBOperation_request(conn, param=[{'operate': 0}], is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"EPBOperation{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_SetGear_request(conn, param=[{'gear': 0}], is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"SetGear{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetGear_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetGear{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetGearFault_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetGearFault{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetWheelSpeed_request(conn, param=[{'wheels': ['1']}], is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetWheelSpeed{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetWheelImpluseCounter_request(conn, param=[{'wheels': ['1']}], is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetWheelImpluseCounter{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetVehicleMotionState_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetVehicleMotionState{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetSteerErrorReqStatus_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetSteerErrorReqStatus{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetESCWorkStatus_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetESCWorkStatus{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetTraveledDistance_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetTraveledDistance{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetGearShiftParkStatus_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetGearShiftParkStatus{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_GetSportModeAvailableStatus_request(conn, param={}, is_async=False):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    req = {
        "action": "request",
        "function": f"GetSportModeAvailableStatus{is_async and 'Async' or ''}",
        "args": json.dumps(args)
    }
    print("执行方法请求：{}".format(req))
    conn.sendall(bytes(json.dumps(req), encoding='utf-8'))


def method_all_request(conn):
    method_GetSuspFailrStatus_request(conn, {})
    time.sleep(1)
    method_GetBrkFldLvlWarnMsgStatus_request(conn, {})
    time.sleep(1)
    method_getBrkSysWarnIndicateReqSts_request(conn, {})
    time.sleep(1)
    method_BrkSysWarnMsgDisplayReqSts_request(conn, {})
    time.sleep(1)
    method_getABSActInfo_request(conn, {})
    time.sleep(1)
    method_getABSFailSts_request(conn, {})
    time.sleep(1)
    method_getABSWarnIndicateReqSts_request(conn, {})
    time.sleep(1)
    method_getDisplayReqSts_request(conn, {})
    time.sleep(1)
    method_getIndicatorLightReqSts_request(conn, {})
    time.sleep(1)
    method_getWarnChimeReqSts_request(conn, {})
    time.sleep(1)
    method_getBrkRelsWarnReqSts_request(conn, {})
    time.sleep(1)
    method_getHdcWorkSts_request(conn, {})
    time.sleep(1)
    method_GetAutoHoldFunctionAvailable_request(conn, {})
    time.sleep(1)
    method_SetEscSportMode_request(conn, [{'id': 0}, {'isOpen': False}])
    time.sleep(1)
    method_getAvhDisplayReqSts_request(conn, {})
    time.sleep(1)
    method_GetEscSportModeStatus_request(conn, {})
    time.sleep(1)
    method_getESCWarnIndicateReqSts_request(conn, {})
    time.sleep(1)
    method_getESCOffIndicateLightSts_request(conn, {})
    time.sleep(1)
    method_getVehReadySts_request(conn, {})
    time.sleep(1)
    method_GetAccrPedalPosRate_request(conn, {})
    time.sleep(1)
    method_GetBrakePedlPsdStatus_request(conn, {})
    time.sleep(1)
    method_Lock_request(conn, {})
    time.sleep(1)
    method_Unlock_request(conn, {})
    time.sleep(1)
    method_GetLockStatus_request(conn, {})
    time.sleep(1)
    method_GetDisplaySpeed_request(conn, {})
    time.sleep(1)
    method_GetSpeed_request(conn, {})
    time.sleep(1)
    method_SetTorqueMode_request(conn, [{'mode': 0}])
    time.sleep(1)
    method_GetTorqueMode_request(conn, {})
    time.sleep(1)
    method_SetSuspensionLevel_request(conn, [{'level': 0}])
    time.sleep(1)
    method_GetSuspensionLevel_request(conn, {})
    time.sleep(1)
    method_SetAutoHold_request(conn, [{'on': False}])
    time.sleep(1)
    method_GetAutoHold_request(conn, {})
    time.sleep(1)
    method_GetHDCFunctionAvailable_request(conn, {})
    time.sleep(1)
    method_SetHDC_request(conn, [{'on': False}])
    time.sleep(1)
    method_GetHDCOn_request(conn, {})
    time.sleep(1)
    method_SetTowMode_request(conn, [{'on': False}])
    time.sleep(1)
    method_SetCoastEnergyRegenerateMode_request(conn, [{'on': False}])
    time.sleep(1)
    method_SetCreepMode_request(conn, [{'on': False}])
    time.sleep(1)
    method_SetESC_request(conn, [{'on': False}])
    time.sleep(1)
    method_GetESC_request(conn, {})
    time.sleep(1)
    method_GetEPBOperationStatus_request(conn, {})
    time.sleep(1)
    method_EPBOperation_request(conn, [{'operate': 0}])
    time.sleep(1)
    method_SetGear_request(conn, [{'gear': 0}])
    time.sleep(1)
    method_GetGear_request(conn, {})
    time.sleep(1)
    method_GetGearFault_request(conn, {})
    time.sleep(1)
    method_GetWheelSpeed_request(conn, [{'wheels': ['1']}])
    time.sleep(1)
    method_GetWheelImpluseCounter_request(conn, [{'wheels': ['1']}])
    time.sleep(1)
    method_GetVehicleMotionState_request(conn, {})
    time.sleep(1)
    method_GetSteerErrorReqStatus_request(conn, {})
    time.sleep(1)
    method_GetESCWorkStatus_request(conn, {})
    time.sleep(1)
    method_GetTraveledDistance_request(conn, {})
    time.sleep(1)
    method_GetGearShiftParkStatus_request(conn, {})
    time.sleep(1)
    method_GetSportModeAvailableStatus_request(conn, {})
    time.sleep(1)


def send_data_to(conn, data):
    byte_len = MESSAGE_LENGTH_BYTES_FMT % len(json.dumps(data))
    conn.sendall(bytes(byte_len + json.dumps(data), encoding='utf-8'))


def recv_data_from(conn):
    recv_data = b''
    msg_len_bcd = conn.recv(MESSAGE_LENGTH_BYTES * 2)
    msg_len = int(msg_len_bcd.decode('utf-8'), 16)
    while msg_len > len(recv_data):
        data = conn.recv(BUFFER_SIZE)
        recv_data += data
    return recv_data


class ChassisServiceClient:

    def __init__(self):
        self.stop_loop = False
        self.running = False
        self.tcp_socket_list = []

    def stop_handler(self):
        self.running = False
        for tcp_socket in self.tcp_socket_list:
            tcp_socket.close()
        self.tcp_socket_list.clear()

    def start_handler(self, connect_info, handler):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(connect_info)
        thread = Thread(target=handler, args=(conn, ))
        thread.setDaemon(True)
        thread.start()
        return conn

    def send_method_request(self, conn, method_name, args, is_async=False):
        req = {
            "action": "request",
            "function": f"{method_name}{is_async and 'Async' or ''}",
            "args": json.dumps(args)
        }
        conn.sendall(bytes(json.dumps(req), encoding='utf-8'))
        time.sleep(1)

    def method_run_init(self, service_name):
        self.running = True
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect(('127.0.0.1', DEFAULT_PORT))
        req = {
            "action": "request",
            "function": "get_current_service_list",
            "args": None
        }
        send_data_to(tcp_socket, req)
        recv_data = recv_data_from(tcp_socket)
        resp1 = json.loads(recv_data.decode("utf-8"))
        result = json.loads(resp1['result'])
        req = {
            "action": "request",
            "function": "running_service",
            "args": None
        }
        send_data_to(tcp_socket, req)
        recv_data = recv_data_from(tcp_socket)
        resp1 = json.loads(recv_data.decode("utf-8"))
        result = json.loads(resp1['result'])
        req = {
            "action": "request",
            "function": "start_config",
            "args": json.dumps({
                 service_name: {
                     "role": "client",
                     "name": "{}Test".format(service_name)
                  }
            })
        }
        send_data_to(tcp_socket, req)
        recv_data = recv_data_from(tcp_socket)
        resp1 = json.loads(recv_data.decode("utf-8"))
        result = json.loads(resp1['result'])
        tcp_socket.close()
        time.sleep(1)
        window_conn = self.start_handler(
            tuple(result[service_name+'_client']), self.window_handler)
        self.tcp_socket_list.append(window_conn)
        time.sleep(1)
        return window_conn

    def window_handler(self, conn):
        conn.settimeout(60)
        while self.running:
            try:
                recv_data = conn.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    break
                response = json.loads(recv_data.decode("utf-8"))
                print("收到服务端响应：{}".format(response))
            except OSError as e:
                print(e.__repr__())
                print.info("remote end is closed")
                break
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/output/ChassisService_client.py")
                print.info(e.__repr__())
                continue


if __name__ == "__main__":
    client = ChassisServiceClient()
    window_conn = client.method_run_init("ChassisService")
    method_all_request(window_conn)
    time.sleep(10)
    client.stop_handler()
