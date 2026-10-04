import time
from contextlib import contextmanager
from typing import List

from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu

from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.common.logmanagment.logmanager import Logmagment
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.soa_partner.src.base_partner import S2sBaseClass
from xat_cases.legacy.tcam.case_helper.constants import CarMode, UsageMode
from xat_cases.legacy.tcam.case_helper.xcall.constants import (
    CALL_SERVICE_CLIENT,
    eCallReqSource,
    eCallOperationCmd,
    eCallFunctionSts,
    eCallType,
    eCallSts
)
from xat_cases.legacy.tcam.cell_network.xcall.interface import XcallInterface


class XcallCaseHelper(XcallInterface):
    def __init__(
            self,
            partner: S2sBaseClass,
            busapp: BusApp,
            tcam_ssh: TCAM_SSH,
            sd_tester: Sd_Tester,
            log_manage: Logmagment,
            ipdu: ISignalIPdu
    ):
        self.partner = partner
        self.busapp = busapp
        self.tcam_ssh = tcam_ssh
        self.sd_tester = sd_tester
        self.log_manage = log_manage
        self.ipdu = ipdu
        self.call_mode_dict = {
            'partner': self.__call_sos_by_soa_partner,
            'can': self.__call_sos_by_can,
            'pwm': self.__call_sos_by_pwm,
            'crash': self.__call_sos_by_crash,
        }

    def __call_sos_by_soa_partner(self):
        try:
            self.partner.send_request_and_ck_resp(
                CALL_SERVICE_CLIENT,
                'SetECallMode',
                {"Cmd": eCallOperationCmd.kSTART_ECALL, "Src": eCallReqSource.kCDC},
                {"out": True}
            )
        except AssertionError as e:
            logger.error(f"点击SOS失败, 原因:{str(e)}")
            assert False, str(e)
        try:
            self.partner.chk_notify(
                CALL_SERVICE_CLIENT,
                'NotifyECallStatus',
                {"Sts": {"FunctionSts": eCallFunctionSts.kECALL_ERROR_SEVERE,
                         "Type": eCallType.kACTIVE,
                         "Status": eCallSts.kWAIT_FOR_CONFIRM}}
            )
        except AssertionError as e:
            logger.error(f"检查点击SOS服务状态失败, 原因:{str(e)}")
            assert False, str(e)

    def __call_sos_by_can(self):
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 0)
        time.sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'CrashStsSafeSts', 1)

    def __call_sos_by_pwm(self):
        pass

    def __call_sos_by_crash(self):
        self.sd_tester.change_car_mode(CarMode.CRASH)

    def trigger_call_sos(self, trigger_mode):
        logger.info("点击SOS")
        mode = self.call_mode_dict.get(trigger_mode)
        if mode is None:
            assert False, f"trigger_mode只支持{[self.call_mode_dict.keys()]}"
        mode()
        logger.info("点击SOS成功")

    def confirm_call_sos(self):
        """
        确认呼叫SOS
        @return:
        """
        logger.info("确认呼叫")
        try:
            self.partner.send_request_and_ck_resp(
                CALL_SERVICE_CLIENT,
                'SetECallMode',
                {"Cmd": eCallOperationCmd.kCONFIRM_ECALL, "Src": eCallReqSource.kCDC},
                {"out": True},
            )
        except AssertionError as e:
            logger.error(f"点击确认呼叫SOS失败, 原因:{str(e)}")
            assert False, str(e)

    def cancel_call_sos(self):
        logger.info("取消拨打SOS")
        try:
            self.partner.send_request_and_ck_resp(
                CALL_SERVICE_CLIENT,
                'SetECallMode',
                {"Cmd": eCallOperationCmd.kHANG_UP_ECALL, "Src": eCallReqSource.kCDC},
                {"out": True}
            )
        except AssertionError as e:
            logger.error(f"拨打SOS失败, 原因:{str(e)}")
            assert False, str(e)
        try:
            self.partner.chk_notify(
                CALL_SERVICE_CLIENT,
                'NotifyECallStatus',
                {"Sts": {
                    "FunctionSts": eCallFunctionSts.kECALL_ERROR_SEVERE,
                    "Type": eCallType.kACTIVE,
                    "Status": eCallSts.kIDLE}}
            )
        except AssertionError as e:
            logger.error(f"拨打SOS失败, 原因:{str(e)}")
            assert False, str(e)
        else:
            logger.info("成功取消拨打SOS")

    def hang_up_call_sos(self):
        """
        挂断呼叫SOS
        @return:
        """
        try:
            self.partner.send_request_and_ck_resp(
                CALL_SERVICE_CLIENT,
                'SetECallMode',
                {"Cmd": eCallOperationCmd.kHANG_UP_ECALL, "Src": eCallReqSource.kCDC},
                {"out": True}
            )
        except AssertionError as e:
            logger.error(f"挂断SOS失败, 原因:{str(e)}")
            assert False, str(e)
        else:
            logger.info("挂断成功")

    def activate_flight_mode(self):
        """
        开启飞行模式
        @return:
        """
        self.tcam_ssh.type_commands('cat /dev/smd8 & echo -en "at+cfun=0\\r\\n" > /dev/smd8', timeout=10)

    def turn_off_flight_mode(self):
        """
        关闭飞行模式
        @return:
        """
        logger.info('关闭飞行模式')
        self.tcam_ssh.type_commands('cat /dev/smd8 & echo -en "at+cfun=1\\r\\n" > /dev/smd8', timeout=10)

    def set_kin_self_test(self):
        """
        自检中
        @return:
        """
        self.sd_tester.change_car_mode(CarMode.Normal)
        time.sleep(0.5)
        self.sd_tester.change_usage_mode(UsageMode.INACTIVE)
        time.sleep(0.5)
        self.sd_tester.change_usage_mode(UsageMode.CONVENIENCE)
        time.sleep(0.5)
        try:
            self.partner.chk_notify(
                CALL_SERVICE_CLIENT,
                'NotifyECallStatus',
                {"Sts": {"FunctionSts": eCallFunctionSts.kIN_SELF_TEST,
                         "Type": eCallType.kIDLE,
                         "Status": eCallSts.kIDLE}}
            )
        except AssertionError as e:
            logger.error(f"检查自检服务状态失败, 原因:{str(e)}")
            assert False, str(e)

    @contextmanager
    def check_jetlog_by_keywords(self, keywords_list: List, timeout: int):
        self.log_manage.check_log_by_keywords_start_thread(
            log_type='EcallService.cpp',
            keywords=keywords_list,
            timeout=timeout
        )
        try:
            yield
        finally:
            assert self.log_manage.check_log_by_keywords_stop_thread()[0]
