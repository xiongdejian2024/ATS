#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_central_lock.py
@Time         :2024/11/07 11:44
@Author       :renyue.dai@jiduauto.com
@Description  :
"""
from xat_cases.dp2.cd_mcu.case_helper.test_abc_base import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.sdk.Internal_ETH.tools.eth_internal_dp20 import *
from xat_ecu.legacy.common.logger import Logger
from xat_ecu.api.interfaces.dp2.cd_mcu.buscomm import *
# from sdk_interface.interfaces.dp2.cd_mcu.ssh import *
from xat_cases.dp2.cd_mcu.case_helper.McuKeywords import McuKeywords


class TestCentralLock(CommonABCTestBase):

    def before_class(self, ecu: EcuInfo):
        logger.info("before_class")
        self.mcu_obj = McuKeywords(self.bus_comm)
        self.mcu_obj.start_mcu_forward_and_pre_env_to_ready()
        self.mcu_obj.start_mock_ecu()
        super().before_class(self, ecu)

    def before_each_func(self, ecu: EcuInfo):
        super().before_each_func(ecu)
        logger.info("before_each_func")

    def after_each_func(self, ecu: EcuInfo):
        super().after_each_func(ecu)
        logger.info("after_each_func")

    def after_class(self, ecu: EcuInfo):
        logger.info("after_class")
        self.mcu_obj.stop_mock_ecu()
        time.sleep(2)
        super().after_class(self, ecu)

    def test_demo(self):
        logger.info(f"test demo")

    def test_101001(self):
        logger.info("开始用例")
        self.bus_comm.set("publiccanfd", "LCURPublicCANFDFr07", "TrMtnSts", 5)
        self.bus_comm.set("publiccanfd", "LCURPublicCANFDFr07", "TrOutdSwtSts", 2)
        time.sleep(1)
        self.bus_comm.set("publiccanfd", "LCURPublicCANFDFr07", "TrOutdSwtSts", 1)
        print(000000000000)
        self.bus_comm.check("publiccanfd", "CCUMCUCDPublicCANFDFr04",
                            "TrCtrlReq", 3)

    # def test_101013(self):
    #     logger.info("------------UsgMod静止状态，开启充电口盖成功-------------")
    #     VehMovgDirVehMovgDir = [1,2,3]
    #     # 车辆处于静止状态：PropulsionCANFD ::CCUMCUCDPropulsionCANFDSignalIPdu01 ::VMMGlbSigUsgModSts
    #     # =0_UsgModSts1_UsgModAbdnd或1_UsgModSts1_UsgModInActv或2_UsgModSts1_UsgModCnvinc；
    #     logger.info("------------测试用例前提条件-------------")
    #     self.bus_comm.set("propulsioncanfd","LCURPublicCANFDFr07","VehMovgDirVehMovgDir",1)
    #     self.ETH_LCUL.send_pdu(0x50FF05)
    #     self.ETH_LCUL.set_signal_value("ChargeLidMoveSts", 2)
    #     time.sleep(2)
    #     logger.info("------------测试步骤-------------")
    #     # NormChargeLidMoveCtrl从任意状态
    #     # （0_OpenClsCtrlReq_Idle或2_OpenClsCtrlReq_Close）切换到 1_OpenClsCtrlReq_Open
    #     self.ETH_CDSOC.send_pdu(0x40206F)
    #     self.ETH_CDSOC.set_signal_value("NormChargeLidMoveCtrl", 2)
    #     time.sleep(1)
    #     self.ETH_CDSOC.set_signal_value("NormChargeLidMoveCtrl", 1)
    #     print(000000000000)
    #     self.bus_comm.check("publiccanfd", "CCUMCUCDPublicCANFDFr04",
    #                         "TrCtrlReq",3,0.5)
    #     self.bus_comm.check("publiccanfd", "CCUMCUCDPublicCANFDFr04",
    #                         "TrCtrlReq",0)
    #     print(111111111111)
    # def test_101014(self):
    #     logger.info("------------VehMovgDir静止状态，开启充电口盖成功-------------")
    #     VehMovgDirVehMovgDir = [1,2,3]
    #     # 车辆处于静止状态：PropulsionCANFD ::CCUMCUCDPropulsionCANFDSignalIPdu01 ::VMMGlbSigUsgModSts
    #     # =0_UsgModSts1_UsgModAbdnd或1_UsgModSts1_UsgModInActv或2_UsgModSts1_UsgModCnvinc；
    #     logger.info("------------测试用例前提条件-------------")
    #     self.bus_comm.set("propulsioncanfd","LCURPublicCANFDFr07","VehMovgDirVehMovgDir",1)
    #     self.ETH_LCUL.send_pdu(0x50FF05)
    #     self.ETH_LCUL.set_signal_value("ChargeLidMoveSts", 2)
    #     self.ChangeUsgMod(2)
    #     time.sleep(2)
    #     logger.info("------------测试步骤-------------")
    #     # NormChargeLidMoveCtrl从任意状态
    #     # （0_OpenClsCtrlReq_Idle或2_OpenClsCtrlReq_Close）切换到 1_OpenClsCtrlReq_Open
    #     self.ETH_CDSOC.send_pdu(0x40206F)
    #     self.ETH_CDSOC.set_signal_value("NormChargeLidMoveCtrl", 2)
    #     time.sleep(1)
    #     self.ETH_CDSOC.set_signal_value("NormChargeLidMoveCtrl", 1)
    #     print(000000000000)
    #     self.bus_comm.check("publiccanfd", "CCUMCUCDPublicCANFDFr04",
    #                         "TrCtrlReq",3,0.5)
    #     self.bus_comm.check("publiccanfd", "CCUMCUCDPublicCANFDFr04",
    #                         "TrCtrlReq",0)
    #     print(111111111111)
    # def test_101007(self):
    #     logger.info("------------关闭充电口盖成功-------------")
    #     VehMovgDirVehMovgDir = [1,2,3]
    #     logger.info("------------测试用例前提条件-------------")
    #     self.bus_comm.set("propulsioncanfd","VCUPropulsionCANFDFr08","OnBdChrgrHndlSts",0)

    #     self.ETH_LCUL.send_pdu(0x50FF05)
    #     self.ETH_LCUL.set_signal_value("ChargeLidMoveSts", 2)
    #     time.sleep(2)
    #     logger.info("------------测试步骤-------------")
    #     # NormChargeLidMoveCtrl从任意状态
    #     # （0_OpenClsCtrlReq_Idle或2_OpenClsCtrlReq_Close）切换到 1_OpenClsCtrlReq_Open
    #     self.ETH_CDSOC.send_pdu(0x40206F)
    #     self.ETH_CDSOC.set_signal_value("NormChargeLidMoveCtrl", 2)
    #     time.sleep(1)
    #     self.ETH_CDSOC.set_signal_value("NormChargeLidMoveCtrl", 1)
    #     print(000000000000)
    #     self.bus_comm.check("publiccanfd", "CCUMCUCDPublicCANFDFr04",
    #                         "TrCtrlReq",3,0.5)
    #     self.bus_comm.check("publiccanfd", "CCUMCUCDPublicCANFDFr04",
    #                         "TrCtrlReq",0)
    #     print(111111111111)
    # def test_223(self):
    #     logger.info("111111111111111")
    #     self.ChangeUsgMod(2)
    def test_123(self):
        # # self.ChangeUsgMod(2)
        # self.ETH_LCUL.empty()
        # time.sleep(2)
        # result = self.ETH_LCUL.get_signal_values("FLPwrSideDoorPosnSetPosnCtrlSrc")
        # # print(11111,result)
        # logger.info(f"self.ETH_LCUL.get_signal_values:{result}")
        # self.ETH_LCUL.send_pdu(0x502001)
        # self.ETH_LCUL.set_signal_value("PrimBattChrgnUReq", 5)

        # self.ETH_LCUR.empty()
        # time.sleep(2)
        # result = self.ETH_LCUR.get_signal_values("FRPwrSideDoorPosnSetPosnCtrlSrc")
        # # print(22222,result)
        # logger.info(f"self.ETH_LCUR.get_signal_values:{result}")
        # self.ETH_LCUR.send_pdu(0x602004)
        # self.ETH_LCUR.set_signal_value("FRPwrDoorMotPrmStopEvnt", 2)  # 如果是周期报文，会用修改后的值周期发送
        # time.sleep(2)
        # self.ETH_CDSOC.empty()
        # time.sleep(2)
        # result = self.ETH_CDSOC.get_signal_values("ActFusnSeatStsDrvrSeatSts")
        # logger.info(f"self.ETH_CDSOC.get_signal_values:{result}")
        # # print(33333,result)
        # self.ETH_CDSOC.send_pdu(0x402002)
        # self.ETH_CDSOC.set_signal_value("ClimateAirFlwBascCalcnReLe", 1)  # 如果是周期报文，会用修改后的值周期发送
        # time.sleep(1)
        print(888888888888)

    def test_SocketMulticast(self):
        logger.info("------------LCUL SocketMulticast-------------")
        self.mcu_obj.ETH_LCUL.empty()
        time.sleep(0.2)
        result = self.mcu_obj.ETH_LCUL.get_signal_values("CrashInfoImpctDvx")
        # print(11111,result)
        logger.info(f"self.ETH_LCUL.get_signal_values:{result}")
        # self.mcu_obj.ETH_LCUL.send_pdu(0x502001)
        self.mcu_obj.ETH_LCUL.set_signal_value("SecRowLeOccpSnsrRawSts", 5)
        time.sleep(1)
        self.mcu_obj.ETH_LCUL.set_signal_value("SecRowLeOccpSnsrRawSts", 3)
        time.sleep(1)

        logger.info("------------LCUR SocketMulticast-------------")
        self.mcu_obj.ETH_LCUR.empty()
        time.sleep(0.2)
        result = self.mcu_obj.ETH_LCUR.get_signal_values("GearLvrIndcnRealGearLvrIndcn")
        # print(22222,result)
        logger.info(f"self.ETH_LCUR.get_signal_values:{result}")
        # self.mcu_obj.ETH_LCUR.send_pdu(0x602004)
        self.mcu_obj.ETH_LCUR.set_signal_value("FRDoorOpenClsSts", 2)  # 如果是周期报文，会用修改后的值周期发送
        time.sleep(1)
        self.mcu_obj.ETH_LCUR.set_signal_value("FRDoorOpenClsSts", 3)
        time.sleep(1)

        logger.info("------------CDSOC SocketMulticast-------------")
        self.mcu_obj.ETH_CDSOC.empty()
        time.sleep(2)
        result = self.mcu_obj.ETH_CDSOC.get_signal_values("BrkOilLvl")
        logger.info(f"self.ETH_CDSOC.get_signal_values:{result}")
        # print(33333,result)
        # self.mcu_obj.ETH_CDSOC.send_pdu(0x402002)
        self.mcu_obj.ETH_CDSOC.set_signal_value("SetCarModProxyReq", 1)  # 如果是周期报文，会用修改后的值周期发送
        time.sleep(1)

    def test_1111(self):
        # self.mcu_obj.ChangeUsgMod(1)
        # time.sleep(1)
        self.mcu_obj.SetVehMovgDir(2)
        time.sleep(1)
        self.mcu_obj.SetDoorOpenClsSts(2, 2, 2, 2, 2)
        time.sleep(1)
        self.mcu_obj.CheckDoorOpenClsSts(2, 2, 2, 2, 2)
        self.mcu_obj.SetLocalCenLockCtrl(1, 6)
        McutoSoc_FotaModSts = self.mcu_obj.ETH_CDSOC.get_signal_values("FotaModSts")
        logger.info(f"McutoSoc_FotaModSts:{McutoSoc_FotaModSts}")
        # time.sleep(5)
        self.mcu_obj.CheckCenLockSts(1, 0xe, 2)

    def test_100923(self):
        self.bus_comm.set('publiccanfd', 'CCUMCUADPublicCANFDFr07', 'ADActT', 120)
        time.sleep(10)
        result = self.mcu_obj.GetSignalvalues_Eth("ETH_CDSOC", "ECUCoolgReq")
        result1 = self.mcu_obj.GetSignalvalues_Eth("ETH_CDSOC", "ECUCooltFlwReq")
        logger.info(f"ECUCoolgReq:{result}")
        logger.info(f"ECUCooltFlwReq:{result1}")
        # result = self.mcu_obj.ETH_CDSOC.get_signal_values("ECUCoolgReq")
        # result1 = self.mcu_obj.ETH_CDSOC.get_signal_values("ECUCooltFlwReq")
        # logger.info(f"ECUCoolgReq:{result}")
        # logger.info(f"ECUCooltFlwReq:{result1}")

    def test_100583(self):
        self.mcu_obj.SetDoorOpenClsSts(2, 2, 2, 2, 2)
        time.sleep(2)

    def test_SocTo(self):
        self.mcu_obj.ETH_CDSOC.set_signal_value("SetUsgModUpProxyReq", 1)
        self.mcu_obj.SetDoorOpenClsSts(0, 0, 0, 0, 0)
        self.mcu_obj.SetDoorOpenClsSts(2, 2, 2, 2, 2)

        # time.sleep(1)
        # self.mcu_obj.ETH_CDSOC.set_signal_value("LocalCenLockCtrlLockCmdTrigSrc", 6)
        # self.mcu_obj.ETH_CDSOC.set_signal_value("LocalCenLockCtrlCentralLockCmd", 1)
        # self.mcu_obj.ETH_CDSOC.send_pdu(0x402006)
        self.mcu_obj.SetLocalCenLockCtrl(1, 6)
        time.sleep(5)

        # self.mcu_obj.SetLocalCenLockCtrl(2, 8)
        # time.sleep(5)

    def test_100654(self):
        Testdict = {
            'VehMovgDir': 2, 'FLDoorSts': 2, 'FRDoorSts': 2, 'RLDoorSts': 2, 'RRDoorSts': 2, 'TrSts': 2,
            # 以上是测试case前提条件
            'CentralLockCmd': 1, 'CmdTrigSrc': 1,
            # 以上是测试case触发条件
            'CenLockSts': 1, 'TrigSrc': 0xe, 'TrigSrcType': 2, 'UpdateEvnt': -1
            # 以上是测试case预期结果
        }
        self.mcu_obj.CenLockStsTest_SOCtoMCU1(Testdict)
