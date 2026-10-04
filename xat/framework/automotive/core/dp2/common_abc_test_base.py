# -*- coding: utf-8 -*-
"""
@File        : common_abc_test_base.py
@Author      : dejian.xiong@jiduauto.com
@Time        : 2022/7/11 11:33
@Description :
@Examples    :
"""
import copy
import inspect
import uuid

from xat_ecu.legacy.interface.nuc_app import partner_process_check

from framework.automotive.utils.data_type import EcuInfo
from xat_ecu.api.call_tracker import ObjExecutor
from xat_ecu.api.abc_interface import *
from framework.automotive.utils.conftest_helper import mkdir_folder, kill_process
from framework.automotive.utils.new_relay_helper import jy_dam0800_check_and_repair
from xat_ecu.api.interfaces.dp2.main_obj import (
    BusComm,
    DiagMock,
    Io,
    LogManagement,
    Mix,
    SdTest,
    Serial,
    Soa,
    Ssh,
    Tsp,
    Mock
)


class CommonABCTestBase:
    @staticmethod
    def change_bench_config(ecu: EcuInfo) -> EcuInfo:
        """子类重写该接口，自定义台架类型为单域、两域或者四域"""
        return ecu

    def before_class_setup(self, ecu: EcuInfo):
        logger.info(inspect.stack()[0].function + ' start!')
        logger.debug("ecu : {}".format(ecu))
        ecu.class_uuid = uuid.uuid4()
        ecu.class_case_fail_flag = False
        ecu.class_bgm_log = {}
        ecu_new = copy.deepcopy(ecu)
        ecu_new = self.change_bench_config(ecu=ecu_new)
        self.tb_config = ecu_new.tb_config
        self.tc_config = ecu_new.tc_config
        self.domain = ecu_new.domain

        self.tc_config.update(self.tb_config)
        wifi_localhost = self.tc_config.get("wifi_localhost")
        logger.info(f"当前在{wifi_localhost}台架上运行")

        self.veh_type = self.tc_config.get("veh_type")
        self.bl_ver = self.tc_config.get("bl_ver")
        if self.veh_type and self.bl_ver:
            self.cls_path = f"sdk/data/{self.veh_type}/can_lin_fr_cls/{self.bl_ver}"
            self.tn_config_path = f"config/{self.veh_type}/{self.bl_ver}/ecu_network.yaml"
        else:
            err_msg = f"Config error : self.veh_type is {self.veh_type}  self.bl_ver is {self.bl_ver}"
            raise exception_error.ConfigError(err_msg)
        # 初始化云端模拟
        self.tsp = Tsp(**self.tc_config)
        # 初始化日志管理
        self.log_manage = LogManagement()
        # 初始化io
        self.io = Io(self.tc_config)
        # 初始化串口
        self.serial = Serial()
        # 初始化诊断仪
        self.sd_tester = SdTest(**self.tc_config)
        # 初始化总线
        self.bus_comm = BusComm(self.cls_path, **self.tc_config)
        self.tc_config["tosun_obj"] = self.bus_comm.bus_app.bus_dict.get("tosun_tc1018")  # 增加同星can实体
        self.tc_config["tosun_fr_obj"] = self.bus_comm.bus_app.bus_dict.get("tosun_tc1034")  # 增加同星fr实体
        # 初始化soa服务
        self.soa = Soa()
        # 初始化ssh
        for key, value in self.domain.items():
            if value:
                domain = key
                break
        else:
            err_msg = 'domain参数获取为None，环境识别失败停止运行'
            logger.error(err_msg)
            raise exception_error.ConfigError(err_msg)
        self.ssh = Ssh(domain=domain)
        logger.info(f"domain:{domain}")
        if ecu_new.disable_env is False:
            pass
        # 初始化诊断
        self.diag_mock = DiagMock(**self.tc_config)
        # 初始化mock
        self.mock = Mock()
        # 混个接口初始化
        self.mix = Mix(
            tsp=self.tsp,
            log_manage=self.log_manage,
            io=self.io,
            serial=self.serial,
            sd_tester=self.sd_tester,
            bus_comm=self.bus_comm,
            soa=self.soa,
            ssh=self.ssh,
            diag_mock=self.diag_mock,
            mock=self.mock
        )
        mkdir_folder()
        self.log_manage.start_record_soa_partner_log()

        self.before_class(self, ecu_new)

    def after_class_teardown(self, ecu: EcuInfo):
        try:
            self.after_class(self, ecu)
            if "power_control_type" in ecu.tb_config:
                if ecu.tb_config.get("power_control_type") == "jydam0800":
                    jy_dam0800_check_and_repair()
        except AttributeError:
            pass
        finally:
            # 执行对象的stop方法，同时销毁存储的对象
            if hasattr(self, 'log_manage'):
                self.log_manage.stop_record_soa_partner_log()
            with ObjExecutor() as obj:
                if "SdTest" in obj.start_cache:
                    try:
                        self.sd_tester.stop_sd_tester()
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/core/dp2/common_abc_test_base.py")
                        logger.warning(f"关闭sd_tester错误，得到：{e}")
                    logger.info("优先关闭 SdTest")
                if "DiagMock" in obj.start_cache:
                    self.diag_mock.all_close()
                    logger.info("优先关闭 DiagMock")
                for obj_name in obj.start_cache:
                    if obj_name == 'BusComm':
                        self.bus_comm.stop_all_cyclic_msgs()  # 停止数据模拟,总线收发报文
                    elif obj_name == 'Io':
                        self.io.stop_io()
                    elif obj_name == 'Soa':
                        self.soa.stop_soa()
                        partner_process_check()
                    elif obj_name == 'Serial':
                        self.serial.stop_serial()
            kill_process('diagd')

    def before_func_setup(self, ecu: EcuInfo):
        wifi_localhost = self.tc_config.get("wifi_localhost")
        logger.info(f"当前在{wifi_localhost}台架上运行")
        if ecu.record_log:
            self.log_manage.start_record_log(case_name=ecu.testname)
        if ecu.trace_log:
            self.bus_comm.start_record_trace_log(file_name=ecu.testname)
        for obj_name in ObjExecutor().start_cache:
            if obj_name == 'BusComm':
                self.bus_comm.bus_app.check_tosun_process()
        self.before_each_func(ecu)

    def after_func_teardown(self, ecu: EcuInfo):
        try:
            self.after_each_func(ecu)
        finally:
            if ecu.class_uuid:
                logger.info(f"当前用例所在class的日志可以在/root/fail_case_log/{ecu.class_uuid}目录下查看")
            if ecu.record_log:
                jet_path = self.log_manage.stop_record_log()
                ecu.log_path['jet_log'] = jet_path
            partner_log = self.log_manage.stop_record_soa_partner_log()
            ecu.log_path['parter_log'] = partner_log
            if ecu.trace_log:
                if ecu.testresult == 'Pass':
                    self.bus_comm.stop_record_trace_log(is_record_status=False)
                else:
                    # 只有失败的case才将trace放在allure报告上作为附件
                    trace_path = self.bus_comm.stop_record_trace_log()
                    ecu.log_path['trace_log'] = trace_path
                    self.bus_comm.bus_app.check_tosun_trace()

    def before_class(self, ecu: EcuInfo):
        pass

    def before_each_func(self, ecu: EcuInfo):
        pass

    def after_each_func(self, ecu: EcuInfo):
        pass

    def after_class(self, ecu: EcuInfo):
        pass
