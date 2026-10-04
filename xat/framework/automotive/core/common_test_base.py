# -*- coding: utf-8 -*-
"""
@File        : common_test_base.py
@Author      : jinhui.zhao@jiduauto.com
@Time        : 2022/7/11 11:33
@Description :
@Examples    :
"""

import os, sys
import uuid

from xat_ecu.legacy.sdk.sdk_tools import get_pdu_value_and_time

from framework.automotive.utils.conftest_helper import mkdir_folder, check_process
from framework.automotive.utils.data_type import EcuInfo
from framework.automotive.utils.new_relay_helper import jy_dam0800_check_and_repair


from xat_ecu.legacy.sdk.i_signal_i_pdu import *
from xat_ecu.legacy.sdk.bus_app import BusApp
from xat_ecu.legacy.common.logmanagment.logmanager import *
from xat_ecu.legacy.sdk.driver.jidutest_io.io.io_system import IOSystem
from framework.automotive.utils.bgm_helper import get_class_begin_bgm_log, get_class_after_bgm_log


class CommonTestBase:
    @staticmethod
    def change_bench_config(ecu: EcuInfo) -> EcuInfo:
        """子类重写该接口，自定义台架类型为单域、两域或者四域"""
        return ecu

    def before_class_setup(self, ecu: EcuInfo):
        logger.info(inspect.stack()[0].function + ' start!')
        try:
            if "power_control_type" in ecu.tb_config:
                if ecu.tb_config.get("power_control_type") == "jydam0800":
                    jy_dam0800_check_and_repair()
        except Exception as e:
            logger.exception(f"继电器恢复初始状态时，执行异常, 异常原因:{str(e)}")

        ecu.class_uuid = uuid.uuid4()
        ecu.class_case_fail_flag = False
        ecu.class_bgm_log = {}
        ecu_new = copy.deepcopy(ecu)
        ecu_new = self.change_bench_config(ecu=ecu_new)
        self.tb_config = ecu_new.tb_config
        self.tc_config = ecu_new.tc_config

        self.tc_config.update(self.tb_config)
        logger.debug("ecu : {}".format(ecu_new))
        wifi_localhost = self.tc_config.get("wifi_localhost")
        logger.info(f"当前在{wifi_localhost}台架上运行")
        # init cls
        try:
            self.io = IOSystem(self.tc_config)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/core/common_test_base.py")
            logger.error(f'IO初始化异常,原因:{str(e)}')
            raise exception_error.IOSystemError(f'IO初始化异常,原因:{str(e)}')
        self.veh_type = self.tc_config.get("veh_type")
        self.bl_ver = self.tc_config.get("bl_ver")
        if self.veh_type and self.bl_ver:
            self.cls_path = "sdk/data/{}/can_lin_fr_cls/{}".format(
                self.veh_type, self.bl_ver
            )
            self.tn_config_path = "config/{}/{}/ecu_network.yaml".format(
                self.veh_type, self.bl_ver
            )
        else:
            err_msg = f"Config error : self.veh_type is {self.veh_type}  self.bl_ver is {self.bl_ver}"
            logger.error(err_msg)
            raise exception_error.ConfigError(err_msg)
        self.dut_ecu = self.tc_config.get("dut_ecu")
        try:
            self.nucapp = NucApp(self.tc_config)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/core/common_test_base.py")
            logger.error(f'NucApp初始化异常，原因:{str(e)}')
            raise exception_error.NucAppError(f'NucApp初始化异常，原因:{str(e)}')
        if (
            ecu_new.domain.single_bgm or
            ecu_new.domain.two_domain or
            ecu_new.domain.four_domain or
            ecu_new.domain.bgm_cdc_acu or
            ecu_new.domain.bgm_tcam_acu or
            ecu_new.domain.bgm_tcam_cdc
        ):  # 如果当前台架包含BGM
            try:
                self.bgmcli = BGM_SSH()
                # 获取版本号：
                if ecu_new.disable_env is False:
                    try:
                        version_info = self.bgmcli.get_version()
                        logger.info(f"获取bgm的版本信息version_info={version_info}")
                    except Exception as e:
                        __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/core/common_test_base.py")
                        logger.warning(f"获取bgm版本信息失败:{str(version_info)}")

                    # set salt.json
                    self.bgmcli.get_set_salt()

                    # 获取bgm 开机信息
                    uptime = self.bgmcli.get_uptime()
                    logger.info(f"bgm 开机时间信息 :  {uptime}")
                    get_class_begin_bgm_log(self.bgmcli, ecu)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/core/common_test_base.py")
                logger.error(f"ssh 连接失败 {str(e)}")
        elif ecu_new.domain.single_tcam:
            logger.info("通过TCAM更新soa partner")
            self.bgmcli = None
            if ecu_new.disable_env is False:
                try:
                    version_info = TCAM_SSH().get_soa_jidl_name()
                    logger.info(f"获取TCAM的版本信息version_info={version_info}")
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/core/common_test_base.py")
                    logger.warning(f"获取TCAM版本信息失败:{e.__repr__()}")

                # set salt.json
                TCAM_SSH().get_set_salt()
        # auto目录将venus改为mars1
        cls_path = self.cls_path.replace('venus', 'mars1')
        set_sig_auto(cls_path)  # set sig auto version
        try:
            logger.info(self.cls_path)
            self.ipdu = ISignalIPdu(cls_path=self.cls_path, dut_ecu=self.dut_ecu)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/core/common_test_base.py")
            logger.error(f'ipdu初始化失败，原因:{str(e)}')
            raise exception_error.IpduError(f'ipdu初始化失败，原因:{str(e)}')
        try:
            self.busapp = BusApp(self.ipdu, **self.tc_config)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/core/common_test_base.py")
            logger.error(f'busapp初始化失败，原因:{str(e)}')
            raise exception_error.BusAppError(f'busapp初始化失败，原因:{str(e)}')
        try:
            self.log_manage = Logmagment()  # 初始化日志管理
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/framework/automotive/core/common_test_base.py")
            logger.error(f'log_manage初始化失败，原因:{str(e)}')
            raise exception_error.LogManageError(f'log_manage初始化失败，原因:{str(e)}')
        mkdir_folder()
        # 调用子类
        self.log_manage.start_record_soa_partner_log()
        self.before_class(self, ecu_new)

    def after_class_teardown(self, ecu: EcuInfo):
        # 调用子类
        try:
            self.after_class(self, ecu)
            if not ecu.domain.single_tcam and ecu.disable_env is False:
                get_class_after_bgm_log(self.bgmcli, ecu)  # 如果类有失败用例，则拷贝类相关的日志文件
            if "power_control_type" in ecu.tb_config:
                if ecu.tb_config.get("power_control_type") == "jydam0800":
                    jy_dam0800_check_and_repair()
        except AttributeError:
            # 获取错误的描述信息，例如sd_tester，ipdu，partner等
            # AttributeError: type object 'xxxx' has no attribute 'xxx'
            # error_obj = str(e).split('attribute ')[-1]
            if hasattr(self, 'ipdu'):
                self.ipdu.time_control_stop()
            if hasattr(self, 'busapp'):
                self.busapp.stop_all_cyclic_msgs()
            # raise Exception(f'{error_obj}初始化失败，请检查before_class或者before_each_func中{error_obj}初始化是否正常')
        except Exception as e:
            err_msg = f'子类after_class执行失败，原因是:{str(e)}'
            logger.exception(err_msg)
            if hasattr(self, 'ipdu'):
                self.ipdu.time_control_stop()
                self.ipdu.recv_pdu_thread_all_stop()
            if hasattr(self, 'busapp'):
                self.busapp.stop_all_cyclic_msgs()
            # raise Exception(err_msg)
        finally:
            logger.info(inspect.stack()[0].function + ' start!')
            if hasattr(self, 'io'):
                self.io.close()
            if hasattr(self, 'log_manage'):
                self.log_manage.stop_record_soa_partner_log()
            # 检查上位机上是否有其它未关闭的soa_partner进程在运行，如果有，则杀死进程
            partner_process_check()
            # 检查上位机上是否有其它未关闭的defunc进程在运行，如果有，则重载进程
            defunc_process_check()

    def before_func_setup(self, ecu: EcuInfo):
        logger.info(inspect.stack()[0].function + ' start!')
        wifi_localhost = self.tc_config.get("wifi_localhost")
        logger.info(f"当前在{wifi_localhost}台架上运行")
        if hasattr(self, 'nucapp'):
            if 'BGM' in self.dut_ecu:
                self.nucapp.bgm_diag_line_up()
                # 链接tcam的kl15
            if 'TCAM' in self.dut_ecu:
                self.nucapp.tcam_kl15_up()
        if ecu.record_log and hasattr(self, 'log_manage'):
            self.log_manage.start_record_log(ecu.testname)
        if ecu.trace_log and hasattr(self, 'busapp'):
            self.busapp.start_record_trace_log(ecu.testname)
            self.busapp.check_tosun_process()
        # 调用子类
        self.before_each_func(ecu)

    def after_func_teardown(self, ecu: EcuInfo):
        # 调用子类
        try:
            self.after_each_func(ecu)
        except AttributeError as e:
            # 获取错误的描述信息，例如sd_tester，ipdu，partner等
            # AttributeError: type object 'xxxx' has no attribute 'xxx'
            # error_obj = str(e).split('attribute ')[-1]
            # raise Exception(f'{error_obj}初始化失败，请检查before_class或者before_each_func中{error_obj}初始化是否正常')
            pass
        finally:
            if ecu.class_uuid:
                logger.info("")
                logger.info(f"当前用例所在class的日志可以在/root/fail_case_log/{ecu.class_uuid}目录下查看")
                logger.info("")
            logger.info(inspect.stack()[0].function + ' start!')
            if hasattr(self, 'log_manage'):
                partner_log = self.log_manage.stop_record_soa_partner_log()
                ecu.log_path['parter_log'] = partner_log
            if ecu.record_log and hasattr(self, 'log_manage'):
                jet_path = self.log_manage.stop_record_log()
                ecu.log_path['jet_log'] = jet_path
            if ecu.trace_log and hasattr(self, 'busapp'):
                if ecu.testresult == 'Pass':
                    self.busapp.stop_record_trace_log(is_record_status=False)
                else:
                    # 只有失败的case才将trace放在allure报告上作为附件
                    trace_path = self.busapp.stop_record_trace_log()
                    ecu.log_path['trace_log'] = trace_path
                    self.busapp.check_tosun_trace()

    def before_class(self, ecu: EcuInfo, start=False):
        pass

    def before_each_func(self, ecu: EcuInfo, start=False):
        pass

    def after_each_func(self, ecu: EcuInfo, start=False):
        pass

    def after_class(self, ecu: EcuInfo, start=False):
        pass

    def bgm_power_off_and_on(self, timeout=1):
        """bgm下电再上电"""
        self.nucapp.bgm_power_off()
        sleep(5)
        self.nucapp.bgm_power_on()
        sleep(timeout)

    def wait_for_doip_announcement(self, timeout=20):
        """等待车辆公告出现，上电超10s请求车辆公告无响应，则报错"""
        st = time.time()
        while time.time() - st < timeout:
            ip = self.nucapp.get_announcement_ip()
            if ip is None:
                sleep(1)
            else:
                return ip
        else:
            raise TimeoutError(f"{timeout}s超时未获取到车辆公告ip")

    def restart_bgm_and_connect_service(self, partner_name, pause_all_bus=True, resume_all_bus=True):
        """
        bgm重启并连接服务
        @param partner_name: 待连接的服务
        @param pause_all_bus: 是否在下电的时候停止总线
        @param resume_all_bus: 是否在上电之后恢复总线
        """
        self.bgmcli.delete_debug_script_executed_count()
        if pause_all_bus:
            self.ipdu.pause_all_bus_send()
        sleep(1)  # 下电前等待1s，否则之前的日志可能还没有落盘，造成有效日志丢失
        self.bgm_power_off_and_on(timeout=3)
        self.partner.empty_all()
        if resume_all_bus:
            self.ipdu.resume_all_bus_send()
        self.partner.wait_for_service_reconnect(partner_name)

    def bgm_sleep_and_awake(self):
        pass  # todo

    def stop_tcpdump_and_copy_and_calculate(self, save_name, data_list):
        """
        停止抓包并且返回期望的数据结果
        @param save_name: 保存的文件名
        @param data_list: 待解析的pdu信号，例[(15006, 2, 1, 10)]
        """
        self.bgmcli.stop_bgm_tcpdump()
        file_path = self.bgmcli.scp_bgm_log_to_local(bgm_log_name=save_name, del_flag=True)
        self.pcap_path = file_path
        res = get_pdu_value_and_time(data_list, file_path)
        res.update(get_pdu_value_and_time(data_list, file_path, src_ip='172.16.5.2', des_ip='172.16.5.1'))
        return res

    def kill_bgm_process(self, process_name='s2s_service'):
        """在bgm内kill指定进程"""
        res = self.bgmcli.type_commands(f"ps -ef |grep app |grep {process_name} |grep -v grep", alias="1")
        pid = res.split()[1]
        self.bgmcli.type_commands(f"kill -9 {pid}", alias="1")
