# -*- coding: utf-8 -*-
"""
@File        : ltg
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/5/15 20:56
@Description :

"""
import os
import sys
import time
from time import sleep
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from nuc_app import NucApp
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig
from xat_ecu.legacy.sdk.i_signal_i_pdu import *
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.sdk.driver.jidutest_io.io.io_system import IOSystem



class CarMode(object):
    '''
        @value(0) NORMAL,
        @value(1) TRANSPORT,
        @value(2) FACTORY,
        @value(3) CRASH,
        @value(5) DYNO
    '''
    NORMAL = 0
    TRANSPORT = 1
    FACTORY = 2
    CRASH = 3
    DYNO = 5


class UsageMode(object):
    '''
     /** 废弃 */ @value(0) ABANDONED,
        /** 未激活 */ @value(1) INACTIVE,
        /** 充电 */ @value(2) CONVENIENCE,
        /** 激活 */ @value(11) ACTIVE,
        /** 驾驶 */ @value(13) DRIVING
    '''
    INACTIVE = 1
    CONVENIENCE = 2
    ACTIVE = 11
    DRIVING = 13
    ABANDONED = 0


USAGE_MODE_MAP = {
    0: "ABANDONED",
    1: "INACTIVE",
    2: "CONVENIENCE",
    11: "ACTIVE",
    13: "DRIVING",
}

CAR_MODE_MAP = {
    0: "NORMAL",
    1: "TRANSPORT",
    2: "FACTORY",
    3: "CRASH",
    5: "DYNO",
}


