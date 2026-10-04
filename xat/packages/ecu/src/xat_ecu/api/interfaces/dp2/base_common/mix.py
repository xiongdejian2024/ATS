#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :mix.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :需要多个基础能力一起模拟的场景，提供对应实现接口；
"""
from xat_ecu.api.call_tracker import BaseABCMeta
from .tsp import Tsp as CommonTsp
from .logmanagment import LogManagement as CommonLogManagement
from .io import Io as CommonIo
from .serial import Serial as CommonSerial
from .sdtest import SdTest as CommonSdTest
from .buscomm import BusComm as CommonBusComm
from .soa import Soa as CommonSoa
from .ssh import Ssh as CommonSsh
from .diagmock import DiagMock as CommonDiagMock
from .mock import Mock as ComMock


class Mix(metaclass=BaseABCMeta):
    def __init__(
            self,
            tsp: CommonTsp,
            log_manage: CommonLogManagement,
            io: CommonIo,
            serial: CommonSerial,
            sd_tester: CommonSdTest,
            bus_comm: CommonBusComm,
            soa: CommonSoa,
            ssh: CommonSsh,
            diag_mock: CommonDiagMock,
            mock: ComMock
    ):
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
        self.all_bus_data_info = {}
        self.all_bus_msgid_info = {}
