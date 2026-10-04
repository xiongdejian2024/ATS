# import grpc
# from ecu_simulator.common.logger import logger
from groot2.cloud.base.jidu_log_service.manager import JiduLogServiceManager
from groot2.cloud.biz.iov_gateway.manager import IovGatewayManager
# from groot2.lib_s.jidu_log_service.manager import JiduLogServiceManager
# from groot2.busi_lib.iov_gateway.manager import IovGatewayManager
# from ecu_simulator.tsp.data.proto.rvs import bus_status_pb2 as bus_status
# from ecu_simulator.tsp.data.proto.rvs import cabin_status_pb2 as cabin_status
# from ecu_simulator.tsp.data.proto.rvs import driving_status_pb2 as driving_status
# from ecu_simulator.tsp.data.proto.rvs import eic_charging_pb2 as charging_info
# from ecu_simulator.tsp.data.proto.rvs import wti_info_pb2 as wti_info
# from ecu_simulator.tsp.data.proto.rvs import gis_and_travel_pb2 as position_info
# from ecu_simulator.tsp.data.proto.rvs import ecu_pb2 as ecu_info
# from ecu_simulator.tsp.data.proto.rvs import vehicle_body_pb2 as vehicle_body
# from ecu_simulator.tsp.data.proto.rvs import vehicle_mode_pb2 as vehicle_mode
# import requests
# from requests.packages import urllib3
import time
import json