class EcuInterFace(object):

    def __init__(self, sd_test=None, ipdu=None, io_obj=None, dk=None, nucapp=None, soa=None, ecu_sim_app=None, cfg=None,
                 **kwargs):
        '''
        @param sd_test:
        @param ipdu:
        @param io:
        @param soa:
        @param ecu_sim_app:
        @param cfg:
        '''

        logger.info(f"====cfg_path=={cfg}===========================================================")
        if isinstance(cfg, str):
            tccfg = ParseTBConfig(cfg)
            self.tc_config = tccfg.yaml_content
        elif isinstance(cfg, dict):
            tb_path = cfg.get("tbcfg")
            tc_path = cfg.get("tccfg")
            self.tc_config = {}
            if tb_path:
                tbcfg = ParseTBConfig(tb_path)
                tb_config = tbcfg.yaml_content
                self.tc_config.update(tb_config)
                if tc_path:
                    tccfg = ParseTBConfig(tc_path)
                    tc_config = tccfg.yaml_content
                    self.tc_config.update(tc_config)
            else:
                self.tc_config = cfg

        # init cls
        self.veh_type = self.tc_config.get("veh_type")
        self.bl_ver = self.tc_config.get("bl_ver")
        if self.veh_type and self.bl_ver:
            self.cls_path = "sdk/data/{}/can_lin_fr_cls/{}".format(self.veh_type, self.bl_ver)
            self.tn_config_path = "config/{}/{}/ecu_network.yaml".format(self.veh_type, self.bl_ver)
        self.dut_ecu = self.tc_config.get("dut_ecu")

        # sdtest 处理
        self.sd_test_obj = None
        self.sd_test_p = sd_test
        self.sd_test_p_start_flag = False

        if sd_test is None:
            self.init_sd_tester()
            # self.start_sd_tester()
        elif isinstance(sd_test, Sd_Tester):
            self.sd_test_obj = sd_test
        elif sd_test:
            # 如果是True  则实例 并启动
            self.init_sd_tester()
            self.start_sd_tester()
        # ipdu
        self.ipdu = None
        self.busapp = kwargs.get("busapp", None)
        self.ipdu_p = ipdu
        self.ipdu_start_flag = False

        if ipdu is None:
            self.init_ipdu()
            # self.start_ipdu()
        elif isinstance(ipdu, ISignalIPdu):
            self.ipdu = ipdu
        elif ipdu:
            self.init_ipdu()
            self.start_ipdu()

        # io
        self.io_obj = None
        if io_obj is None:
            self.init_io()
        elif isinstance(io_obj, IOSystem):
            self.io_obj = io_obj

        # 数字钥匙的处理
        if isinstance(dk, DigitalKey):
            self.dk = dk
        elif dk is True or dk is None:
            self.init_dk()
        else:
            pass

        if isinstance(nucapp, NucApp):
            self.nucapp = nucapp
        elif nucapp is True or nucapp is None:
            self.nucapp = NucApp(self.tc_config)
        else:
            self.nucapp = nucapp
        # soa partner
        self.soa_partner = kwargs.get("soa_partner")

    def init_sd_tester(self, **kwargs):
        '''
        实例
        @param cfg:
        @return:
        '''
        try:
            self.sd_test_obj = Sd_Tester(**self.tc_config)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ecuinterface.py")
            self.sd_test_obj = None
            logger.error(f"sd_tester 实例失败：{str(e)}")

    def start_sd_tester(self, **kwargs):
        '''
        启动 sd_tester
        @return:
        '''
        doipid = kwargs.get('doipid', 0x1002)
        if self.sd_test_p_start_flag:
            return
        #
        try:
            self.sd_test_obj.diagnostic_client_sim_start()
            time.sleep(0.2)
            self.sd_test_obj.tester_present()
            time.sleep(1)
            self.update_serverdoipid(doipid)
            self.sd_test_p_start_flag = True
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ecuinterface.py")
            self.sd_test_obj = None
            logger.error(f"sd_tester 启动失败：{str(e)}")
            self.sd_test_p_start_flag = False

    def stop_sd_tester(self):
        '''
        停止
        @return:
        '''
        self.sd_test_p_start_flag = True
        try:
            self.sd_test_obj.diagnostic_client_sim_close()
            self.sd_test_obj.stop_tester_present()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ecuinterface.py")
            logger.warning(f"sd_tester 停止：{str(e)}")
            self.sd_test_obj = None
        time.sleep(1)

    def update_serverdoipid(self, doipid):
        '''
        更新逻辑地址
        @param doipid:
        @return:
        '''

        try:
            self.sd_test_obj.update_serverdoipid(doipid)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ecuinterface.py")
            self.sd_test_obj = None
            logger.error(f"sd_tester update_serverdoipid 失败：{str(e)}")

    def init_ipdu(self):
        try:
            set_sig_auto(self.cls_path)
            self.ipdu = ISignalIPdu(cls_path=self.cls_path, dut_ecu=self.dut_ecu)
            self.busapp = BusApp(self.ipdu, **self.tc_config)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ecuinterface.py")
            logger.error(f"ipdu 启动失败：{str(e)}")
            self.ipdu = None
            self.busapp = None

    def start_ipdu(self):
        '''
        模拟发送数据
        @return:
        '''
        if self.ipdu_start_flag:
            return
        try:
            self.ipdu.start_all_time_control()  # 启动数据模拟（数据库周期性报文和调度表）
            self.busapp.start_all_cyclic_msg()  # 启动 can lin fr 驱动，总线开始收发报文
            self.ipdu_start_flag = True
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ecuinterface.py")
            logger.error(f"start ipdu 失败：{str(e)}")
            self.ipdu_start_flag = False

    def stop_ipdu(self):
        '''
        亭停止发送数据
        @return:
        '''
        self.ipdu_start_flag = False
        try:
            self.ipdu.time_control_stop()  # 停止数据模拟（数据库周期性报文和调度表）
            self.busapp.stop_all_cyclic_msgs()  # 停止 can lin fr 驱动，停止在总线收发报文
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ecuinterface.py")
            logger.error(f"stop ipdu 失败：{str(e)}")

    def init_io(self):
        '''
        初始化io
        @return:
        '''
        try:
            self.io_obj = IOSystem(self.tc_config)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ecuinterface.py")
            logger.error(f"io_obj 启动失败：{str(e)}")
            self.io_obj = None

    def close_io(self):
        '''
        关闭io串口
        @return:
        '''
        try:
            self.io_obj.close()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ecuinterface.py")
            logger.error(f"io_obj 关闭失败：{str(e)}")
            self.io_obj = None

    def init_dk(self):
        '''
        初始化数字钥匙
        @return:
        '''
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io_obj, self.tc_config)

    def close_dk(self):
        try:
            self.dk.stop_listen_dk_bgm_response()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ecuinterface.py")
            logger.warning(str(e))

    def close(self):

        self.close_dk()
        self.close_io()

    # ############################# usage 模式 诊断切换切换#####################
    def change_usage_mode_by_uds_and_check_status(self, usage_mode, do_assert=True, **kwargs):
        '''
        诊断切换 usage_mode，校验状态
        @param usage_mode:
        @return:
        '''
        #
        if self.ipdu_p is None:
            self.start_ipdu()
        if self.sd_test_p is None:
            self.start_sd_tester()

        timeout = kwargs.get('timeout', 5)
        vehmtnst_value = kwargs.get('vehmtnst_value', 3)
        #
        self.set_vehmtnst_status(vehmtnst_value)
        time.sleep(1)
        keep_usage = kwargs.get('keep_usage', True)
        # 切换 usage 模式
        self.sd_test_obj.change_usage_mode(usage_mode, do_assert=do_assert, **kwargs)
        # 校验
        result, realvalue, expectedvalue = self.check_usage_mode_status(expectedmode=usage_mode, do_assert=do_assert,
                                                                        **kwargs)
        logger.info(f"获取当前模式是{USAGE_MODE_MAP.get(realvalue)} 期望是{USAGE_MODE_MAP.get(expectedvalue)}")
        # 要先校验 才能停止
        if not keep_usage:
            self.stop_sd_tester()
        return result, realvalue, expectedvalue

    def check_usage_mode_status(self, expectedmode, do_assert=True, **kwargs):
        '''
        校验 usage 状态
        @param expectedmode:
        @param do_assert:
        @param timeout:
        @param kwargs:
        @return:
        '''
        timeout = kwargs.get('timeout', 5)
        msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.bodycan.CEMBodyFr12)
        signal_name = kwargs.get('signal_name', 'VehModMngtGlbSafe1UsgModSts_3_CEMBodySignalIPdu12')

        result, realvalue, expectedvalue = self.ipdu.check(msg_signals_obj=msg_signals_obj,
                                                           signal_name=signal_name,
                                                           sig_value_name=expectedmode,
                                                           do_assert=do_assert, timeout=timeout, )

        return result, realvalue, expectedvalue

    def change_usage_mode_to_abandoned(self, **kwargs):
        '''
        诊断切换到 ABANDONED
        @return:
        '''
        keep_usage = kwargs.get('keep_usage', True)
        timeout = kwargs.get('timeout', 5)
        vehmtnst_value = kwargs.get('vehmtnst_value', 3)
        result, realvalue, expectedvalue = self.change_usage_mode_by_uds_and_check_status(UsageMode.ABANDONED,
                                                                                          do_assert=False, **kwargs)
        logger.info(F"切换到 ABANDONED {'成功' if result else '失败'}")
        assert result, f"切换到 ABANDONED 失败 最终是 {realvalue}"

    def change_usage_mode_to_inactive(self, **kwargs):
        '''
        诊断切换到 INACTIVE
        @return:
        '''
        keep_usage = kwargs.get('keep_usage', True)
        timeout = kwargs.get('timeout', 5)
        vehmtnst_value = kwargs.get('vehmtnst_value', 3)
        result, realvalue, expectedvalue = self.change_usage_mode_by_uds_and_check_status(UsageMode.INACTIVE,
                                                                                          do_assert=False, **kwargs)
        logger.info(F"切换到 INACTIVE {'成功' if result else '失败'}")
        assert result, f"切换到 INACTIVE 失败 最终是 {realvalue}"

    def change_usage_mode_to_active(self, **kwargs):
        '''
        诊断切换到 ACTIVE
        @return:
        '''
        keep_usage = kwargs.get('keep_usage', True)
        timeout = kwargs.get('timeout', 5)
        vehmtnst_value = kwargs.get('vehmtnst_value', 3)

        result, realvalue, expectedvalue = self.change_usage_mode_by_uds_and_check_status(UsageMode.ACTIVE,
                                                                                          do_assert=False, **kwargs)
        logger.info(F"切换到 ACTIVE {'成功' if result else '失败'}")
        assert result, f"切换到 ACTIVE 失败 最终是 {realvalue}"

    def change_usage_mode_to_conveniene(self, **kwargs):
        '''
        诊断切换到 CONVENIENCE
        @return:
        '''
        keep_usage = kwargs.get('keep_usage', True)
        timeout = kwargs.get('timeout', 5)
        vehmtnst_value = kwargs.get('vehmtnst_value', 3)

        result, realvalue, expectedvalue = self.change_usage_mode_by_uds_and_check_status(UsageMode.CONVENIENCE,
                                                                                          do_assert=False, **kwargs)
        logger.info(F"切换到 CONVENIENCE {'成功' if result else '失败'}")
        assert result, f"切换到 CONVENIENCE 失败 最终是 {realvalue}"

    def change_usage_mode_to_driving(self, **kwargs):
        '''
        诊断切换到 DRIVING
        @return:
        '''
        keep_usage = kwargs.get('keep_usage', True)
        timeout = kwargs.get('timeout', 5)
        vehmtnst_value = kwargs.get('vehmtnst_value', 3)
        result, realvalue, expectedvalue = self.change_usage_mode_by_uds_and_check_status(UsageMode.DRIVING,
                                                                                          do_assert=False, **kwargs)
        logger.info(F"切换到 DRIVING {'成功' if result else '失败'}")
        assert result, f"切换到 DRIVING 失败 最终是 {realvalue}"

    ############################# 非诊断切换#################

    # #############################car 模式切换#####################

    def check_car_mode_status(self, expectedmode, do_assert=True, **kwargs):
        '''
        校验 car 状态
        @param expectedmode:
        @param do_assert:
        @param timeout:
        @param kwargs:
        @return:
        '''
        timeout = kwargs.get('timeout', 5)
        msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.bodycan.CEMBodyFr12)
        signal_name = kwargs.get('signal_name', 'VehModMngtGlbSafe1CarModSts1_3_CEMBodySignalIPdu12')

        result, realvalue, expectedvalue = self.ipdu.check(msg_signals_obj=msg_signals_obj,
                                                           signal_name=signal_name,
                                                           sig_value_name=expectedmode,
                                                           do_assert=do_assert, timeout=timeout, )
        return result, realvalue, expectedvalue

    def change_car_mode_by_uds_and_check_status(self, car_mode, do_assert=True, **kwargs):
        '''
        诊断切换 usage_mode，校验状态
        @param usage_mode:
        @return:
        '''
        if self.ipdu_p is None:
            self.start_ipdu()
        if self.sd_test_p is None:
            self.start_sd_tester()
        timeout = kwargs.get('timeout', 5)
        vehmtnst_value = kwargs.get('vehmtnst_value', 3)
        keep_car = kwargs.get('keep_car', True)
        #
        self.set_vehmtnst_status(vehmtnst_value)
        time.sleep(0.5)
        # 切换 usage 模式
        self.sd_test_obj.change_car_mode(car_mode, do_assert=do_assert, **kwargs)
        # 校验
        result, realvalue, expectedvalue = self.check_car_mode_status(expectedmode=car_mode, do_assert=do_assert,
                                                                      **kwargs)
        # 要先校验 才能停止
        if not keep_car:
            self.stop_sd_tester()
        return result, realvalue, expectedvalue

    def change_car_mode_to_normal(self, **kwargs):
        '''
        诊断切换到 NORMAL
        @return:
        '''
        keep_car = kwargs.get('keep_car', True)
        timeout = kwargs.get('timeout', 5)
        vehmtnst_value = kwargs.get('vehmtnst_value', 3)
        result, realvalue, expectedvalue = self.change_car_mode_by_uds_and_check_status(CarMode.NORMAL,
                                                                                        do_assert=False, **kwargs)
        logger.info(F"切换到 NORMAL {'成功' if result else '失败'}")
        assert result, f"切换到 NORMAL 失败 最终是 {realvalue}"

    def change_car_mode_to_transport(self, **kwargs):
        '''
        诊断切换到 TRANSPORT
        @return:
        '''
        keep_car = kwargs.get('keep_car', True)
        timeout = kwargs.get('timeout', 5)
        vehmtnst_value = kwargs.get('vehmtnst_value', 3)
        result, realvalue, expectedvalue = self.change_car_mode_by_uds_and_check_status(CarMode.TRANSPORT,
                                                                                        do_assert=False, **kwargs)
        logger.info(F"切换到 TRANSPORT {'成功' if result else '失败'}")
        assert result, f"切换到 TRANSPORT 失败 最终是 {realvalue}"

    def change_car_mode_to_factory(self, **kwargs):
        '''
        诊断切换到 FACTORY
        @return:
        '''
        keep_car = kwargs.get('keep_car', True)
        timeout = kwargs.get('timeout', 5)
        vehmtnst_value = kwargs.get('vehmtnst_value', 3)
        result, realvalue, expectedvalue = self.change_car_mode_by_uds_and_check_status(CarMode.FACTORY,
                                                                                        do_assert=False,
                                                                                        **kwargs)
        logger.info(F"切换到 FACTORY {'成功' if result else '失败'}")
        assert result, f"切换到 FACTORY 失败 最终是 {realvalue}"

    def change_car_mode_to_crash(self, **kwargs):
        '''
        诊断切换到 CRASH
        @return:
        '''
        keep_car = kwargs.get('keep_car', True)
        timeout = kwargs.get('timeout', 5)
        vehmtnst_value = kwargs.get('vehmtnst_value', 3)
        result, realvalue, expectedvalue = self.change_car_mode_by_uds_and_check_status(CarMode.CRASH,
                                                                                        do_assert=False, **kwargs)
        logger.info(F"切换到 CRASH {'成功' if result else '失败'}")
        assert result, f"切换到 CRASH 失败 最终是 {realvalue}"

    def change_car_mode_to_dyno(self, **kwargs):
        '''
        诊断切换到 DYNO
        @return:
        '''

        keep_car = kwargs.get('keep_car', True)
        timeout = kwargs.get('timeout', 5)
        vehmtnst_value = kwargs.get('vehmtnst_value', 3)
        result, realvalue, expectedvalue = self.change_car_mode_by_uds_and_check_status(CarMode.DYNO,
                                                                                        do_assert=False, **kwargs)
        logger.info(F"切换到 DYNO {'成功' if result else '失败'}")
        assert result, f"切换到 DYNO 失败 最终是 {realvalue}"

    def set_vehmtnst_status(self, value=3, **kwargs):
        '''
        value = {'VehMtnSt2_Ukwn': 0, 'VehMtnSt2_StandStillVal1': 1, 'VehMtnSt2_StandStillVal2': 2,
                'VehMtnSt2_StandStillVal3': 3, 'VehMtnSt2_RollgFwdVal1': 4, 'VehMtnSt2_RollgFwdVal2': 5,
                'VehMtnSt2_RollgBackwVal1': 6, 'VehMtnSt2_RollgBackwVal2': 7
        }

        @param value:
        @return:
        '''
        ipdu = kwargs.get("ipdu", self.ipdu)
        value_list = {'VehMtnSt2_Ukwn': 0, 'VehMtnSt2_StandStillVal1': 1, 'VehMtnSt2_StandStillVal2': 2,
                      'VehMtnSt2_StandStillVal3': 3, 'VehMtnSt2_RollgFwdVal1': 4, 'VehMtnSt2_RollgFwdVal2': 5,
                      'VehMtnSt2_RollgBackwVal1': 6, 'VehMtnSt2_RollgBackwVal2': 7
                      }
        dic = dict(zip(list(value_list.values()), list(value_list.keys())))

        logger.info(f"set vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00 ==>>{dic.get(value)}")
        if value == 0:
            ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_ukwn()
        elif value == 1:
            ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval1()
        elif value == 2:
            ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval2()
        elif value == 3:
            ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        elif value == 4:
            ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_rollgfwdval1()
        elif value == 5:
            ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_rollgfwdval2()
        elif value == 6:
            ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_rollgbackwval1()
        elif value == 7:
            ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_rollgbackwval2()
        else:
            logger.warning(f"该模式{value}不存在")
            pass

    def check_driver_door_status(self, sig_value, **kwargs):
        '''
        校验 driver_door 的状态
        @param sig_value: {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        @param kwargs:
        @return:
        '''
        # DoorDrvrSts_2_CemBodySignalIPdu02
        msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.bodycan.CemBodyFr02)
        signal_name = kwargs.get('signal_name', 'DoorDrvrSts_2_CemBodySignalIPdu02')
        do_assert = kwargs.get('do_assert', False)
        timeout = kwargs.get('timeout', 5)

        result, realvalue, expectedvalue = self.ipdu.check(msg_signals_obj,
                                                           signal_name, sig_value, do_assert=do_assert,
                                                           timeout=timeout)
        if not result:
            logger.error(f" driver_door bodycan.CemBodyFr02 的 DoorSts 是{realvalue}，期望应该是{sig_value}")
        return result, realvalue, expectedvalue

    def check_passager_door_status(self, sig_value, **kwargs):
        '''
        校验 passager_door 的状态
        @param sig_value: {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        @param kwargs:
        @return:
        '''
        msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.bodycan.CEMBodyFr11)
        signal_name = kwargs.get('signal_name', 'DoorPassSts_2_CEMBodySignalIPdu11')
        do_assert = kwargs.get('do_assert', False)
        timeout = kwargs.get('timeout', 5)

        result, realvalue, expectedvalue = self.ipdu.check(msg_signals_obj,
                                                           signal_name, sig_value, do_assert=do_assert,
                                                           timeout=timeout)
        if not result:
            logger.error(f" passager_door bodycan.CEMBodyFr11 的 DoorSts 是{realvalue}，期望应该是{sig_value}")
        return result, realvalue, expectedvalue

    def check_lere_door_status(self, sig_value, **kwargs):
        '''
        校验 lere_door 的状态
        @param sig_value: {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        @param kwargs:
        @return:
        '''
        msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.bodycan.CemBodyFr02)
        signal_name = kwargs.get('signal_name', 'DoorLeReSts_1_CemBodySignalIPdu02')
        do_assert = kwargs.get('do_assert', False)
        timeout = kwargs.get('timeout', 5)

        result, realvalue, expectedvalue = self.ipdu.check(msg_signals_obj,
                                                           signal_name, sig_value, do_assert=do_assert,
                                                           timeout=timeout)
        if not result:
            logger.error(f" lere_door bodycan.CemBodyFr02 的 DoorSts 是{realvalue}，期望应该是{sig_value}")
        return result, realvalue, expectedvalue

    def check_rire_door_status(self, sig_value, **kwargs):
        '''
        校验 rire_door 的状态
        @param sig_value: {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        @param kwargs:
        @return:
        '''
        msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.bodycan.CEMBodyFr11)
        signal_name = kwargs.get('signal_name', 'DoorRiReSts_1_CEMBodySignalIPdu11')
        do_assert = kwargs.get('do_assert', False)
        timeout = kwargs.get('timeout', 5)

        result, realvalue, expectedvalue = self.ipdu.check(msg_signals_obj,
                                                           signal_name, sig_value, do_assert=do_assert,
                                                           timeout=timeout)
        if not result:
            logger.error(f" rire_door bodycan.CEMBodyFr11 的 DoorSts 是{realvalue}，期望应该是{sig_value}")
        return result, realvalue, expectedvalue

    def check_trunk_status(self, sig_value, **kwargs):
        '''
        校验 行李箱 的状态
        @param sig_value: {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        @param kwargs:
        @return:
        '''

        msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.bodycan.CEMBodyFr11)
        signal_name = kwargs.get('signal_name', 'TrSts_2_CEMBodySignalIPdu11')
        do_assert = kwargs.get('do_assert', False)
        timeout = kwargs.get('timeout', 5)

        result, realvalue, expectedvalue = self.ipdu.check(msg_signals_obj,
                                                           signal_name, sig_value, do_assert=do_assert,
                                                           timeout=timeout)
        if not result:
            logger.error(f" tr_door bodycan.CEMBodyFr11 的 DoorSts 是{realvalue}，期望应该是{sig_value}")
        return result, realvalue, expectedvalue

    def check_hood_status(self, sig_value, **kwargs):
        '''
        校验 引擎盖 的状态
        @param sig_value: {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        @param kwargs:
        @return:
        '''
        # self.connectivitycanfd.VgmConnFr04
        msg_signals_obj = kwargs.get('msg_signals_obj', self.ipdu.backbonefr.CemBackBoneFr06)
        signal_name = kwargs.get('signal_name', 'HoodSts')
        do_assert = kwargs.get('do_assert', False)
        timeout = kwargs.get('timeout', 5)

        result, realvalue, expectedvalue = self.ipdu.check(msg_signals_obj,
                                                           signal_name, sig_value, do_assert=do_assert,
                                                           timeout=timeout)
        if not result:
            logger.error(f" tr_door backbonefr.CemBackBoneFr06 的 DoorSts 是{realvalue}，期望应该是{sig_value}")
        return result, realvalue, expectedvalue

    def set_cenlock_lock(self):
        '''
        中控锁 上锁
        @return:
        '''
        self.dk.set_cenlock_sts(3)

    def set_cenlock_unlock(self):
        '''
        中控锁  解锁
        @return:
        '''
        self.dk.set_cenlock_sts(1)

    def set_usage_mode_to_abandoned(self, enter_aband_time=10 * 60, do_assert=True, **kwargs):
        '''
        进入 abandoned 模式
        断开诊断激活线后若是 想快速进入 则 enter_aband_time=0 会上下电 bgm
        如果想正常进入 则需要等待一定时间 默认 10min

        @param enter_aband_time:  关闭四门两盖以后，中控锁上锁后，最长等待时间
        @param do_assert: 为true   进入失败则会报错，为False 则不会报错，返回当前模式
        @param kwargs:
        @return:
        '''
        # tcam 是否休眠
        tcam_sleep = kwargs.get("tcam_sleep", True)
        nucapp = kwargs.get("nucapp", self.nucapp)
        io = kwargs.get("io", self.io_obj)
        ipdu = kwargs.get("ipdu", self.ipdu)
        lin_channel = kwargs.get("lin_channel", "cem_lin6")
        lin_id = kwargs.get("lin_id", 0x06)
        lin_msg = kwargs.get("lin_msg", [0x0, 0x7c, 0xc8, 0xff, 0xff, 0xff, 0xff])

        # 3. 四门两盖关闭
        logger.info("关闭四门两盖")
        io.drvr_door_close()
        io.lere_door_close()
        io.pass_door_close()
        io.rire_door_close()
        io.trunk_door_close()
        io.hood_door1_close()
        # 四门两盖是否关闭
        self.check_driver_door_status(2)
        self.check_passager_door_status(2)
        self.check_lere_door_status(2)
        self.check_rire_door_status(2)
        self.check_trunk_status(2)
        self.check_hood_status(2)

        # 1 断开诊断激活线
        logger.info("断开诊断激活线")
        nucapp.bgm_diag_line_down()
        nucapp.bgm_diag_line_down()
        # tcam kl15 线断开
        if tcam_sleep:
            nucapp.tcam_kl15_down()
            nucapp.tcam_kl15_down()
        if not enter_aband_time:
            nucapp.bgm_power_off()
            time.sleep(3)
            nucapp.bgm_power_on()
            time.sleep(20)
            # 2 发送lin 报文 补电
            self.ipdu.set(self.ipdu.cem_lin6.CemCem_Lin6Fr02, "BattSnsrStReq", 1)
            ipdu.send_pdu(lin_channel, lin_id, lin_msg)
            enter_aband_time = 10 * 60
        else:
            # 2 发送lin 报文 补电
            self.ipdu.set(self.ipdu.cem_lin6.CemCem_Lin6Fr02, "BattSnsrStReq", 1)
            ipdu.send_pdu(lin_channel, lin_id, lin_msg)
            logger.info(f"未上下电，需要等待{enter_aband_time}秒")
            # time.sleep(enter_aband_time)

        # 4. 解锁 闭锁
        self.set_cenlock_lock()
        # 过滤中间的一次跳变，要加延时，否则会误收报文
        time.sleep(5)
        # 清除缓存
        self.ipdu.rx_flag_reset_all()
        # 等待一定时间
        logger.info(f"最长等待{enter_aband_time}秒,让 bgm 进入abandoned 模式，超过时间未进入则退出")
        t1 = time.time()
        realvalue = None
        while time.time() - t1 < enter_aband_time:
            result, realvalue, expectedvalue = self.check_usage_mode_status(expectedmode=UsageMode.ABANDONED,
                                                                            do_assert=False)
            logger.info(f"当前模式为{USAGE_MODE_MAP.get(realvalue)}期望模式为{USAGE_MODE_MAP.get(expectedvalue)}")
            #
            if result:
                # 进入
                logger.info(f"成功进入 abandoned 状态耗时{time.time() - t1}s")
                return True
        else:
            if do_assert:
                assert 0, "进入abandoned  失败"
            return False

    def partner_change_mode(self, method_name, method_par, **kwargs):
        '''
        通过服务切换 模式
        @param method_name:
        @param method_par:
        @param kwargs:
        @return:
        '''
        try:
            # S2sBaseClass = kwargs.get('soa_partner', self.soa_partner)
            # Service = kwargs.get("Service", [("VehicleModeService", "client")])
            # # self.partner = S2sBaseClass(Service)
            # self.partner = S2sBaseClass([("VehicleModeService", "client")])
            self.partner = self.soa_partner
            self.partner.send_method_request(
                'VehicleModeService_client',
                method_name,
                method_par,
            )
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ecuinterface.py")
            logger.error(f"{method_name} 服务调用失败>>{str(e)}")
        # try:
        #     self.partner.stop_operators()
        # except Exception as e:
        #     logger.info(f"{str(e)}")

    def s2s_change_usage_mode_and_check_result(self, usage_mode, do_assert=True, **kwargs):
        '''
        通过s2s 切换 car mode
        '''
        # 先获取下 当前模式
        # curren_usage_mode = self.get_usage_mode_by_soa(**kwargs)
        result, curren_usage_mode, expectedvalue = self.check_usage_mode_status(expectedmode=usage_mode,
                                                                                do_assert=False)
        curr_usage_mode_name = USAGE_MODE_MAP.get(curren_usage_mode)
        logger.info(f"当前模式为 为{curr_usage_mode_name}:{curren_usage_mode}")
        if curren_usage_mode < usage_mode:
            method_name = "SetUsageModeUp"
        elif curren_usage_mode > usage_mode:
            method_name = "SetUsageModeDown"
        else:
            # 已经是所需要模式，无需切换，直接返回
            return 1, curren_usage_mode, curren_usage_mode
        # 如果切到driving 模式以后 不设置为0 则切不成功
        self.ipdu.backbonefr_vddmbackbonefr00_engst1wdstsengst1wdsts_engst1_ini()
        # 设置 同星信号
        self.set_vehmtnst_status(3)
        usage_mode_name = USAGE_MODE_MAP.get(usage_mode)
        logger.info(f"设置usage_mode_name 为{usage_mode_name}:{usage_mode}")
        logger.info(f"Step:调用 {method_name}(mode:{usage_mode}))")

        method_par = {"mode": usage_mode}
        self.partner_change_mode(method_name, method_par)

        logger.info(f"验证切换结果是否为{usage_mode_name}:{usage_mode}")
        result, realvalue, expectedvalue = self.check_usage_mode_status(expectedmode=usage_mode, do_assert=False)

        string = f" 切换前为{curr_usage_mode_name}，切换后本应为 {USAGE_MODE_MAP.get(usage_mode)} 实际为 {USAGE_MODE_MAP.get(realvalue)}"
        logger.info(string)
        if do_assert and not result:
            string = f" 本应为 {USAGE_MODE_MAP.get(usage_mode)} 实际为 {USAGE_MODE_MAP.get(realvalue)}"
            logger.error(string)
            assert 0, string
        return result, realvalue, expectedvalue

    def set_usage_mode_to_inactivate(self):
        '''
        服务切换 到 inactivate 状态
        @return:
        '''
        self.s2s_change_usage_mode_and_check_result(UsageMode.INACTIVE)

    def set_usage_mode_to_convenience(self):
        '''
        服务切换 到 convenience 状态
        @return:
        '''
        self.s2s_change_usage_mode_and_check_result(UsageMode.CONVENIENCE)

    def set_usage_mode_to_activate(self):
        '''
        服务切换 到 activate 状态
        @return:
        '''
        self.s2s_change_usage_mode_and_check_result(UsageMode.ACTIVE)

    def set_usage_mode_to_driving(self):
        '''
        服务切换 到 driving 状态
        @return:
        '''
        self.s2s_change_usage_mode_and_check_result(UsageMode.ACTIVE)
        self.ipdu.backbonefr_vddmbackbonefr00_engst1wdstsengst1wdsts_engst1_runngrunng()
        self.check_usage_mode_status(UsageMode.DRIVING)

    def init_set_usage_mode(self, **kwargs):
        '''
        寻钥匙
        @return:
        '''

        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_internal_has_key()
        self.set_cenlock_lock()
        self.set_cenlock_unlock()

    def init_network_sleep(self, **kwargs):
        '''
        寻钥匙
        @return:
        '''
        #  暂停发送报文
        self.ipdu.pause_all_bus_send()
        # sleep(2)
        self.ipdu.backbonefr_bcmvddmbackbonefr06_vehspdlgta_0_bcmvddmbackbonesignalipdu06_value(0)
        self.ipdu.backbonefr_vddmbackbonefr18_trsmparklockdtrsmparklockd_trsmparklock1_parkengd()
        self.ipdu.backbonefr_vddmbackbonefr03_gearlvrindcn_gearlvrindcn2_parkindcn()

        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        # self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4})
        # self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下

    def enter_network_sleep(self, enter_aband_time=10 * 60, do_assert=False, **kwargs):
        '''
        进入休眠状态，进入 ABANDONED 状态后  ，诶呦报文发出，只是网络休眠，因没有程控电源，所以无法判断电流
        断开诊断激活线后若是 想快速进入 则 enter_aband_time=0 会上下电 bgm
        如果想正常进入 则需要等待一定时间 默认 10min

        @param kwargs:
        @return:
        '''
        time_delay = kwargs.get("time_delay", 40)
        self.ipdu.pause_all_bus_send()
        time.sleep(1)
        # try:
        #     self.init_sleep()
        # except Exception as e:
        #     logger.warning("init_sleep 失败")
        # 先进入 ABANDONED
        ret = self.set_usage_mode_to_abandoned(enter_aband_time=enter_aband_time, do_assert=do_assert)
        if not ret:
            if do_assert:
                assert 0, "bgm 未进入 ABANDONED状态"
            logger.info(f"未进入 ABANDONED状态 ,检查环境，确认下，bodycan 是否能收到报文")
            return 0

        logger.info(f"bgm 进入 ABANDONED 状态后延时{time_delay}")
        time.sleep(time_delay)
        # 判断 通道 有么有报文
        ret = self.check_all_channel_recv_no_msg(**kwargs)
        if do_assert and not ret:
            assert 0, "bgm 未休眠，进入可以收到报文"
        return ret

    def check_all_channel_recv_no_msg(self, **kwargs):
        '''
        接收所有通道
        @param kwargs:
        @return:
        '''
        all_bus = self.tc_config.get('bus', None)
        print('all_bus', all_bus)
        # lin 通道
        lin_channel_list = ["cem_lin1", "cem_lin2", "cem_lin3", "cem_lin4", "cem_lin5", "cem_lin6"]
        # can 通道
        can_channel_list = ["bodycan", "propulsioncan", "chassiscan1", "chassiscan2", "passivesafetycan",
                            "diagnosticcan", "infocanfd", "adcanfd", "bodyalmcanfd1", "connectivitycanfd",
                            "bodyexposedcanfd", "bodyalmcanfd2"
                            ]
        fr_channel_list = ['backbonefr']
        all_channel = lin_channel_list + can_channel_list + fr_channel_list

        if all_bus:
            all_channel = [i for i in list(all_bus.keys()) if 'can' in i or 'lin' in i or 'backbonefr' in i]

        # 清除缓存
        self.ipdu.rx_flag_reset_all()
        err_list = []
        for channel in all_channel:
            # logger.info(f"{channel} 开始接收报文")
            try:
                msgs = self.ipdu.check_bus_recv_message(channel)
                string = ''
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/ecuinterface.py")
                msgs = ""
                string = str(e)
            logger.info(f"{channel} 通道{'本不应接收到报文，实际' if msgs else '未'}接收报文 {string}")
            if msgs:
                err_list.append(channel)
        if len(err_list):
            logger.error(f"本不应接收到报文，{err_list}通道接收到报文")
            return False
        return True

    def set_car_mode_to_exhibition(self, **kwargs):
        '''
        服务切换展车模式
        @return:
        '''
        ipdu = kwargs.get('ipdu', self.ipdu)
        if ipdu:
            ipdu.set(
                ipdu.backbonefr.BcmVddmBackBoneFr00,
                'EpbStsEpbSts',
                3,
            )
            time.sleep(1)

        method_name = "SetExhibitionMode"
        method_par = {"isOpen": True}
        self.partner_change_mode(method_name, method_par)
        # 校验 展车模式
        ret = self.check_car_mode_exhibition(exhibition=True)
        return ret

    def set_car_mode_to_unexhibition(self, **kwargs):
        '''
        服务切非换展车模式
        @return:
        '''
        ipdu = kwargs.get('ipdu', self.ipdu)
        if ipdu:
            ipdu.set(
                ipdu.backbonefr.BcmVddmBackBoneFr00,
                'EpbStsEpbSts',
                3,
            )
            time.sleep(1)
        method_name = "SetExhibitionMode"
        method_par = {"isOpen": False}
        self.partner_change_mode(method_name, method_par)
        # 校验 非展车模式
        ret = self.check_car_mode_exhibition(exhibition=False)
        return ret

    def check_car_mode_exhibition(self, exhibition=True, do_assert=True, **kwargs):
        '''
        exhibition 为 True 校验 当前模式，验当前是展车模式，
        exhibition 为 False 校验 当前模式，验当前是非展车模式，

        @return: 返回 True 是展车模式，False 不是展车模式
        '''
        ipdu = kwargs.get('ipdu', self.ipdu)
        if ipdu:
            ipdu.set(
                ipdu.backbonefr.BcmVddmBackBoneFr00,
                'EpbStsEpbSts',
                3,
            )
            time.sleep(1)
        if exhibition:
            ck_info = {'out': {'isOpen': True, 'isValid': True}}
        else:
            ck_info = {'out': {'isOpen': False, 'isValid': True}}

        method_name = 'GetExhibitionModeSts'
        ret = self.partner.send_request_and_ck_resp(
            'VehicleModeService_client',
            method_name,
            {}, ck_info=ck_info
        )
        logger.info(f"VehicleModeService ck_info={ck_info}       ret={ret}")
        if exhibition:
            logger.info(F"当前为  {'展车模式' if ret else '非展车模式'}")
        else:
            logger.info(F"当前为  {'展车模式' if not ret else '非展车模式'}")

        if do_assert and not ret:
            assert 0, "模式不匹配"
        if ret:
            return True
        else:
            return False

    def change_car_mode_to_exhibition(self, do_assert=True, **kwargs):
        '''
        诊断切换到 展车模式
        @return: True 切换成功 False 切换失败
        '''
        if self.ipdu_p is None:
            self.start_ipdu()
        if self.sd_test_p is None:
            self.start_sd_tester()

        result = self.sd_test_obj.set_exhibition_mode(do_assert=False, ipdu=self.ipdu)

        logger.info(F"切换到 展车模式 {'成功' if result else '失败'}")
        if do_assert:
            assert result, f"切换到展车模式失败 "
        return result

    def change_car_mode_to_unexhibition(self, do_assert=True, **kwargs):
        '''
        诊断切换到 非展车模式  退出展模式
        @return: True 切换成功 False 切换失败
        '''
        if self.ipdu_p is None:
            self.start_ipdu()
        if self.sd_test_p is None:
            self.start_sd_tester()

        result = self.sd_test_obj.set_unexhibition_mode(do_assert=False, ipdu=self.ipdu)

        logger.info(F"退出展车模式 {'成功' if result else '失败'}")
        if do_assert:
            assert result, f"退出展车模式失败 "
        return result

    def get_exhibition_mode(self):
        '''
        获取展车模式
        @return: 返回True 是展车模式 False 为非展车模式
        '''
        if self.ipdu_p is None:
            self.start_ipdu()
        if self.sd_test_p is None:
            self.start_sd_tester()

        result = self.sd_test_obj.get_exhibition_mode(do_assert=False, ipdu=self.ipdu)

        logger.info(F"当前为  {'展车模式' if result else '非展车模式'}")
        return result

    def set_lock_unlock(self, value, do_assert=True, **kwargs):
        '''
        中控锁接闭锁
        @param value: 1 解锁，3上锁
        @param do_assert:
        @param kwargs:
        @return:
        '''

        io = kwargs.get("io", self.io_obj)
        # 获取中控锁状态
        # sig_value_table = {'LockSt3_LockUndefd': 0, 'LockSt3_LockUnlckd': 1, 'LockSt3_LockTrUnlckd': 2, 'LockSt3_LockLockd': 3}
        curr_sts = self.ipdu.get_recent_signal_raw_value(self.ipdu.connectivitycanfd.VgmConnFr12,'LockgCenStsLockSt_2_VgmConnSignalIPdu12')
        logger.info(f"当前中控锁的状态为:{curr_sts},期望为{value}")
        if curr_sts == value:
            return True
        # 3. 四门两盖关闭
        logger.info("关闭四门两盖")
        io.drvr_door_close()
        io.lere_door_close()
        io.pass_door_close()
        io.rire_door_close()
        io.trunk_door_close()
        io.hood_door1_close()
        # 四门两盖是否关闭
        self.check_driver_door_status(2)
        self.check_passager_door_status(2)
        self.check_lere_door_status(2)
        self.check_rire_door_status(2)
        self.check_trunk_status(2)
        self.check_hood_status(2)

        # 发送
        if value == 1:
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr08, "DoorOpenerDrvrSts_2_VgmConnSignalIPdu08", 5)
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr08, "DoorOpenerPassSts_2_VgmConnSignalIPdu08", 5)
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr08, "DoorOpenerLeReSts_2_VgmConnSignalIPdu08", 5)
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr08, "DoorOpenerRiReSts_2_VgmConnSignalIPdu08", 5)

            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr08, "DoorDrvrLockSts_2_VgmConnSignalIPdu08", 1)
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr08, "DoorPassLockSts_2_VgmConnSignalIPdu08", 1)
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr08, "DoorLeReLockSts_2_VgmConnSignalIPdu08", 1)
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr08, "DoorRiReLockSts_2_VgmConnSignalIPdu08", 1)
        else:
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr08, "DoorOpenerDrvrSts_2_VgmConnSignalIPdu08", 1)
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr08, "DoorOpenerPassSts_2_VgmConnSignalIPdu08", 1)
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr08, "DoorOpenerLeReSts_2_VgmConnSignalIPdu08", 1)
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr08, "DoorOpenerRiReSts_2_VgmConnSignalIPdu08", 1)

            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr08, "DoorDrvrLockSts_2_VgmConnSignalIPdu08", 2)
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr08, "DoorPassLockSts_2_VgmConnSignalIPdu08", 2)
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr08, "DoorLeReLockSts_2_VgmConnSignalIPdu08", 2)
            self.ipdu.set(self.ipdu.connectivitycanfd.VgmConnFr08, "DoorRiReLockSts_2_VgmConnSignalIPdu08", 2)
        # time.sleep(1)
        self.dk.send_nfc_cmd()
        time.sleep(1)
        curr_sts = self.ipdu.get_recent_signal_raw_value(self.ipdu.connectivitycanfd.VgmConnFr12,'LockgCenStsLockSt_2_VgmConnSignalIPdu12')
        logger.info(f"当前中控锁的状态为:{curr_sts},期望为{value}")
        if curr_sts == value:
            return True
        if do_assert:
            assert 0, f"当前中控锁模式不对，本应为{value}实际为{curr_sts}"
        return False

    def set_lock(self, do_assert=True, **kwargs):
        '''
        整车闭锁
        @param do_assert: 为true   进入失败则会报错，为False 则不会报错，返回当前模式
        @param kwargs:
        @return:
        '''
        self.set_lock_unlock(3, do_assert, **kwargs)

    def set_unlock(self, do_assert=True, **kwargs):
        '''
        整车解锁
        @param do_assert: 为true   进入失败则会报错，为False 则不会报错，返回当前模式
        @param kwargs:
        @return:
        '''
        self.set_lock_unlock(1, do_assert, **kwargs)

