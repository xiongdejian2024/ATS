#!/usr/bin/python3
import sys, getopt

# ******************************************************************************
class doip_payload():
    GENERIC_TYPE=0x0000
    VEHICLE_ID_REQ_TYPE=0x0001
    VEHICLE_ID_REQ_EID_TYPE=0x0002
    VEHICLE_ID_REQ_VIN_TYPE=0x0003
    VEHICLE_ANN_TYPE=0x0004
    VEHICLE_ID_RESP_TYPE=0x0004
    ROUTING_ACT_REQ_TYPE=0x0005
    ROUTING_ACT_RESP_TYPE=0x0006
    ALIVE_CHK_REQ_TYPE=0x0007
    ALIVE_CHK_RESP_TYPE=0x0008
    DOIP_ENTITY_STATE_REQ_TYPE=0x4001
    DOIP_ENTITY_STATE_RESP_TYPE=0x4002
    DIAG_POWER_MODE_INFO_REQ_TYPE=0x4003
    DIAG_POWER_MODE_INFO_RESP_TYPE=0x4004
    DIAG_MSG_TYPE=0x8001
    DIAG_MSG_POS_ACK_TYPE=0x8002
    DIAG_MSG_NEG_ACK_TYPE=0x8003
    
    # ****************************************
    def __init__(self, payload_type=None, payload=None):
        self.payload_types = [0x0000,0x0001,0x0002,0x0003,0x0004,0x0005,0x0006,0x0007,0x0008,0x4001,0x4002,0x4003,0x4004,0x8001,0x8002,0x8003]
        self.payload_types_str = ["Nagative Ack","Vehicle ID request","Vehicle ID request with EID","Vehicle ID request with VIN","Vehicle announcement/ID response","Routing Activation Request","Routing Activation Response","Alive Check request","Alive Check response","DoIP Entity status request","DoIP entity status response","Diagnostics power mode info request","Diagnostics power mode info response","Diagnostics message","Diagnostics message positive Ack","Diagnostics message negative Ack"]
        self.protocol_version = 0x02
        self.inverse_protocol_version = self.protocol_version ^ 0xFF
        self.payload_type = payload_type
        if payload:
            self.length = len(payload) + 8
            self.payload=payload
        else:
            self.length = 0
            self.payload= None
            
    # ****************************************
    def get_payload_from_data(self,data):
        if self.is_complete(data) == False:
            return ([], [])
        length = (data[4] << 24) + (data[5] << 16) + (data[6] << 8) + data[7]
        return(data[0:(8+length)],data[(8+length):])
        
    # ****************************************
    def is_complete(self, data):
        if len(data) >= 8:
            length = (data[4] << 24) + (data[5] << 16) + (data[6] << 8) + data[7]
            if (len(data) -8) >= length:
                return True
            print("incomplete payload, expected: %d, received: %d" % (length,len(data)))
        return False
            
    # ****************************************
    def add_data(self,data):
        if len(data) >= 8:
            self.protocol_version = data[0]
            self.inverse_protocol_version = data[1]
            self.payload_type = (data[2] << 8) + data[3]
            self.length = (data[4] << 24) + (data[5] << 16) + (data[6] << 8) + data[7] 
            self.payload = data[8:]
        else:
            self.protocol_version = None
            self.inverse_protocol_version = None
            self.payload_type = None
            self.length = None
            self.payload = None
    # ****************************************
    def data(self):
        return self.payload

    # ****************************************
    def size(self):
        return self.length

    # ****************************************
    def is_valid(self):
        if self.type() in self.payload_types:
            return True
        else:
            print("Payload type invalid, Type: ", self.type(), "- Size: ", self.length, "Payload: ",self.payload)
            return False
    # ****************************************
    def type(self):
        return self.payload_type
    
    # ****************************************
    def type_str(self):
        return self.payload_types_str[self.payload_types.index(self.payload_type)]
    
    # ****************************************
    def is_negative_ack_type(self):
        if self.payload_type == 0x00:
            return True
        return False
    # ****************************************
    def is_vin_req_type(self):
        if self.payload_type == 0x01:
            return True
        return False
    # ****************************************
    def is_vin_req_with_EID_type(self):
        if self.payload_type == 0x02:
            return True
        return False
    # ****************************************
    def is_vin_req__with_vin_type(self):
        if self.payload_type == 0x03:
            return True
        return False
    # ****************************************
    def is_vehicle_announcement_or_id_type(self):
        if self.payload_type == 0x04:
            return True
        return False
    # ****************************************
    def is_routing_act_req_type(self):
        if self.payload_type == 0x05:
            return True
        return False
    # ****************************************
    def is_routing_act_resp_type(self):
        if self.payload_type == 0x06:
            return True
        return False
    # ****************************************
    def is_alive_check_req_type(self):
        if self.payload_type == 0x07:
            return True
        return False
    # ****************************************
    def is_alive_check_resp_type(self):
        if self.payload_type == 0x08:
            return True
        return False
    # ****************************************
    def is_entity_status_req_type(self):
        if self.payload_type == 0x4001:
            return True
        return False
    # ****************************************
    def is_entity_status_resp_type(self):
        if self.payload_type == 0x4002:
            return True
        return False
    # ****************************************
    def is_diags_power_mode_info_req_type(self):
        if self.payload_type == 0x4003:
            return True
        return False
    # ****************************************
    def is_diags_power_mode_info_resp_type(self):
        if self.payload_type == 0x4004:
            return True
        return False
    # ****************************************
    def is_diags_msg_type(self):
        if self.payload_type == 0x8001:
            return True
        return False
    # ****************************************
    def is_diags_msg_pos_ack_type(self):
        if self.payload_type == 0x8002:
            return True
        return False
    # ****************************************
    def is_diags_msg_neg_ack_type(self):
        if self.payload_type == 0x8003:
            return True
        return False
