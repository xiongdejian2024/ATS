#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File         :gnss_server.py
@Time         :2023/5/16 19:32:14
@Author       :jiabin.zhu@jiduauto.com
@Description  :
'''
import time

from xat_ecu.legacy.soa_partner.src.base_partner import *


class ANPMRCService_Server(S2sBaseClass):
    """soa_partner模拟"""
    def __init__(self, partners):
        super().__init__(partners)
        self.ack_GetMRCSts = True
        self.ack_GetANPDegraedFault = True
        self.notify_flg = True
        self.anpStatus = 0
        self.running = True
        self.register_callback(ANPMRC_SERVICE_SERVER, self.on_GetANPDegraedFault)
        self.register_callback(ANPMRC_SERVICE_SERVER, self.on_GetMRCSts)
        thread1 = Thread(target=self.notify_auto_driver_status, daemon=True)
        thread1.start()
        
    def notify_auto_driver_status(self):
        """起一个线程来控制event发送"""
        while self.running:
            time.sleep(1)
            try:
                if self.notify_flg:
                    self.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus",
                                                {"sts": {"anpStatus": self.anpStatus}})
            except Exception as e:
                logger.info(e)
    
    def on_GetMRCSts(self, partner_key, msg):
        if partner_key == "ANPMRCService_server" and msg["function"] == "GetMRCSts":
            if self.ack_GetMRCSts:
                self.send_method_response(partner_key, "GetMRCSts", 1)
            else:
                self.send_method_response(partner_key, "GetMRCSts", "a")
    
    def on_GetANPDegraedFault(self, partner_key, msg):
        if partner_key == "ANPMRCService_server" and msg["function"] == "GetANPDegraedFault":
            if self.ack_GetANPDegraedFault:
                self.send_method_response(partner_key, "GetANPDegraedFault", 1)
            else:
                self.send_method_response(partner_key, "GetANPDegraedFault", "a")

