#!/usr/bin/python3

import threading
import socket
from src.socket_recv import *
from xat_ecu.legacy.common.logger import logger
import time

DEFAULT_PORT = 6789
BUFFER_SIZE = 1024 * 1000

class HighVoltageServer():
    def __init__(self, connect_info):
        self.connect_info = connect_info
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.current_status = ""
        self.battery_low_warn_info = {
            "color": 2, # RED
            'lowTeLSts': 1, # TELLTALE_ON
            'isFirstWarn': True,
            'isSecondWarn': False
            }
        self.hvsoc_info = {
            'realSoc': 90.5,
            'displaySoc': 90,
            "calculateDTESOC": 90.2
             }
        self.charging_msg = {
            'chargingState': 1, # NoCHARGING
            'chargingSpeed': 10,
            'remainChargingTime': 30,
            "isConnect": False,
            "isTempHigh": False,
            "bookChargeResp": 1,
            "bookStateFeedBack": 1,
            "chargeTargetSoc": 95.0,
            'pluggerStatus': 0,
            "chargePower": 1200,
            "totalChargeEnergy": 31526200,
            "chargeEnergyThisTime": 13500,
            "chargeSpeedCalculate": 1300,
            "recentChargeStartTime": int(time.time()) - 1200,
            "recentChargeEndTime": int(time.time()),
            "chargingCompleteStatus": True,
            "bookChargests": 2,
            "isChargingPreparing": False
        }
        self.book_event_info = {
            'type': 0, # CHARGING
            'startTime': 1653031862,
            'endTime': 1653032862
        }
        self.battery_code_info = {
            'length': 24,
            'code': [0x31,0x30,0x33,0x34,0x32,0x36,0x37,0x35,0x39,0x30,0x39,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x31,0x32,0x33,0x34,0x35,0x36]
        }
        self.battery_temperature_info = {
            "maxTemperature": -17.5,
            "minTemperature": -31.5,
            "averageTemperature": -18.0
        }
        self.equipment_info = {
            "maxCurrent": 35.0,
            "actualCurrent": 16.9,
            "equipmentTypes": [2]
        }
        self.battmaintreqsts = 1
        self.output_status = True
        self.hvactivests = 1
        self.battery_heating_info = {
            "currentState": 2,
            "reqState": 1,
            "estimateTime": 35
        }
        self.hvthermal_outofcontrol = False
        self.batt_min_temp = -30.1
        self.plugger_status = 0
        self.start()

    def send_response(self, timeout=5.0):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetHVSOCInfo":
                    CheckMethodRequest(self.tcp_socket, 'GetHVSOCInfo', self.hvsoc_info)
                if req["function"] == "GetChargingInfo":
                    CheckMethodRequest(self.tcp_socket, 'GetChargingInfo', self.charging_msg)
                if req["function"] == "GetBatteryCodeInfo":
                    CheckMethodRequest(self.tcp_socket, 'GetBatteryCodeInfo', self.battery_code_info)
                if req["function"] == "GetOutput":
                    CheckMethodRequest(self.tcp_socket, 'GetOutput', self.output_status)
                if req["function"] == "getEquipmentInfo":
                    CheckMethodRequest(self.tcp_socket, 'getEquipmentInfo', self.equipment_info)
                if req["function"] == "GetBatteryTemperatureInfo":
                    CheckMethodRequest(self.tcp_socket, 'GetBatteryTemperatureInfo', self.battery_temperature_info)
                if req["function"] == "GetHVThermalOutOfControl":
                    CheckMethodRequest(self.tcp_socket, 'GetHVThermalOutOfControl', self.hvthermal_outofcontrol)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/high_voltage_server.py")
                continue
    
    def send_response_select(self, key_value, timeout=2.0):
        time_s = time.time()
        while time.time() - time_s < timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == key_value[0]:
                    logger.info("Received request: {}".format(req))
                    CheckMethodRequest(self.tcp_socket, key_value[0], key_value[1])
                    return True
                else:
                    return False
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/high_voltage_server.py")
                continue

    def listenning_request(self, func_name, timeout=2.0):
        time_s = time.time()
        while time.time()-time_s<timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                logger.info("Length & Data: {0}, {1}".format(len(recv_data), recv_data))
                req = json.loads(recv_data.decode("utf-8"))
                logger.info("Received request: {}".format(req))
                if req["function"] == func_name:
                    return True
                else:
                    return False
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/high_voltage_server.py")
                continue

    def listen_setoutput_request(self, response=False, timeout=2.0):
        time_s = time.time()
        while time.time()-time_s<timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "SetOutput":
                    logger.info("SetOutput: {}".format(req))
                    if response == True:
                        CheckMethodRequest(self.tcp_socket, 'SetOutput', None)
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/high_voltage_server.py")
                continue
        return False

    def listen_getpluggerstatus_request(self, response=True, timeout=2.0):
        time_s = time.time()
        while time.time()-time_s<timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetPluggerStatus":
                    logger.info("GetPluggerStatus: {}".format(req))
                    if response == True:
                        CheckMethodRequest(self.tcp_socket, 'GetPluggerStatus', self.plugger_status)
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/high_voltage_server.py")
                continue
        return False

    def listen_getequipmentinfo_request(self, response=True, timeout=2.0):
        time_s = time.time()
        while time.time()-time_s<timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "getEquipmentInfo":
                    logger.info("getEquipmentInfo: {}".format(req))
                    if response == True:
                        CheckMethodRequest(self.tcp_socket, 'getEquipmentInfo', self.equipment_info)
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/high_voltage_server.py")
                continue
        return False

    def listen_gethvactivests_request(self, response=True, timeout=2.0):
        time_s = time.time()
        while time.time()-time_s<timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GethvActiveSts":
                    logger.info("GethvActiveSts: {}".format(req))
                    if response == True:
                        CheckMethodRequest(self.tcp_socket, 'GethvActiveSts', self.hvactivests)
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/high_voltage_server.py")
                continue
        return False

    def listen_setbatteryheating_request(self, response=True, timeout=2.0):
        time_s = time.time()
        while time.time()-time_s<timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "SetBatteryHeating":
                    logger.info("SetBatteryHeating: {}".format(req))
                    if response == True:
                        CheckMethodRequest(self.tcp_socket, 'SetBatteryHeating', None)
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/high_voltage_server.py")
                continue
        return False
    
    def listen_getbatterytemperatureinfo_request(self, response=True, timeout=2.0):
        time_s = time.time()
        while time.time()-time_s<timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetBatteryTemperatureInfo":
                    logger.info("GetBatteryTemperatureInfo: {}".format(req))
                    if response == True:
                        CheckMethodRequest(self.tcp_socket, 'GetBatteryTemperatureInfo', self.battery_temperature_info)
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/high_voltage_server.py")
                continue
        return False

    def listen_getcharginginfo_request(self, response=True, timeout=2.0):
        time_s = time.time()
        while time.time()-time_s<timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetChargingInfo":
                    logger.info("GetChargingInfo: {}".format(req))
                    if response == True:
                        CheckMethodRequest(self.tcp_socket, 'GetChargingInfo', self.charging_msg)
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/high_voltage_server.py")
                continue
        return False

    def listen_getbatteryheatinginfo_request(self, response=False, timeout=2.0):
        time_s = time.time()
        while time.time()-time_s<timeout:
            try:
                recv_data = self.tcp_socket.recv(BUFFER_SIZE)
                if len(recv_data) == 0:
                    continue
                req = json.loads(recv_data.decode("utf-8"))
                if req["function"] == "GetBatteryHeatingInfo":
                    logger.info("GetBatteryHeatingInfo: {}".format(req))
                    if response == True:
                        CheckMethodRequest(self.tcp_socket, 'GetBatteryHeatingInfo', self.battery_heating_info)
                    return True
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/high_voltage_server.py")
                continue
        return False            

    def start_send_response_hvactiverequest(self):
        self.hvactive_response_sending_thread = threading.Thread(name="hvactive_response", target=self.send_response,args=(self.tcp_socket,) )
        self.hvactive_response_sending_thread.start()

    def stop_send_response_hvactiverequest(self):
        self.hvactive_response_sending_thread.join()

    def notify_batterymintemperature_event(self):
        event = {
            "action": "event",
            "function": "BatteryMinTemperature",
            "args": json.dumps({"value": -30.1})
        }
        try:
            logger.info('Send BatteryMinTemperature: {}'.format(event))
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(
                f"HighVoltageServer:UpdateOutputStateEvent send periodic status failure with broken pipe: {str(e)}")

    def notify_batteryheatinginfo_event(self):
        event = {
            "action": "event",
            "function": "UpdateBatteryHeatingInfoEvent",
            "args": json.dumps({"sts": self.battery_heating_info})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(
                f"HighVoltageServer:UpdateBatteryHeatingInfoEvent send periodic status failure with broken pipe: {str(e)}")

    def notify_hvactivests_event(self):
        event = {
            "action": "event",
            "function": "UpdatehvActiveStsEvent",
            "args": json.dumps({"sts": self.hvactivests})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(
                f"HighVoltageServer:UpdatehvActiveStsEvent send periodic status failure with broken pipe: {str(e)}")

    def notify_outputstate_event(self):
        event = {
            "action": "event",
            "function": "UpdateOutputStateEvent",
            "args": json.dumps({"on": self.output_status})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(
                f"HighVoltageServer:UpdateOutputStateEvent send periodic status failure with broken pipe: {str(e)}")

    def notify_book_event(self):
        event = {
            "action": "event",
            "function": "UpdateNotifyBookEventInfoEvent",
            "args": json.dumps(self.book_event_info)
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"HighVoltageServer:UpdateNotifyBookEventInfoEvent send periodic status failure with broken pipe: {str(e)}")

    def notify_battery_code_info(self):
        event = {
            "action": "event",
            "function": "UpdateNotifyHvBatteryCodeEvent",
            "args": json.dumps({"info": self.battery_code_info})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"HighVoltageServer:UpdateNotifyHvBatteryCodeEvent send periodic status failure with broken pipe: {str(e)}")

    def notify_charging_info(self):
        event = {
            "action": "event",
            "function": "UpdateChargingInfoEvent",
            "args": json.dumps({"info": self.charging_msg})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(f"HighVoltageServer:UpdateChargingInfoEvent send periodic status failure with broken pipe: {str(e)}")

    def notify_hvsoc_info(self):
        event = {
            "action": "event",
            "function": "UpdateHVSOCInfoEvent",
            "args": json.dumps({"info": self.hvsoc_info})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
            pass
        except BrokenPipeError as e:
            logger.error(f"HighVoltageServer:UpdateCHVSOCInfoEvent send periodic status failure with broken pipe: {str(e)}")

    def notify_battmaintreqsts_event(self):
        event = {
            "action": "event",
            "function": "UpdateBattMaintReqStsEvent",
            "args": json.dumps({"sts": self.battmaintreqsts})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(
                f"HighVoltageServer:UpdateBattMaintReqStsEvent send periodic status failure with broken pipe: {str(e)}")

    def notify_hvthermaloutOfcontrol_event(self):
        event = {
            "action": "event",
            "function": "UpdateHVThermalOutOfControlEvent",
            "args": json.dumps({"state": self.hvthermal_outofcontrol})
        }
        try:
            self.tcp_socket.sendall(bytes(json.dumps(event), encoding='utf-8'))
        except BrokenPipeError as e:
            logger.error(
                f"HighVoltageServer:UpdateHVThermalOutOfControlEvent send periodic status failure with broken pipe: {str(e)}")

    def start_notify_hvactivests_event(self):
        self.hvactivests_sending_thread = threading.Thread(name="HvActiveSts", target=self.notify_hvactivests_event,)
        self.hvactivests_sending_thread.start()

    def start_notify_book_event(self):
        self.book_sending_thread = threading.Thread(name="BookEvent", target=self.notify_book_event,)
        self.book_sending_thread.start()


    def start(self):
        logger.info('Start to connect: {}'.format(self.connect_info))
        try:
            self.tcp_socket.connect(self.connect_info)
            self.tcp_socket.settimeout(1)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/soa_partner/src/high_voltage_server.py")
            logger.error(str(e))

def UpdateEventResponse(conn, event_name, args):
    event = {
        "action": "event",
        "function": f"Update{event_name}Event",
        "args": json.dumps(args)
    }
    conn.sendall(bytes(json.dumps(event), encoding='utf-8'))

def CheckMethodRequest(conn, method_name, data):
        resp = {
            "action": "response",
            "function": method_name,
            "result": json.dumps({"out": data})
        }
        logger.info("Send response: {}".format(json.dumps(resp)))
        conn.sendall(bytes(json.dumps(resp), encoding='utf-8'))