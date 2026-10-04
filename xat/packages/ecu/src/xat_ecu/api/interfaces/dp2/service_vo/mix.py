#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :mix.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :需要多个基础能力一起模拟的场景，提供对应实现接口；
"""

from xat_ecu.api.interfaces.dp2.base_common.mix import Mix as BaseMix
from .tsp import Tsp
from .logmanagment import LogManagement
from .io import Io
from .serial import Serial
from .sdtest import SdTest
from .buscomm import BusComm
from .soa import Soa
from .ssh import Ssh
from .diagmock import DiagMock
from .mock import Mock


class Mix(BaseMix):
    def __init__(
            self,
            tsp: Tsp,
            log_manage: LogManagement,
            io: Io,
            serial: Serial,
            sd_tester: SdTest,
            bus_comm: BusComm,
            soa: Soa,
            ssh: Ssh,
            diag_mock: DiagMock,
            mock: Mock):
        super().__init__(tsp, log_manage, io, serial, sd_tester, bus_comm, soa, ssh, diag_mock, mock)
        self.tsp = tsp
        self.log_manage = log_manage
        self.io = io
        self.serial = serial
        self.sd_tester = sd_tester
        self.bus_comm = bus_comm
        self.soa = soa
        self.ssh = ssh
        self.diag_mock = diag_mock
        self.mock = mock
