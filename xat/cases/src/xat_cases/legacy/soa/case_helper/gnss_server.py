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


class GNSSServiceServer(S2sBaseClass):
    """soa_partner模拟"""

    def __init__(self, partners):
        super().__init__(partners)
        self.TimeManagementService = True
        self.UTCDate = 0
        self.UTCTime = 0
        self.timestamp = 0
        self.fixType = 0
        self.GNSSStatus = 8
        self.longitude = 0
        self.latitude = 0
        self.ellipsoid = 0
        self.velocityOverGround = 0
        self.trueNorthVelocity = 0
        self.trueEastVelocity = 0
        self.downVelocity = 0
        self.heading = 0
        self.estimateHorizontalAccuracy = 0
        self.estimatedLongPrecision = 0
        self.estimatedLatPrecision = 0
        self.estimatedHighPrecision = 0
        self.estimateVelocityAccuracy = 0
        self.estimatedNorthVelocityPrecision = 0
        self.estimatedEastVelocityPrecision = 0
        self.estimatedDownVelocityPrecision = 0
        self.estimatedHeadingPrecision = 0
        self.satellitesInView = 0
        self.satellitesInUse = 0
        self.CN0 = 0
        self.PDOP = 0
        self.HDOP = 0
        self.GDOP = 0
        self.TDOP = 0
        self.VDOP = 0
        self.leapSecond = 0
        self.GNSSErrorCode = 0
        self.coordinateSystem = 0
        self.stateIliteInViewInfo = {"numberOfSatellitesInView": 0,
                                     "satelliteInfo": [{"satelliteID": 1,
                                                        "elevationInDegrees": 1,
                                                        "azimuthInDegrees": 1,
                                                        "sNRIndB": 1,
                                                        "fixStatus": 0}]}

    @property
    def gnss_info(self):
        gnss_info = {
            "UTCDate": self.UTCDate,
            "UTCTime": self.UTCTime,
            "timestamp": self.timestamp,
            "fixType": self.fixType,
            "GNSSStatus": self.GNSSStatus,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "ellipsoid": self.ellipsoid,
            "velocityOverGround": self.velocityOverGround,
            "trueNorthVelocity": self.trueNorthVelocity,
            "trueEastVelocity": self.trueEastVelocity,
            "downVelocity": self.downVelocity,
            "heading": self.heading,
            "estimateHorizontalAccuracy": self.estimateHorizontalAccuracy,
            "estimatedLongPrecision": self.estimatedLongPrecision,
            "estimatedLatPrecision": self.estimatedLatPrecision,
            "estimatedHighPrecision": self.estimatedHighPrecision,
            "estimateVelocityAccuracy": self.estimateVelocityAccuracy,
            "estimatedNorthVelocityPrecision": self.estimatedNorthVelocityPrecision,
            "estimatedEastVelocityPrecision": self.estimatedEastVelocityPrecision,
            "estimatedDownVelocityPrecision": self.estimatedDownVelocityPrecision,
            "estimatedHeadingPrecision": self.estimatedHeadingPrecision,
            "satellitesInView": self.satellitesInView,
            "satellitesInUse": self.satellitesInUse,
            "CN0": self.CN0,
            "PDOP": self.PDOP,
            "HDOP": self.HDOP,
            "GDOP": self.GDOP,
            "TDOP": self.TDOP,
            "VDOP": self.VDOP,
            "leapSecond": self.leapSecond,
            "GNSSErrorCode": self.GNSSErrorCode,
            "coordinateSystem": self.coordinateSystem,
            "stateIliteInViewInfo": self.stateIliteInViewInfo,
        } 
        return gnss_info
    
    def on_GetGNSSInformation(self, partner_key, msg):
        if "GNSSService_server" in partner_key and msg["function"] == "GetGNSSInformation":
            if msg["function"] == "GetGNSSInformation":
                    self.send_method_response(partner_key, "GetGNSSInformation", self.gnss_info)


if __name__ == "__main__":
    # working dir: sat/xat_cases/legacy/bgm
    pass
