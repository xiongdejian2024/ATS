#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :main_obj.py
@Time         :2024/10/25 15:07
@Author       :dejian.xiong@jiduauto.com
@Description  :所有模块对象入口
"""
from xat_ecu.api.interfaces.dp2.basetech.adb import Adb as BaseTechAdb
from xat_ecu.api.interfaces.dp2.cd_mcu.adb import Adb as CdMcuAdb
from xat_ecu.api.interfaces.dp2.cd_service.adb import Adb as CdServiceAdb
from xat_ecu.api.interfaces.dp2.cd_soc.adb import Adb as CdSocAdb
from xat_ecu.api.interfaces.dp2.connectivity_vo.adb import Adb as ConnectivityVoAdb
from xat_ecu.api.interfaces.dp2.lcu.adb import Adb as LcuAdb
from xat_ecu.api.interfaces.dp2.nad.adb import Adb as NadAdb
from xat_ecu.api.interfaces.dp2.service_vo.adb import Adb as ServiceVoAdb

from xat_ecu.api.interfaces.dp2.basetech.buscomm import BusComm as BaseTechBusComm
from xat_ecu.api.interfaces.dp2.cd_mcu.buscomm import BusComm as CdMcuBusComm
from xat_ecu.api.interfaces.dp2.cd_service.buscomm import BusComm as CdServiceBusComm
from xat_ecu.api.interfaces.dp2.cd_soc.buscomm import BusComm as CdSocBusComm
from xat_ecu.api.interfaces.dp2.connectivity_vo.buscomm import BusComm as ConnectivityVoBusComm
from xat_ecu.api.interfaces.dp2.lcu.buscomm import BusComm as LcuBusComm
from xat_ecu.api.interfaces.dp2.nad.buscomm import BusComm as NadBusComm
from xat_ecu.api.interfaces.dp2.service_vo.buscomm import BusComm as ServiceVoBusComm

from xat_ecu.api.interfaces.dp2.basetech.diagmock import DiagMock as BaseTechDiagMock
from xat_ecu.api.interfaces.dp2.cd_mcu.diagmock import DiagMock as CdMcuDiagMock
from xat_ecu.api.interfaces.dp2.cd_service.diagmock import DiagMock as CdServiceDiagMock
from xat_ecu.api.interfaces.dp2.cd_soc.diagmock import DiagMock as CdSocDiagMock
from xat_ecu.api.interfaces.dp2.connectivity_vo.diagmock import DiagMock as ConnectivityVoDiagMock
from xat_ecu.api.interfaces.dp2.lcu.diagmock import DiagMock as LcuDiagMock
from xat_ecu.api.interfaces.dp2.nad.diagmock import DiagMock as NadDiagMock
from xat_ecu.api.interfaces.dp2.service_vo.diagmock import DiagMock as ServiceVoDiagMock

from xat_ecu.api.interfaces.dp2.basetech.io import Io as BaseTechIo
from xat_ecu.api.interfaces.dp2.cd_mcu.io import Io as CdMcuIo
from xat_ecu.api.interfaces.dp2.cd_service.io import Io as CdServiceIo
from xat_ecu.api.interfaces.dp2.cd_soc.io import Io as CdSocIo
from xat_ecu.api.interfaces.dp2.connectivity_vo.io import Io as ConnectivityVoIo
from xat_ecu.api.interfaces.dp2.lcu.io import Io as LcuIo
from xat_ecu.api.interfaces.dp2.nad.io import Io as NadIo
from xat_ecu.api.interfaces.dp2.service_vo.io import Io as ServiceVoIo

from xat_ecu.api.interfaces.dp2.basetech.logmanagment import LogManagement as BaseTechLogManagement
from xat_ecu.api.interfaces.dp2.cd_mcu.logmanagment import LogManagement as CdMcuLogManagement
from xat_ecu.api.interfaces.dp2.cd_service.logmanagment import LogManagement as CdServiceLogManagement
from xat_ecu.api.interfaces.dp2.cd_soc.logmanagment import LogManagement as CdSocLogManagement
from xat_ecu.api.interfaces.dp2.connectivity_vo.logmanagment import LogManagement as ConnectivityVoLogManagement
from xat_ecu.api.interfaces.dp2.lcu.logmanagment import LogManagement as LcuLogManagement
from xat_ecu.api.interfaces.dp2.nad.logmanagment import LogManagement as NadLogManagement
from xat_ecu.api.interfaces.dp2.service_vo.logmanagment import LogManagement as ServiceVoLogManagement

from xat_ecu.api.interfaces.dp2.basetech.mix import Mix as BaseTechMix
from xat_ecu.api.interfaces.dp2.cd_mcu.mix import Mix as CdMcuMix
from xat_ecu.api.interfaces.dp2.cd_service.mix import Mix as CdServiceMix
from xat_ecu.api.interfaces.dp2.cd_soc.mix import Mix as CdSocMix
from xat_ecu.api.interfaces.dp2.connectivity_vo.mix import Mix as ConnectivityVoMix
from xat_ecu.api.interfaces.dp2.lcu.mix import Mix as LcuMix
from xat_ecu.api.interfaces.dp2.nad.mix import Mix as NadMix
from xat_ecu.api.interfaces.dp2.service_vo.mix import Mix as ServiceVoMix

from xat_ecu.api.interfaces.dp2.basetech.sdtest import SdTest as BaseTechSdTest
from xat_ecu.api.interfaces.dp2.cd_mcu.sdtest import SdTest as CdMcuSdTest
from xat_ecu.api.interfaces.dp2.cd_service.sdtest import SdTest as CdServiceSdTest
from xat_ecu.api.interfaces.dp2.cd_soc.sdtest import SdTest as CdSocSdTest
from xat_ecu.api.interfaces.dp2.connectivity_vo.sdtest import SdTest as ConnectivityVoSdTest
from xat_ecu.api.interfaces.dp2.lcu.sdtest import SdTest as LcuSdTest
from xat_ecu.api.interfaces.dp2.nad.sdtest import SdTest as NadSdTest
from xat_ecu.api.interfaces.dp2.service_vo.sdtest import SdTest as ServiceVoSdTest

from xat_ecu.api.interfaces.dp2.basetech.serial import Serial as BaseTechSerial
from xat_ecu.api.interfaces.dp2.cd_mcu.serial import Serial as CdMcuSerial
from xat_ecu.api.interfaces.dp2.cd_service.serial import Serial as CdServiceSerial
from xat_ecu.api.interfaces.dp2.cd_soc.serial import Serial as CdSocSerial
from xat_ecu.api.interfaces.dp2.connectivity_vo.serial import Serial as ConnectivityVoSerial
from xat_ecu.api.interfaces.dp2.lcu.serial import Serial as LcuSdSerial
from xat_ecu.api.interfaces.dp2.nad.serial import Serial as NadSdSerial
from xat_ecu.api.interfaces.dp2.service_vo.serial import Serial as ServiceVoSerial

from xat_ecu.api.interfaces.dp2.basetech.soa import Soa as BaseTechSoa
from xat_ecu.api.interfaces.dp2.cd_mcu.soa import Soa as CdMcuSoa
from xat_ecu.api.interfaces.dp2.cd_service.soa import Soa as CdServiceSoa
from xat_ecu.api.interfaces.dp2.cd_soc.soa import Soa as CdSocSoa
from xat_ecu.api.interfaces.dp2.connectivity_vo.soa import Soa as ConnectivityVoSoa
from xat_ecu.api.interfaces.dp2.lcu.soa import Soa as LcuSoa
from xat_ecu.api.interfaces.dp2.nad.soa import Soa as NadSoa
from xat_ecu.api.interfaces.dp2.service_vo.soa import Soa as ServiceVoSoa

from xat_ecu.api.interfaces.dp2.basetech.ssh import Ssh as BaseTechSsh
from xat_ecu.api.interfaces.dp2.cd_mcu.ssh import Ssh as CdMcuSsh
from xat_ecu.api.interfaces.dp2.cd_service.ssh import Ssh as CdServiceSsh
from xat_ecu.api.interfaces.dp2.cd_soc.ssh import Ssh as CdSocSsh
from xat_ecu.api.interfaces.dp2.connectivity_vo.ssh import Ssh as ConnectivityVoSsh
from xat_ecu.api.interfaces.dp2.lcu.ssh import Ssh as LcuSsh
from xat_ecu.api.interfaces.dp2.nad.ssh import Ssh as NadSsh
from xat_ecu.api.interfaces.dp2.service_vo.ssh import Ssh as ServiceVoSsh

from xat_ecu.api.interfaces.dp2.basetech.tsp import Tsp as BaseTechTsp
from xat_ecu.api.interfaces.dp2.cd_mcu.tsp import Tsp as CdMcuTsp
from xat_ecu.api.interfaces.dp2.cd_service.tsp import Tsp as CdServiceTsp
from xat_ecu.api.interfaces.dp2.cd_soc.tsp import Tsp as CdSocTsp
from xat_ecu.api.interfaces.dp2.connectivity_vo.tsp import Tsp as ConnectivityVoTsp
from xat_ecu.api.interfaces.dp2.lcu.tsp import Tsp as LcuTsp
from xat_ecu.api.interfaces.dp2.nad.tsp import Tsp as NadTsp
from xat_ecu.api.interfaces.dp2.service_vo.tsp import Tsp as ServiceVoTsp

from xat_ecu.api.interfaces.dp2.basetech.mock import Mock as BaseTechMock
from xat_ecu.api.interfaces.dp2.cd_mcu.mock import Mock as CdMcuMock
from xat_ecu.api.interfaces.dp2.cd_service.mock import Mock as CdServiceMock
from xat_ecu.api.interfaces.dp2.cd_soc.mock import Mock as CdSocMock
from xat_ecu.api.interfaces.dp2.connectivity_vo.mock import Mock as ConnectivityVoMock
from xat_ecu.api.interfaces.dp2.lcu.mock import Mock as LcuMock
from xat_ecu.api.interfaces.dp2.nad.mock import Mock as NadMock
from xat_ecu.api.interfaces.dp2.service_vo.mock import Mock as ServiceVoMock


class Adb(BaseTechAdb, CdMcuAdb, CdServiceAdb, CdSocAdb, ConnectivityVoAdb, LcuAdb, NadAdb, ServiceVoAdb):
    pass


class BusComm(BaseTechBusComm, CdMcuBusComm, CdServiceBusComm, CdSocBusComm, ConnectivityVoBusComm,
              LcuBusComm, NadBusComm, ServiceVoBusComm):
    pass


class DiagMock(BaseTechDiagMock, CdMcuDiagMock, CdServiceDiagMock, CdSocDiagMock, ConnectivityVoDiagMock,
               LcuDiagMock, NadDiagMock, ServiceVoDiagMock):
    pass


class Io(BaseTechIo, CdMcuIo, CdServiceIo, CdSocIo, ConnectivityVoIo, LcuIo, NadIo, ServiceVoIo):
    pass


class LogManagement(BaseTechLogManagement, CdMcuLogManagement, CdServiceLogManagement, CdSocLogManagement,
                    ConnectivityVoLogManagement, LcuLogManagement, NadLogManagement, ServiceVoLogManagement):
    pass


class Mix(BaseTechMix, CdMcuMix, CdServiceMix, CdSocMix, ConnectivityVoMix, LcuMix, NadMix, ServiceVoMix):
    pass


class SdTest(BaseTechSdTest, CdMcuSdTest, CdServiceSdTest, CdSocSdTest, ConnectivityVoSdTest, LcuSdTest,
             NadSdTest, ServiceVoSdTest):
    pass


class Serial(BaseTechSerial, CdMcuSerial, CdServiceSerial, CdSocSerial, ConnectivityVoSerial, LcuSdSerial,
             NadSdSerial, ServiceVoSerial):
    pass


class Soa(BaseTechSoa, CdMcuSoa, CdServiceSoa, CdSocSoa, ConnectivityVoSoa, LcuSoa, NadSoa, ServiceVoSoa):
    pass


class Ssh(BaseTechSsh, CdMcuSsh, CdServiceSsh, CdSocSsh, ConnectivityVoSsh, LcuSsh, NadSsh, ServiceVoSsh):
    pass


class Tsp(BaseTechTsp, CdMcuTsp, CdServiceTsp, CdSocTsp, ConnectivityVoTsp, LcuTsp, NadTsp, ServiceVoTsp):
    pass


class Mock(BaseTechMock, CdMcuMock, CdServiceMock, CdSocMock, ConnectivityVoMock, LcuMock, NadMock, ServiceVoMock):
    pass
