# -*- coding: utf-8 -*-
"""
@File        : BgmFotaCase.py
@Author      : quan.sun@jiduauto.com
@Time        : 2022/09/19 17:35
@Description :
@Examples    :
"""

import time
from xat_ecu.legacy.soa_partner.src.fotasim import FotaSim


class BgmFotaCase:
    def test_bgm_tcam(self):
        # @value(0) IDLE,
        # @value(1) QUERY,
        # @value(2) NEW_TASK,
        # @value(3) DOWNLOADING,
        # @value(4) ACTIVE,
        # @value(5) UPDATE,
        # @value(6) ROLLBACK,
        # @value(7) FailedNotDriving

        self.fotasim = FotaSim(False, True, False, True)
        self.fotasim.fota_master_client.start()
        self.fotasim.cdc_ua_server.start()
        self.fotasim.acu_ua_server.start()

        time.sleep(10000)

        self.fotasim.fota_master_client.distroy()
        self.fotasim.cdc_ua_server.distroy()
        self.fotasim.acu_ua_server.distroy()

        self.fotasim.kill_operators()

if __name__ == "__main__":
    bgmfotatest = BgmFotaCase()
    bgmfotatest.test_bgm_tcam()