class RvsClient:
    def __init__(self, vid="0f98d132b68fc59e47a88042c831ab9a",env_name = "staging"):
        # channel = grpc.insecure_channel("10.80.32.63:9090")
        # self.stub = sync_engine_tsp_pb2_grpc.SyncEngineServiceStub(channel)
        self.vid = vid
        self.manager = IovGatewayManager(env_name=env_name)
        # logger.info("vid: {0}".format(self.vid))

    # def get_ecu_version(self):
    #     grpc_data = self.stub.Get(sync_engine_tsp_pb2.GetBlocksReq(Vid=self.vid, BlockID=10101))
    #     logger.info("Get message: {0}".format(grpc_data))
    #     vehicle_data = grpc_data.Data.Details.pop().Data
    #     vehicle = ecu_info.EcuBlock()
    #     logger.info("Client received: {0}".format(vehicle.FromString(vehicle_data)))
    #     return vehicle.FromString(vehicle_data)

    # def get_vehicle_mode(self):
    #     grpc_data = self.stub.Get(sync_engine_tsp_pb2.GetBlocksReq(Vid=self.vid, BlockID=10102))
    #     logger.info("Get message: {0}".format(grpc_data))
    #     vehicle_data = grpc_data.Data.Details.pop().Data
    #     vehicle = vehicle_mode.VehicleModeBlock()
    #     logger.info("Client received: {0}".format(vehicle.FromString(vehicle_data)))
    #     return vehicle.FromString(vehicle_data)

    # def get_vehicle_body_info(self):
    #     grpc_data = self.stub.Get(sync_engine_tsp_pb2.GetBlocksReq(Vid=self.vid, BlockID=10103))
    #     logger.info("Get message: {0}".format(grpc_data))
    #     vehicle_data = grpc_data.Data.Details.pop().Data
    #     vehicle = vehicle_body.VehicleBodyBlock
    #     logger.info("Client received: {0}".format(vehicle.FromString(vehicle_data)))
    #     return vehicle.FromString(vehicle_data)

    # def get_cabin_info(self):
    #     grpc_data = self.stub.Get(sync_engine_tsp_pb2.GetBlocksReq(Vid=self.vid, BlockID=10104))
    #     logger.info("Get message: {0}".format(grpc_data))
    #     vehicle_data = grpc_data.Data.Details.pop().Data
    #     vehicle = cabin_status.CabinStatusBlock()
    #     logger.info("Client received: {0}".format(vehicle.FromString(vehicle_data)))
    #     return vehicle.FromString(vehicle_data)

    # def get_position_info(self):
    #     grpc_data = self.stub.Get(sync_engine_tsp_pb2.GetBlocksReq(Vid=self.vid, BlockID=10105))
    #     logger.info("Get message: {0}".format(grpc_data))
    #     vehicle_data = grpc_data.Data.Details.pop().Data
    #     vehicle = position_info.GISAndTravelBlock()
    #     logger.info("Client received: {0}".format(vehicle.FromString(vehicle_data)))
    #     return vehicle.FromString(vehicle_data)

    # def get_driving_info(self):
    #     grpc_data = self.stub.Get(sync_engine_tsp_pb2.GetBlocksReq(Vid=self.vid, BlockID=10106))
    #     logger("Get message: {0}".format(grpc_data))
    #     vehicle_data = grpc_data.Data.Details.pop().Data
    #     vehicle = driving_status.DrivingStatusBlock()
    #     logger.info("Client received: {0}".format(vehicle.FromString(vehicle_data)))
    #     return vehicle.FromString(vehicle_data)

    # def get_charging_info(self):
    #     grpc_data = self.stub.Get(sync_engine_tsp_pb2.GetBlocksReq(Vid=self.vid, BlockID=10107))
    #     logger.info("Get message: {0}".format(grpc_data))
    #     vehicle_data = grpc_data.Data.Details.pop().Data
    #     vehicle = charging_info.EicChargingBlock()
    #     logger.info("Client received: {0}".format(vehicle.FromString(vehicle_data)))
    #     return vehicle.FromString(vehicle_data)

    # def get_wti_info(self):
    #     grpc_data = self.stub.Get(sync_engine_tsp_pb2.GetBlocksReq(Vid=self.vid, BlockID=10108))
    #     logger("Get message: {0}".format(grpc_data))
    #     vehicle_data = grpc_data.Data.Details.pop().Data
    #     vehicle = wti_info.WtiInfoBlock()
    #     logger.info("Client received: {0}".format(vehicle.FromString(vehicle_data)))
    #     return vehicle.FromString(vehicle_data)

    # def get_function_info(self):
    #     grpc_data = self.stub.Get(sync_engine_tsp_pb2.GetBlocksReq(Vid=self.vid, BlockID=10109))
    #     logger.info("Get message: {0}".format(grpc_data))
    #     vehicle_data = grpc_data.Data.Details.pop().Data
    #     # vehicle = wti_info.WTIBlock()
    #     vehicle = bus_status.BusStatusBlock()
    #     logger.info("Client received: {0}".format(vehicle.FromString(vehicle_data)))
    #     return vehicle.FromString(vehicle_data)

    # ######################################################################
    # ##########    0.55
    # ######################################################################
    # def get_vehicle_messages(self,vid='0f98d132b68fc59e47a88042c831ab9a'):
    #     blockids = [10101,10102,10103,10104,10105,10106,10107,10108,10109]
    #     grpc_data = self.stub.Get(sync_engine_tsp_pb2.GetBlocksReq(Vid=vid, BlockIDs=blockids))
    #     block_dict = {
    #         '10101':ecu_info.EcuBlock,
    #         '10102':vehicle_mode.VehicleModeBlock,
    #         '10103':vehicle_body.VehicleBodyBlock,
    #         '10104':cabin_status.CabinStatusBlock,
    #         '10105':position_info.GISAndTravelBlock,
    #         '10106':driving_status.DrivingStatusBlock,
    #         '10107':charging_info.EicChargingBlock,
    #         '10108': wti_info.WtiInfoBlock,
    #         '10109': bus_status.BusStatusBlock
    #     }
    #     vehicle_data = grpc_data.Data.GetData
    #     msg_dict = {}
    #     for data in vehicle_data:
    #         msg_dict[str(data.BlockID)] = block_dict[str(data.BlockID)].FromString(data.Data)
    #         logger.info("Received block: {0}, {1}".format(data.BlockID, msg_dict[str(data.BlockID)]))
    #     return msg_dict

    def get_rvs_data_from_cloud(self, blockid):
        cloud_data = self.manager.get_rvs_data(vid=self.vid, block_id=blockid)
        return json.loads(cloud_data)

class CloudLogServer():
    def __init__(self):
        manager = JiduLogServiceManager(env_name="prod")
        ret = manager.common_log_search(
            index="jidulogapp-staging-remote-monitor-wti-*",
            service_name="remote-monitor-wti",
            fuzzy_query=[
                "vehicleModel:VmMarsOne",
            ],
        )
        print("elastic log: {0}".format(ret))


if __name__ == '__main__':
    data = RvsClient().get_rvs_data_from_cloud(10702) #vid="055f7aa6ac9c58587097ab94319adde8"
    print(data)
