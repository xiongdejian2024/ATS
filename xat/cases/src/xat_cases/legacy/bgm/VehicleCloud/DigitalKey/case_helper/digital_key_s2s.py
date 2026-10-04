#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File         :digital_key_s2s.py
@Time         :2022/11/20 21:05:14
@Author       :jiabin.zhu@jiduauto.com
@Description  :
'''
from xat_ecu.legacy.soa_partner.src.base_partner import *

class DigitalKeyPartner(S2sBaseClass):
    """soa_partner模拟"""

    def __init__(self, partners):
        super().__init__(partners)
        self.lastHandleUid = 0
        self.LastHandleType = 0
        self.APAFunctionStatus = 0
        self.apaFunctionFailReason = 0

    def update_apa_sts(self, pa_sts, last_handle_type, uid='0000000000000001', apa_fail_reason=0):
        """更新apa状态，用于BGM GetApaSts的输入更新"""
        self.lastHandleUid = int(uid, 16)
        self.LastHandleType = last_handle_type
        self.APAFunctionStatus = pa_sts
        self.apaFunctionFailReason = apa_fail_reason
    
    def on_GetAPAStatus(self, partner_key, msg):
        if partner_key == RPAAPA_SERVICE_SERVER and msg["function"] == "GetAPAStatus":
            apa_sts_info = {
                            "paStatus": self.APAFunctionStatus,
                            "lastHandleType": self.LastHandleType,
                            "lastHandleUid": self.lastHandleUid,
                            "apaFunctionFailReason": 0
                        }
            self.send_method_response(partner_key, "GetAPAStatus", apa_sts_info)


# if __name__ == "__main__":
#     # working dir: sat/xat_cases/legacy/bgm
#     partner_process_check()
#     a = DigitalKeyPartner([("KeyService", "client")])
#     time.sleep(3)
#     a.send_method_request("KeyService_client", "GetKeyWhiteListVersion", {"type": 0})
#     time.sleep(1)
#     a.send_method_request("KeyService_client", "GetKeyWhiteListVersion", {"type": 1})
#     time.sleep(1)
