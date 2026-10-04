
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.tsp.data.proto.rvs import bus_status_pb2 as bus_status
from xat_ecu.legacy.tsp.data.proto.rvs import cabin_status_pb2 as cabin_status
from xat_ecu.legacy.tsp.data.proto.rvs import driving_status_pb2 as driving_status
from xat_ecu.legacy.tsp.data.proto.rvs import eic_charging_pb2 as charging_info
from xat_ecu.legacy.tsp.data.proto.rvs import wti_info_pb2 as wti_info
from xat_ecu.legacy.tsp.data.proto.rvs import gis_and_travel_pb2 as position_info
from xat_ecu.legacy.tsp.data.proto.rvs import ecu_pb2 as ecu_info
from xat_ecu.legacy.tsp.data.proto.rvs import vehicle_body_pb2 as vehicle_body
from xat_ecu.legacy.tsp.data.proto.rvs import vehicle_mode_pb2 as vehicle_mode
from xat_ecu.legacy.tsp.data.proto.rvs import block_head_pb2 as block_head
from xat_ecu.legacy.tsp.data.proto.rvs import AVP_pb2 as avp_status
from xat_ecu.legacy.tsp.data.proto.rvs import charging_bluetooth_pb2 as BLEEicCharging_info
import time
import json



class ProtoParse:
    def __init__(self):
        pass

    def get_data_block(self, raw_data):
        vehicle = block_head.BlockHead()
        logger.info("Client received: {0}".format(vehicle.FromString(raw_data)))
        return vehicle.FromString(raw_data)

    def get_ecu_version(self, raw_data):
        vehicle = ecu_info.EcuBlock()
        logger.info("Client received: {0}".format(vehicle.FromString(raw_data)))
        return vehicle.FromString(raw_data)

    def get_vehicle_mode(self, raw_data):
        vehicle = vehicle_mode.VehicleModeBlock()
        logger.info("Client received: {0}".format(vehicle.FromString(raw_data)))
        return vehicle.FromString(raw_data)

    def get_vehicle_body_info(self, raw_data):
        vehicle = vehicle_body.VehicleBodyBlock
        logger.info("Client received: {0}".format(vehicle.FromString(raw_data)))
        return vehicle.FromString(raw_data)

    def get_cabin_info(self, raw_data):
        vehicle = cabin_status.CabinStatusBlock()
        logger.info("Client received: {0}".format(vehicle.FromString(raw_data)))
        return vehicle.FromString(raw_data)

    def get_position_info(self, raw_data):
        vehicle = position_info.GISAndTravelBlock()
        logger.info("Client received: {0}".format(vehicle.FromString(raw_data)))
        return vehicle.FromString(raw_data)

    def get_driving_info(self, raw_data):
        vehicle = driving_status.DrivingStatusBlock()
        logger.info("Client received: {0}".format(vehicle.FromString(raw_data)))
        return vehicle.FromString(raw_data)

    def get_charging_info(self, raw_data):
        vehicle = charging_info.EicChargingBlock()
        logger.info("Client received: {0}".format(vehicle.FromString(raw_data)))
        return vehicle.FromString(raw_data)
    
    def get_bleeiccharging_info(self, raw_data):
        vehicle = BLEEicCharging_info.ChargingBlueToothBlock()
        logger.info("Client received: {0}".format(vehicle.FromString(raw_data)))
        return vehicle.FromString(raw_data)

    def get_wti_info(self, raw_data):
        vehicle = wti_info.WtiInfoBlock()
        logger.info("Client received: {0}".format(vehicle.FromString(raw_data)))
        return vehicle.FromString(raw_data)

    def get_function_info(self, raw_data):
        vehicle = bus_status.BusStatusBlock()
        logger.info("Client received: {0}".format(vehicle.FromString(raw_data)))
        return vehicle.FromString(raw_data)

    def get_avp_info(self, raw_data):
        vehicle = avp_status.AVPBlock()
        logger.info("Client received: {0}".format(vehicle.FromString(raw_data)))
        return vehicle.FromString(raw_data)

    def get_vehicle_messages(self, blcokid, raw_data):
        block_dict = {
            '10102':self.get_vehicle_mode,
            '10103':self.get_vehicle_body_info,
            '10105':self.get_position_info,
            '10107':self.get_charging_info,
            '10207':self.get_bleeiccharging_info,
            '19001':self.get_avp_info,
            '10109':self.get_function_info
        }
        block_id = str(self.get_vehicle_mode(raw_data).head.blockID)
        if block_id == blcokid:
            return block_dict[block_id](raw_data)