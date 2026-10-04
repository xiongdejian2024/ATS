from threading import Thread
import time
import socket
import json

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000
MESSAGE_LENGTH_BYTES_FMT = '%08x'
MESSAGE_LENGTH_BYTES = 4


def method_GetSuspFailrStatus_response(conn, param={'failSts': False}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetSuspFailrStatus",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetBrkFldLvlWarnMsgStatus_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetBrkFldLvlWarnMsgStatus",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_getBrkSysWarnIndicateReqSts_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"getBrkSysWarnIndicateReqSts",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_BrkSysWarnMsgDisplayReqSts_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"BrkSysWarnMsgDisplayReqSts",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_getABSActInfo_response(conn, param={'flActSts': False}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"getABSActInfo",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_getABSFailSts_response(conn, param={'out': False}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"getABSFailSts",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_getABSWarnIndicateReqSts_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"getABSWarnIndicateReqSts",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_getDisplayReqSts_response(conn, param={'highPriSts': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"getDisplayReqSts",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_getIndicatorLightReqSts_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"getIndicatorLightReqSts",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_getWarnChimeReqSts_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"getWarnChimeReqSts",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_getBrkRelsWarnReqSts_response(conn, param={'out': False}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"getBrkRelsWarnReqSts",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_getHdcWorkSts_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"getHdcWorkSts",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetAutoHoldFunctionAvailable_response(conn, param={'out': False}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetAutoHoldFunctionAvailable",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_SetEscSportMode_response(conn, param={'out': 'None'}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"SetEscSportMode",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_getAvhDisplayReqSts_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"getAvhDisplayReqSts",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetEscSportModeStatus_response(conn, param={'out': False}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetEscSportModeStatus",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_getESCWarnIndicateReqSts_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"getESCWarnIndicateReqSts",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_getESCOffIndicateLightSts_response(conn, param={'out': False}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"getESCOffIndicateLightSts",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_getVehReadySts_response(conn, param={'out': False}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"getVehReadySts",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetAccrPedalPosRate_response(conn, param={'rate': 0.0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetAccrPedalPosRate",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetBrakePedlPsdStatus_response(conn, param={'isPressed': False}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetBrakePedlPsdStatus",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_Lock_response(conn, param={'out': 'None'}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"Lock",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_Unlock_response(conn, param={'out': 'None'}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"Unlock",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetLockStatus_response(conn, param={'out': False}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetLockStatus",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetDisplaySpeed_response(conn, param={'speed': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetDisplaySpeed",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetSpeed_response(conn, param={'speed': 0.0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetSpeed",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_SetTorqueMode_response(conn, param={'out': 'None'}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"SetTorqueMode",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetTorqueMode_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetTorqueMode",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_SetSuspensionLevel_response(conn, param={'out': 'None'}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"SetSuspensionLevel",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetSuspensionLevel_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetSuspensionLevel",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_SetAutoHold_response(conn, param={'out': 'None'}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"SetAutoHold",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetAutoHold_response(conn, param={'out': False}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetAutoHold",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetHDCFunctionAvailable_response(conn, param={'out': False}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetHDCFunctionAvailable",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_SetHDC_response(conn, param={'out': 'None'}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"SetHDC",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetHDCOn_response(conn, param={'out': False}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetHDCOn",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_SetTowMode_response(conn, param={'out': 'None'}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"SetTowMode",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_SetCoastEnergyRegenerateMode_response(conn, param={'out': 'None'}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"SetCoastEnergyRegenerateMode",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_SetCreepMode_response(conn, param={'out': 'None'}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"SetCreepMode",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_SetESC_response(conn, param={'out': 'None'}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"SetESC",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetESC_response(conn, param={'out': False}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetESC",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetEPBOperationStatus_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetEPBOperationStatus",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_EPBOperation_response(conn, param={'out': 'None'}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"EPBOperation",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_SetGear_response(conn, param={'out': 'None'}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"SetGear",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetGear_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetGear",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetGearFault_response(conn, param={'out': ['0']}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetGearFault",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetWheelSpeed_response(conn, param={'wheelId': 1}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetWheelSpeed",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetWheelImpluseCounter_response(conn, param={'wheelId': 1}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetWheelImpluseCounter",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetVehicleMotionState_response(conn, param={'sts': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetVehicleMotionState",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetSteerErrorReqStatus_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetSteerErrorReqStatus",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetESCWorkStatus_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetESCWorkStatus",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetTraveledDistance_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetTraveledDistance",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetGearShiftParkStatus_response(conn, param={'parkReq': False}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetGearShiftParkStatus",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def method_GetSportModeAvailableStatus_response(conn, param={'out': 0}):
    if param is None:
        args = ""
    else:
        args = param
    resp = {
        "action": "response",
        "function": f"GetSportModeAvailableStatus",
        "result": json.dumps(args)
    }
    print("方法返回结果：{}".format(json.dumps(resp)))
    conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))


def event_brkSysWarnIndicateReqSts_notify(conn, param=[{'sts': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdatebrkSysWarnIndicateReqStsEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_brkSysWarnMsgDisplayReqSts_notify(conn, param=[{'sts': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdatebrkSysWarnMsgDisplayReqStsEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_absActSts_notify(conn, param=[{'flActSts': False}, {'frActSts': False}, {'rlActSts': False}, {'rrActSts': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateabsActStsEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_absFailSts_notify(conn, param=[{'sts': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateabsFailStsEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_absWarnIndicateReqSts_notify(conn, param=[{'sts': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateabsWarnIndicateReqStsEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_epbWorkSts_notify(conn, param=[{'sts': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateepbWorkStsEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_epbDisplayReqSts_notify(conn, param=[{'highPriSts': 0}, {'lowPriSts': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateepbDisplayReqStsEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_epbIndicatorLightReqSts_notify(conn, param=[{'sts': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateepbIndicatorLightReqStsEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_epbWarnChimeReqSts_notify(conn, param=[{'sts': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateepbWarnChimeReqStsEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_brkRelsWarnReqSts_notify(conn, param=[{'sts': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdatebrkRelsWarnReqStsEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_hdcWorkSts_notify(conn, param=[{'sts': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdatehdcWorkStsEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_AutoHoldFunctionAvailable_notify(conn, param=[{'sts': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateAutoHoldFunctionAvailableEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_avhDisplayReqSts_notify(conn, param=[{'sts': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateavhDisplayReqStsEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_escWarnIndicateReqSts_notify(conn, param=[{'sts': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateescWarnIndicateReqStsEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_escOffIndicateLightSts_notify(conn, param=[{'sts': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateescOffIndicateLightStsEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_vehicleReady_notify(conn, param=[{'sts': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdatevehicleReadyEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_NotifyBrkFldLvlWarnMsgStatus_notify(conn, param=[{'msg': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateNotifyBrkFldLvlWarnMsgStatusEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_NotifyCrpModSts_notify(conn, param=[{'sts': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateNotifyCrpModStsEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_NotifySuspFailrStatus_notify(conn, param=[{'failSts': False}, {'factor': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateNotifySuspFailrStatusEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_NotifyEscSportModeStatus_notify(conn, param=[{'sts': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateNotifyEscSportModeStatusEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_ChassisFault_notify(conn, param=[{'faults': ['0']}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateChassisFaultEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_DisplaySpeedChanged_notify(conn, param=[{'speed': 0}, {'speedUnit': 0}, {'isvalid': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateDisplaySpeedChangedEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_SpeedChanged_notify(conn, param=[{'speed': 0.0}, {'isvalid': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateSpeedChangedEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_TorqueMode_notify(conn, param=[{'mode': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateTorqueModeEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_Gear_notify(conn, param=[{'gear': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateGearEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_GearFault_notify(conn, param=[{'faults': ['0']}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateGearFaultEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_WheelSpeed_notify(conn, param=[{'wheelId': 1}, {'speed': 0.0}, {'isvalid': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateWheelSpeedEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_WheelImpluseCounter_notify(conn, param=[{'wheelId': 1}, {'wheelImpluseCounter': 0}, {'isvalid': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateWheelImpluseCounterEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_VehicleMotionState_notify(conn, param=[{'sts': 0}, {'isVaild': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateVehicleMotionStateEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_SteerErrorReqStatus_notify(conn, param=[{'': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateSteerErrorReqStatusEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_ESCWorkStatus_notify(conn, param=[{'': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateESCWorkStatusEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_EPBOperationStatus_notify(conn, param=[{'': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateEPBOperationStatusEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_HDCFunctionAvailableChanged_notify(conn, param=[{'on': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateHDCFunctionAvailableChangedEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_HDCChanged_notify(conn, param=[{'on': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateHDCChangedEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_ESCChanged_notify(conn, param=[{'on': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateESCChangedEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_AutoHoldChanged_notify(conn, param=[{'on': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateAutoHoldChangedEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_SuspensionLevel_notify(conn, param=[{'level': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateSuspensionLevelEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_TraveledDistance_notify(conn, param=[{'value': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateTraveledDistanceEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_CoastEnergyRegenerateMode_notify(conn, param=[{'on': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateCoastEnergyRegenerateModeEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_CreepMode_notify(conn, param=[{'on': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateCreepModeEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_GearShiftParkStatus_notify(conn, param=[{'parkReq': False}, {'validSts': False}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateGearShiftParkStatusEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_SportModeAvailableStatus_notify(conn, param=[{'state': 0}]):
    if param is None:
        args = ""
    else:
        args = {key: value for pa in param for key, value in pa.items()}
    event = {
        "action": "event",
        "function": f"UpdateSportModeAvailableStatusEvent",
         "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
    print("下发事件通知：{}".format(event))


def event_all_notify(conn):
    event_brkSysWarnIndicateReqSts_notify(conn, args=[{'sts': 0}])
    time.sleep(1)
    event_brkSysWarnMsgDisplayReqSts_notify(conn, args=[{'sts': 0}])
    time.sleep(1)
    event_absActSts_notify(conn, args=[{'flActSts': False}, {'frActSts': False}, {'rlActSts': False}, {'rrActSts': False}])
    time.sleep(1)
    event_absFailSts_notify(conn, args=[{'sts': False}])
    time.sleep(1)
    event_absWarnIndicateReqSts_notify(conn, args=[{'sts': 0}])
    time.sleep(1)
    event_epbWorkSts_notify(conn, args=[{'sts': 0}])
    time.sleep(1)
    event_epbDisplayReqSts_notify(conn, args=[{'highPriSts': 0}, {'lowPriSts': 0}])
    time.sleep(1)
    event_epbIndicatorLightReqSts_notify(conn, args=[{'sts': 0}])
    time.sleep(1)
    event_epbWarnChimeReqSts_notify(conn, args=[{'sts': 0}])
    time.sleep(1)
    event_brkRelsWarnReqSts_notify(conn, args=[{'sts': False}])
    time.sleep(1)
    event_hdcWorkSts_notify(conn, args=[{'sts': 0}])
    time.sleep(1)
    event_AutoHoldFunctionAvailable_notify(conn, args=[{'sts': False}])
    time.sleep(1)
    event_avhDisplayReqSts_notify(conn, args=[{'sts': 0}])
    time.sleep(1)
    event_escWarnIndicateReqSts_notify(conn, args=[{'sts': 0}])
    time.sleep(1)
    event_escOffIndicateLightSts_notify(conn, args=[{'sts': False}])
    time.sleep(1)
    event_vehicleReady_notify(conn, args=[{'sts': False}])
    time.sleep(1)
    event_NotifyBrkFldLvlWarnMsgStatus_notify(conn, args=[{'msg': 0}])
    time.sleep(1)
    event_NotifyCrpModSts_notify(conn, args=[{'sts': False}])
    time.sleep(1)
    event_NotifySuspFailrStatus_notify(conn, args=[{'failSts': False}, {'factor': 0}])
    time.sleep(1)
    event_NotifyEscSportModeStatus_notify(conn, args=[{'sts': False}])
    time.sleep(1)
    event_ChassisFault_notify(conn, args=[{'faults': ['0']}])
    time.sleep(1)
    event_DisplaySpeedChanged_notify(conn, args=[{'speed': 0}, {'speedUnit': 0}, {'isvalid': False}])
    time.sleep(1)
    event_SpeedChanged_notify(conn, args=[{'speed': 0.0}, {'isvalid': False}])
    time.sleep(1)
    event_TorqueMode_notify(conn, args=[{'mode': 0}])
    time.sleep(1)
    event_Gear_notify(conn, args=[{'gear': 0}])
    time.sleep(1)
    event_GearFault_notify(conn, args=[{'faults': ['0']}])
    time.sleep(1)
    event_WheelSpeed_notify(conn, args=[{'wheelId': 1}, {'speed': 0.0}, {'isvalid': False}])
    time.sleep(1)
    event_WheelImpluseCounter_notify(conn, args=[{'wheelId': 1}, {'wheelImpluseCounter': 0}, {'isvalid': False}])
    time.sleep(1)
    event_VehicleMotionState_notify(conn, args=[{'sts': 0}, {'isVaild': False}])
    time.sleep(1)
    event_SteerErrorReqStatus_notify(conn, args=[{'': 0}])
    time.sleep(1)
    event_ESCWorkStatus_notify(conn, args=[{'': 0}])
    time.sleep(1)
    event_EPBOperationStatus_notify(conn, args=[{'': 0}])
    time.sleep(1)
    event_HDCFunctionAvailableChanged_notify(conn, args=[{'on': False}])
    time.sleep(1)
    event_HDCChanged_notify(conn, args=[{'on': False}])
    time.sleep(1)
    event_ESCChanged_notify(conn, args=[{'on': False}])
    time.sleep(1)
    event_AutoHoldChanged_notify(conn, args=[{'on': False}])
    time.sleep(1)
    event_SuspensionLevel_notify(conn, args=[{'level': 0}])
    time.sleep(1)
    event_TraveledDistance_notify(conn, args=[{'value': 0}])
    time.sleep(1)
    event_CoastEnergyRegenerateMode_notify(conn, args=[{'on': False}])
    time.sleep(1)
    event_CreepMode_notify(conn, args=[{'on': False}])
    time.sleep(1)
    event_GearShiftParkStatus_notify(conn, args=[{'parkReq': False}, {'validSts': False}])
    time.sleep(1)
    event_SportModeAvailableStatus_notify(conn, args=[{'state': 0}])
    time.sleep(1)


def method_all_response(conn, method_name):
    if method_name == "GetSuspFailrStatus":
        method_GetSuspFailrStatus_response(conn, {'failSts': False})
    if method_name == "GetBrkFldLvlWarnMsgStatus":
        method_GetBrkFldLvlWarnMsgStatus_response(conn, {'out': 0})
    if method_name == "getBrkSysWarnIndicateReqSts":
        method_getBrkSysWarnIndicateReqSts_response(conn, {'out': 0})
    if method_name == "BrkSysWarnMsgDisplayReqSts":
        method_BrkSysWarnMsgDisplayReqSts_response(conn, {'out': 0})
    if method_name == "getABSActInfo":
        method_getABSActInfo_response(conn, {'flActSts': False})
    if method_name == "getABSFailSts":
        method_getABSFailSts_response(conn, {'out': False})
    if method_name == "getABSWarnIndicateReqSts":
        method_getABSWarnIndicateReqSts_response(conn, {'out': 0})
    if method_name == "getDisplayReqSts":
        method_getDisplayReqSts_response(conn, {'highPriSts': 0})
    if method_name == "getIndicatorLightReqSts":
        method_getIndicatorLightReqSts_response(conn, {'out': 0})
    if method_name == "getWarnChimeReqSts":
        method_getWarnChimeReqSts_response(conn, {'out': 0})
    if method_name == "getBrkRelsWarnReqSts":
        method_getBrkRelsWarnReqSts_response(conn, {'out': False})
    if method_name == "getHdcWorkSts":
        method_getHdcWorkSts_response(conn, {'out': 0})
    if method_name == "GetAutoHoldFunctionAvailable":
        method_GetAutoHoldFunctionAvailable_response(conn, {'out': False})
    if method_name == "SetEscSportMode":
        method_SetEscSportMode_response(conn, {'out': 'None'})
    if method_name == "getAvhDisplayReqSts":
        method_getAvhDisplayReqSts_response(conn, {'out': 0})
    if method_name == "GetEscSportModeStatus":
        method_GetEscSportModeStatus_response(conn, {'out': False})
    if method_name == "getESCWarnIndicateReqSts":
        method_getESCWarnIndicateReqSts_response(conn, {'out': 0})
    if method_name == "getESCOffIndicateLightSts":
        method_getESCOffIndicateLightSts_response(conn, {'out': False})
    if method_name == "getVehReadySts":
        method_getVehReadySts_response(conn, {'out': False})
    if method_name == "GetAccrPedalPosRate":
        method_GetAccrPedalPosRate_response(conn, {'rate': 0.0})
    if method_name == "GetBrakePedlPsdStatus":
        method_GetBrakePedlPsdStatus_response(conn, {'isPressed': False})
    if method_name == "Lock":
        method_Lock_response(conn, {'out': 'None'})
    if method_name == "Unlock":
        method_Unlock_response(conn, {'out': 'None'})
    if method_name == "GetLockStatus":
        method_GetLockStatus_response(conn, {'out': False})
    if method_name == "GetDisplaySpeed":
        method_GetDisplaySpeed_response(conn, {'speed': 0})
    if method_name == "GetSpeed":
        method_GetSpeed_response(conn, {'speed': 0.0})
    if method_name == "SetTorqueMode":
        method_SetTorqueMode_response(conn, {'out': 'None'})
    if method_name == "GetTorqueMode":
        method_GetTorqueMode_response(conn, {'out': 0})
    if method_name == "SetSuspensionLevel":
        method_SetSuspensionLevel_response(conn, {'out': 'None'})
    if method_name == "GetSuspensionLevel":
        method_GetSuspensionLevel_response(conn, {'out': 0})
    if method_name == "SetAutoHold":
        method_SetAutoHold_response(conn, {'out': 'None'})
    if method_name == "GetAutoHold":
        method_GetAutoHold_response(conn, {'out': False})
    if method_name == "GetHDCFunctionAvailable":
        method_GetHDCFunctionAvailable_response(conn, {'out': False})
    if method_name == "SetHDC":
        method_SetHDC_response(conn, {'out': 'None'})
    if method_name == "GetHDCOn":
        method_GetHDCOn_response(conn, {'out': False})
    if method_name == "SetTowMode":
        method_SetTowMode_response(conn, {'out': 'None'})
    if method_name == "SetCoastEnergyRegenerateMode":
        method_SetCoastEnergyRegenerateMode_response(conn, {'out': 'None'})
    if method_name == "SetCreepMode":
        method_SetCreepMode_response(conn, {'out': 'None'})
    if method_name == "SetESC":
        method_SetESC_response(conn, {'out': 'None'})
    if method_name == "GetESC":
        method_GetESC_response(conn, {'out': False})
    if method_name == "GetEPBOperationStatus":
        method_GetEPBOperationStatus_response(conn, {'out': 0})
    if method_name == "EPBOperation":
        method_EPBOperation_response(conn, {'out': 'None'})
    if method_name == "SetGear":
        method_SetGear_response(conn, {'out': 'None'})
    if method_name == "GetGear":
        method_GetGear_response(conn, {'out': 0})
    if method_name == "GetGearFault":
        method_GetGearFault_response(conn, {'out': ['0']})
    if method_name == "GetWheelSpeed":
        method_GetWheelSpeed_response(conn, {'wheelId': 1})
    if method_name == "GetWheelImpluseCounter":
        method_GetWheelImpluseCounter_response(conn, {'wheelId': 1})
    if method_name == "GetVehicleMotionState":
        method_GetVehicleMotionState_response(conn, {'sts': 0})
    if method_name == "GetSteerErrorReqStatus":
        method_GetSteerErrorReqStatus_response(conn, {'out': 0})
    if method_name == "GetESCWorkStatus":
        method_GetESCWorkStatus_response(conn, {'out': 0})
    if method_name == "GetTraveledDistance":
        method_GetTraveledDistance_response(conn, {'out': 0})
    if method_name == "GetGearShiftParkStatus":
        method_GetGearShiftParkStatus_response(conn, {'parkReq': False})
    if method_name == "GetSportModeAvailableStatus":
        method_GetSportModeAvailableStatus_response(conn, {'out': 0})


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


class ChassisServiceServer:

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

    def send_event_notify(self, conn, event_name, args):
        event = {
            "action": "event",
            "function": f"Update{event_name}Event",
            "args": json.dumps(args)
        }
        conn.sendall(bytes(json.dumps(event), encoding='utf-8'))
        print("发布事件通知：{}".format(event))

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
                     "role": "server",
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
                req_info = json.loads(recv_data.decode("utf-8"))
                print("收到方法请求：{}".format(req_info))
                method_all_response(conn, req_info["function"])
            except OSError as e:
                print(e.__repr__())
                print.info("remote end is closed")
                break
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/output/ChassisService_server.py")
                print.info(e.__repr__())
                continue


if __name__ == "__main__":
    server = ChassisServiceServer()
    window_conn = server.method_run_init("ChassisService")
    event_all_notify(window_conn)
    time.sleep(10)
    server.stop_handler()
