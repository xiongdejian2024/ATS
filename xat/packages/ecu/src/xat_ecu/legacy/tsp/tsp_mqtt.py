# import grpc
import binascii
import ctypes
import sys
import os
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from groot2.cloud.biz.mock_cloud.manager import VehicleCloudSimulator
from google.protobuf.json_format import MessageToJson

from xat_ecu.legacy.tsp.data.proto.rvc.common_pb2 import CmdSign
from xat_ecu.legacy.tsp.data.proto.rvc.realtime_cmd_pb2 import RealtimeCmdReq
from xat_ecu.legacy.tsp.data.proto.rvc.subscribe_cmd_pb2 import SubscribeTaskReq
import base64
from xat_ecu.legacy.common.logger import logger
import time



def sign_payload(msg):
    with open("./data/certificate/ec_key.pem", 'rb') as f:
        pem_data = f.read()
    private_key = serialization.load_pem_private_key(pem_data, password=None, backend=default_backend())
    return private_key.sign(msg, ec.ECDSA(hashes.SHA256()))


class TSPClient:
    def __init__(self, vid="51e5701381e5f796e7887e9bea1e87b9"):
        self.manager = VehicleCloudSimulator(
            env_name="staging",
            vid=vid,
        )
        self.basic_rvc_cmd = RealtimeCmdReq()
        self.cmd_sign = CmdSign()
        self.schedule_cmd = SubscribeTaskReq()
        self.basic_rvc_cmd.execId = str(time.time()).split(".")[0]
        self.basic_rvc_cmd.vehicleModel = 61
        self.basic_rvc_cmd.cmdCode = 1
        self.basic_rvc_cmd.cmdDetail.lock_control.op = 1
        self.basic_rvc_cmd.cmdDetail.lock_control.userId = "12345678"
        self.basic_rvc_cmd.timestamp = int(time.time())
        self.basic_rvc_cmd.operateUserId = 111111111111
        self.basic_rvc_cmd.vid = vid

    def send_request(self, cmdcode=1, operation=1):
        self.basic_rvc_cmd.cmdCode = cmdcode
        self.basic_rvc_cmd.cmdDetail.lock_control.op = operation
        cmd_body = self.basic_rvc_cmd.SerializeToString()
        # sign编码是base64
        # cmd_body编码不是base64
        self.cmd_sign.cmdBody = cmd_body
        signed_data = sign_payload(cmd_body)
        self.cmd_sign.sign = base64.b64encode(signed_data)
        payload = base64.b64encode(self.cmd_sign.SerializeToString()).decode('ISO-8859-1')
        msg_id = self.manager.push_to_vehicle(
            service="v.rvc",
            api="RVCCmd",
            payload=payload,
        )
        time.sleep(0.5)
        results = self.manager.query_vehicle_resp(msg_id=msg_id)
        if not results:
            logger.error(f"没有查到上行 msg_id: {msg_id}")
        else:
            logger.info(f"查到上行 msg_id: {msg_id} 的结果: {results}")


if __name__ == '__main__':
    tsp_client = TSPClient()
    tsp_client.send_request()
