# -*- coding: utf-8 -*-
"""
@File        : diagnostic_odx_client_simulator_app.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2021-11-10 11:22
@Description : diagnostic_odx_client_simulator_app simulate the diagnostic_client behavior using pcan
                Similar to BD
"""

import os
import sys
import time

from xat_ecu.legacy.common.logger import logger
# from sdk.driver.ecu_simulator.diagnostic_client_sim import Diagnostic_Client_Sim
from xat_ecu.legacy.sdk.ethernet.doip_client_sim_odx import P6_CLIENT_ENHANCED_TIMEOUT, Doip_Client_Sim_Odx
from xat_ecu.legacy.sdk.can_lin.can_lin_diagnostic_client_sim import Can_Lin_Diagnostic_Client_Sim
from time import sleep
from xat_ecu.legacy.sdk.diagnostic_odx_client_simulator_app_auto import Diagnostic_Odx_Client_Sim_App_Auto
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding
from xat_ecu.legacy.sdk.bgm_crc import calc_crc_f106
from xat_ecu.legacy.utils.utils import struct_pretty


class Diagnostic_Odx_Client_Sim_App(Diagnostic_Odx_Client_Sim_App_Auto):
    def __init__(self, ecu="BGM", diag_mode="doip", server_ip="172.20.1.1", server_doip_id=0x1001, can_id=0x605,
                 channel="can0", sec_con={}):
        super().__init__()
        self.file_size = None
        self.first_address = 0
        self.memory_address = [0x00, 0x00, 0x00, 0x00]
        self.memory_size = [0x00, 0x00, 0x00, 0x00]
        if diag_mode == "doip":
            self.doip_id = server_doip_id
            self.client_sim = Doip_Client_Sim_Odx(ecu=ecu, server_doip_id=self.doip_id, server_ip=server_ip,
                                                  server_port=13400, sec_con=sec_con)
        elif diag_mode == "docan":
            bus_type = "can"
            self.client_sim = Can_Lin_Diagnostic_Client_Sim(can_id, channel, bus_type, sec_con=sec_con)

    def send_data(self, data: list):
        '''
        发送数据  列表里面需要是整型
        @param data: such as [0x10, 0x03]
        @return:
        '''
        self.client_sim.send_data(data)
    
    def reset_positive_ack(self):
        self.client_sim.reset_positive_ack()

    def get_recv_sa_id_list(self, timeout=10):
        '''
        只有doip 才有这个接口----在时间内获取的sa id  such as  0x1001
        '''
        return self.client_sim.get_recv_sa_id_list(timeout=timeout)

    def get_response_dict(self):
        # print('return self.client_sm.response_dict=', self.client_sim.response_dict)
        if self.client_sim.response_dict:
            logger.info(f"当前收到诊断回复数据：{struct_pretty(self.client_sim.response_dict)}")
        return self.client_sim.response_dict

    def update_serverdoipid(self, doipid, ecu="BGM"):
        # only for Doip
        # doip_id     0x1001  or 0x1002
        self.client_sim.update_server_doip_id(doipid, ecu=ecu)

    def get_ecu_canid(self, ecu_name):
        ecu_canid = self.data_ecu_diag[ecu_name][0]
        return ecu_canid

    def get_bus_name(self, ecu_name):
        bus_name = self.data_ecu_diag[ecu_name][1]
        return bus_name

    def get_positive_ack(self):
        return self.client_sim.positive_ack

    def check_and_print_response_result(self, diagnostic_action="Diagnostic Action"):
        '''
        用来判断发送请求后，是否接收到正响应，返回值 true 表示接收响应成功，false 表示接收正响应失败
        @param diagnostic_action: 用来描述当前动作的
        @return:
        '''
        check_response = self.client_sim.check_response()
        if check_response == True:
            logger.info("======  {} >>>>>> Pass      ======".format(diagnostic_action))
        elif check_response == False:
            logger.info("======  {} >>>>>> Fail      ======".format(diagnostic_action))
        elif check_response == None:
            logger.info("======  {} >>>>>> Response Time out      ======".format(diagnostic_action))
        return check_response

    def return_udsdata_and_check_and_print_response_result(self, diagnostic_action="Diagnostic Action"):
        '''
        发送诊断请求后，用来接收响应的
        返回一个列表 如 [0x71,0x01,0x02, 0x05,0x10,0x00,0x00,0x00,0x00,]
        @param diagnostic_action: 用来描述当前动作的
        @return:
        '''
        check_response = self.client_sim.retrun_udsdata_and_check_response()
        if check_response[0] == True:
            logger.info("======  {} >>>>>> Pass      ======".format(diagnostic_action))
        elif check_response[0] == False:
            logger.info("======  {} >>>>>> Fail      ======".format(diagnostic_action))
        elif check_response[0] == None:
            logger.info("======  {} >>>>>> Response Time out      ======".format(diagnostic_action))
        return check_response[1]

    def return_dtcdata_readdtcinformation(self):
        udsdata = self.return_udsdata_and_check_and_print_response_result("readdtcinformation")
        if udsdata[0] == 0x7F:
            return False
        else:
            dtcdatas = udsdata[3:]
            dtcdata = []
            if dtcdatas == []:
                dtcdata = dtcdatas
            else:
                dtcnum = len(dtcdatas) // 4
                for i in range(dtcnum):
                    dtcdata.append(dtcdatas[i * 4:i * 4 + 3])
            return dtcdata

    # def set_ecu_sim(self,ecu_canid,channel):
    #     ecu_canid = self.ecu_canid
    #     channel = self.channel
    #     self.ecu_sim = Ecu_Sim(ecu_canid,channel)

    def bgm_nm_all(self):
        self.client_sim.can_single_cycle(data=[0x05, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00], cycle_time=0.64)

    def diagnostic_client_sim_start(self):
        '''
        启动接收和自动回复线程
        @return:
        '''
        self.client_sim.run()

    def diagnostic_client_sim_close(self):
        '''
       关闭接收和自动回复线程
       @return:
        '''
        self.client_sim.close()

    def send_datalist(self, datalist: list):
        self.client_sim.send_data(datalist)

    def reset_ecu(self):
        '''
        硬重置
        该值表明“硬重置”条件，该条件模拟了服务器断开其电源（即电池）之后通常会执行的上电／启动序列。所执行的操作视具体情况而定，且本标准并未对其进行规定。
        这可能导致易失性存储器及非易失性存储器位置重新初始化为预设值
        @return:
        '''
        self.client_sim.send_data([0x11, 0x01])

    def reset_ecu3(self):
        '''
        软重置
        该值表明了“软重置”条件，可使服务器立即重启应用程序（如适用）。所执行的操作视具体情况而定，且本标准并未对其进行规定。
        典型操作是重新启动应用程序，而不重新初始化此前已获得的配置数据、自适应因子及其他长期调整。
        @return:
        '''
        self.client_sim.send_data([0x11, 0x03])

    def reset_ecu_functional_addressing(self):
        if hasattr(self.client_sim, "reset_positive_ack"):
            self.client_sim.reset_positive_ack()
        self.client_sim.send_data_functional_addressing([0x11, 0x81])

    def cleardiagnosticinformation_all_groups(self):
        self.client_sim.send_data([0x14, 0xFF, 0xFF, 0xFF])

    def reportnumberOfdtcbystatusmask(self):
        self.client_sim.send_data([0x19, 0x01, 0xAF])

    def readdtcinformation_default(self):
        self.client_sim.send_data([0x19, 0x02, 0x09])

    def readdtcinformation_new(self):
        self.client_sim.send_data([0x19, 0x02, 0x01])

    def reportnumberofdtc_default(self):
        self.client_sim.send_data([0x19, 0x01, 0x09])

    def reportsupporteddtcs(self):
        self.client_sim.send_data([0x19, 0x0A])

    def dtc_subfunction_not_suppored_0f(self):
        self.client_sim.send_data([0x19, 0x0F])

    def dtc_19_01_length_error(self):
        self.client_sim.send_data([0x19, 0x01, 0xFF, 0xFF, 0xFF, 0xFF])

    def dtc_19_02_length_error(self):
        self.client_sim.send_data([0x19, 0x02, 0xFF, 0xFF, 0xFF, 0xFF])

    def dtc_19_06_length_error(self):
        self.client_sim.send_data([0x19, 0x06, 0xD3, 0x61, 0x83, 0xFF, 0xFF])

    def dtc_19_0a_length_error(self):
        self.client_sim.send_data([0x19, 0x0A, 0xFF, 0xFF, 0xFF, 0xFF])

    def dtc_19_06_record_number_error(self):
        self.client_sim.send_data([0x19, 0x06, 0xD3, 0x61, 0x83, 0x0F])

    def dtc_14_length_error(self):
        self.client_sim.send_data([0x14, 0xFF, 0xFF, 0xFF, 0xFF])

    def dtc_14_group_error(self):
        self.client_sim.send_data([0x14, 0xEE, 0xEE, 0xEE])

    def reportdtcextendeddatarecordsbydtcnumber_01(self):
        self.client_sim.send_data([0x19, 0x06, 0xD3, 0x61, 0x83, 0x01])

    def reportdtcextendeddatarecordsbydtcnumber_02(self):
        self.client_sim.send_data([0x19, 0x06, 0xD3, 0x61, 0x83, 0x02])

    def reportdtcextendeddatarecordsbydtcnumber_ff(self):
        self.client_sim.send_data([0x19, 0x06, 0xD3, 0x61, 0x83, 0xFF])

    def read_Software_part_number(self):
        self.client_sim.send_data([0x22, 0xF1, 0x18])

    def controldtcsettings_on(self):
        self.client_sim.send_data([0x85, 0x01, 0xFF, 0xFF, 0xFF])

    def controldtcsettings_off(self):
        self.client_sim.send_data([0x85, 0x02, 0xFF, 0xFF, 0xFF])

    def readdatabyperiodicidentifier(self):
        self.client_sim.send_data([0x2A, 0x01, 0x00])

    def enter_default_session(self):
        '''
        进入默认会话
        @return:
        '''
        self.client_sim.send_data([0x10, 0x01])

    def send_data_to_functional_addressing(self, data):
        self.client_sim.send_data_functional_addressing(data)

    def enter_default_session_functional_addressing(self):
        self.client_sim.send_data_functional_addressing([0x10, 0x81])

    def enter_extended_session(self):
        '''
        进入扩展会发
        @return:
        '''
        self.client_sim.send_data([0x10, 0x03])

    def diagnostic_session_check(self):
        '''
        诊断会话检查
        @return:
        '''
        self.client_sim.send_data([0x22, 0xF1, 0x86])

    def diagnostic_session_check_functional_addressing(self):
        '''
        诊断会话检查 功能寻址
        @return:
        '''
        self.client_sim.send_data_functional_addressing([0x22, 0xF1, 0x86])

    def diagnostic_session_check_functional_addressing_not_wait(self):
        '''
        诊断会话检查 功能寻址 ，发送结束后不做 P3_CLIENT_MIN3 时间等待
        @return:
        '''
        self.client_sim.send_data_functional_addressing([0x22, 0xF1, 0x86], interval_time=None)

    def information_check_ed20(self):
        '''
        读取 APP ECU完整零件序列号 ，26 byte
        @return:
        '''
        self.client_sim.send_data([0x22, 0xED, 0x20])

    def information_check_f1aa(self):
        '''
        读取ECU硬件号
        BitStartPos:0
        BitLength:64
        DataType : 5BCD+3ASCII
        @return:
        '''
        self.client_sim.send_data([0x22, 0xF1, 0xAA])

    def information_check_f1ae(self):
        '''
        读取ecu 先关信息，
        ECU软件号数量:
            BitStartPos:0
            BitLength:8
            DataType : BCD
        ECU软件号:
            BitStartPos:8
            BitLength:64
            DataType : 5BCD+3ASCII
        MCU bootloader号:
            BitStartPos:72
            BitLength:64
            DataType : 5BCD+3ASCII
        @return:
        '''
        self.client_sim.send_data([0x22, 0xF1, 0xAE])

    def information_check_f1ab(self):
        self.client_sim.send_data([0x22, 0xF1, 0xAB])

    def information_check_f18c(self):
        self.client_sim.send_data([0x22, 0xF1, 0x8C])

    def public_key_status_check(self):
        self.client_sim.send_data([0x22, 0xD0, 0x1C])

    def write_public_key(self, data_list):
        self.client_sim.send_data([0x2E, 0xD0, 0x1C] + data_list)

    def write_vehicleinfo(self, data_list: list):
        self.client_sim.send_data([0x2E, 0xF1, 0x50] + data_list)

    def write_vin_list(self, data_list: list):
        self.client_sim.send_data([0x2E, 0xF1, 0x90] + data_list)

    def write_vin(self, data: str):
        data_list = list(bytes(data, encoding="ascii"))
        self.client_sim.send_data([0x2E, 0xF1, 0x90] + data_list)

    def write_vid(self, data: str):
        # param:data   such as   "5946b3754b09b4a31175208bddce80e0"
        data_list = list(bytes.fromhex(data))
        self.client_sim.send_data([0x2E, 0xB1, 0x63] + data_list)

    def write_security_constant(self, data_list):
        self.client_sim.send_data([0x2E, 0xF1, 0x02], data_list)

    def transfer_key_info(self, keyinfo=[]):
        self.routine_control([0x01], [0x02, 0x08], zz=keyinfo)

    def verify_software_integrity(self):
        self.routine_control([0x01], [0x02, 0x05], zz=[])

    def enter_program_session_functional_addressing(self):
        self.client_sim.send_data_functional_addressing([0x10, 0x82])

    def check_program_pre_condition_functional_addressing(self):
        self.client_sim.send_data_functional_addressing([0x31, 0x01, 0x02, 0x06])

    def cancel_fota(self):
        self.client_sim.send_data([0x31, 0x01, 0xA1, 0x02])

    def enter_programming_session(self):
        '''
        进入编程会话
        @return:
        '''
        self.client_sim.send_data([0x10, 0x02])

    def disable_normal_communication(self):
        self.client_sim.send_data([0x28, 0x01, 0x03])

    def response_on_event(self):
        self.client_sim.send_data([0x86, 0x02, 0x02, 0x01, 0x19, 0x02, 0x01])

    def enter_extended_session_functional_addressing(self):
        self.client_sim.send_data_functional_addressing([0x10, 0x83])

    def tester_present(self):
        '''
        开启发送3e80 线程，周期发送3e80
        @return:
        '''
        # thread
        if not self.client_sim.func_cycle:
            self.client_sim.func_cycle=True
            self.client_sim.send_data_func_cycle_thread([0x3E, 0x80])
        else:
            logger.warning(f"3e80 已经在发送！！！！")

    def tester_present_single_functional(self):
        self.client_sim.send_data_functional_addressing([0x3E, 0x80])

    def stop_tester_present(self):
        '''
        停止周期发送3e80
        @return:
        '''
        self.client_sim.func_cycle = False
        sleep(2)

    def write_data_by_identifier(self, did: int, data: str):
        '''
        写入did
        @param did: type:int     such as :  0xF15A
        @param data: type:str     such as :  "123456789"
        @return:
        '''
        did_list = [(did >> 8), (did & 0xFF)]
        data_list = list(bytes(data, "ascii"))
        if did != 0xF15A:
            self.client_sim.send_data([0x2E] + did_list + data_list)
        else:
            self.client_sim.send_data([0x2E] + did_list + [0x21, 0x04, 0x16] + data_list)

    def read_data_by_identifier(self, did: int):
        '''
        读取did
        @param did: type:int     such as :  0xF15A
        @return:
        '''
        did_list = [(did >> 8), (did & 0xFF)]
        self.client_sim.send_data([0x22] + did_list)

    def query_fota_status(self):
        self.read_data_by_identifier(0xF154)

    def io_control_hsd_out_control(self):
        self.client_sim.send_data([0x2F, 0x33, 0xC2, 0x03, 0xFF, 0xFF])

    def io_control_returncontroltoecu_hsd_out_control(self):
        self.client_sim.send_data([0x2F, 0x33, 0xC2, 0x00, 0xFF])

    def security_access_level(self, level=2):
        '''
        27 解锁过程：包含请求种子，计算key 值，发送key值，接收响应，
        解锁等级 level ：
                level=1 对应 27 01；
                level=2 对应 27 03；
                level=3 对应 27 05；
                level=4 对应 27 07
                level=5 对应 27 09

        @param level: 解锁等级 取值范围为1到5
        @return:
        '''
        self.seed_result = None
        self.key_result = None
        if level == 1:
            self.client_sim.send_data([0x27, 0x01])
        elif level == 2:
            self.client_sim.send_data([0x27, 0x03])
        elif level == 3:
            self.client_sim.send_data([0x27, 0x05])
        elif level == 4:
            self.client_sim.send_data([0x27, 0x07])
        elif level == 5:
            self.client_sim.send_data([0x27, 0x09])
        elif level == 6:
            self.client_sim.send_data([0x27, 0x11])
        elif level == 7:
            self.client_sim.send_data([0x27, 0x19])
        elif level == 8:
            self.client_sim.send_data([0x27, 0x5F])
        else:
            logger.info("security access input level is error")

        self.seed_result = self.check_and_print_response_result("Security Access seed L{}".format(level))

        if self.seed_result:
            i = 0
            while (self.client_sim.message_automatic_sent is None) and (i < 2):
                sleep(0.001)
                i += 0.001
            self.client_sim.message_automatic_sent = None
            if i < 2:
                self.client_sim.send_data(self.client_sim.automatic_send_data)
                self.key_result = self.check_and_print_response_result("Security Access key L{}".format(level))
            else:
                logger.error("Doip message send fail")
        else:
            logger.warning("Security Access seed L{} fail".format(level))

    def assert_security_access(self, security_level=""):
        return self.seed_result and self.key_result

    def security_access_level_l1(self):
        '''
         发送27 01 请求种子
         27 解锁过程：包含请求种子，计算key 值，发送key值，接收响应，
        @return:
        '''
        self.security_access_level(level=1)

    def security_access_level_l2(self):
        '''
         发送27 03 请求种子
         27 解锁过程：包含请求种子，计算key 值，发送key值，接收响应，
        @return:
        '''
        self.security_access_level(level=2)

    def security_access_level_l3(self):
        '''
         发送27 05 请求种子
         27 解锁过程：包含请求种子，计算key 值，发送key值，接收响应，
        @return:
        '''
        self.security_access_level(level=3)

    def security_access_level_l4(self):
        '''
         发送27 07 请求种子
         27 解锁过程：包含请求种子，计算key 值，发送key值，接收响应，
        @return:
        '''
        self.security_access_level(level=4)

    def security_access_level_l5(self):
        '''
         发送27 09 请求种子
         27 解锁过程：包含请求种子，计算key 值，发送key值，接收响应
        @return:
        '''
        self.security_access_level(level=5)
    
    def security_access_level_l6(self):
        '''
         发送27 11 请求种子
         27 解锁过程：包含请求种子，计算key 值，发送key值，接收响应
        @return:
        '''
        self.security_access_level(level=6)
        
    def security_access_level_l7(self):
        '''
         发送27 19 请求种子
         27 解锁过程：包含请求种子，计算key 值，发送key值，接收响应
        @return:
        '''
        self.security_access_level(level=7)
        
    def security_access_level_l8(self):
        '''
         发送27 19 请求种子
         27 解锁过程：包含请求种子，计算key 值，发送key值，接收响应
        @return:
        '''
        self.security_access_level(level=8)

    def routine_control(self, routine_type: list, rid: list, zz=[]):
        self.client_sim.send_data([0x31] + routine_type + rid + zz)

    def stop_setting_of_dtc_functional_addressing(self):
        self.client_sim.send_data_functional_addressing([0x85, 0x82, 0xFF, 0xFF, 0xFF])

    def start_setting_of_dtc_functional_addressing(self):
        self.client_sim.send_data_functional_addressing([0x85, 0x81, 0xFF, 0xFF, 0xFF])

    def stop_setting_of_dtc_functional_addressing_vbf(self):
        self.client_sim.send_data_functional_addressing([0x85, 0x82])

    def start_setting_of_dtc_functional_addressing_vbf(self):
        self.client_sim.send_data_functional_addressing([0x85, 0x81])

    def disable_normal_communication_functional_addressing(self):
        self.client_sim.send_data_functional_addressing([0x28, 0x81, 0x03])

    def enable_normal_communication_functional_addressing(self):
        self.client_sim.send_data_functional_addressing([0x28, 0x80, 0x03])

    def request_file_transfer(self, file_path="SA/flash.json",
                              file_path_and_name_path="../../project/smart_antenna/test/ethernet_comm/uds_doip/flash.json"):
        sid = 0x38
        mode_operation = 0x01

        file_path_and_name = file_path
        file_path_and_name_Length_list = list(len(file_path_and_name).to_bytes(2, byteorder='big'))
        file_path_and_name_raw = bytes(file_path_and_name, encoding="utf-8")
        file_path_and_name_raw_list = list(file_path_and_name_raw)
        # file_path_and_name_path = "../../test/ethernet_comm/uds_doip/flash.json"
        file_size = os.path.getsize(file_path_and_name_path)
        logger.info("file_size is {}".format(file_size))
        file_size_list = list(file_size.to_bytes(4, byteorder='big'))
        data_format_identifier = 0x00
        file_size_parameter_length = 0x04
        file_size_uncompressed = file_size_list
        # file_size_compressed = file_size_list

        data_list = [sid] + [mode_operation] + file_path_and_name_Length_list + file_path_and_name_raw_list + \
                    [data_format_identifier] + [file_size_parameter_length] + file_size_uncompressed
        self.client_sim.send_data(data_list)

    def request_download(self, file_path, compression_encryption_method=[0x00],**kwargs):
        self.file_size = os.path.getsize(file_path)
        logger.info("file_size is {}".format(self.file_size))
        compression_encryption_method = compression_encryption_method
        self.first_address = kwargs.get('first_address',0)
        # self.first_address = 0x1FFF
        if self.file_size < 4 * 1024 * 1024 * 1024:
            length_format = [0x44]
            self.memory_address = list(self.first_address.to_bytes(4, byteorder='big'))
            self.memory_size = list(self.file_size.to_bytes(4, byteorder='big'))
        else:
            length_format = [0x88]
            self.memory_address = list(self.first_address.to_bytes(8, byteorder='big'))
            self.memory_size = list(self.file_size.to_bytes(8, byteorder='big'))
        # print('compression_encryption_method=',compression_encryption_method)
        # print('length_format=',length_format)
        # print('self.memory_address',self.memory_address)
        # print('self.memory_size',self.memory_size)
        self.client_sim.send_data(
            [0x34] + compression_encryption_method + length_format + self.memory_address + self.memory_size)
        
    def request_download_vbf(self, memory_address: list, memory_size: list, length_format=[0x44], compression_encryption_method=[0x00]):
        self.client_sim.send_data(
            [0x34] + compression_encryption_method + length_format + memory_address + memory_size)
        
    def transfer_data_vbf(self, data: bytes, usr_block_length=1000000000):
        # Rely on  request_download
        block_length = self.client_sim.uds_client.max_bl - 2
        if (usr_block_length - 2) < block_length:
            block_length = usr_block_length
        block_sequence_counter = 0
        loop = 0
        remaining_data = data
        while remaining_data:
            if block_sequence_counter == 255:
                loop += 1
                block_sequence_counter = 0
            elif block_sequence_counter < 255:
                block_sequence_counter += 1
            else:
                block_sequence_counter = 0

            if len(remaining_data) <= block_length:
                block_data = remaining_data
                remaining_data = b''
            else:
                block_data = remaining_data[:block_length]
                remaining_data = remaining_data[block_length:]

            self.client_sim.send_data([0x36] + [block_sequence_counter] + list(block_data))

            # i = 0
            # while (self.client_sim.positive_ack is None) and (i<2):
            #     sleep(0.001)
            #     i += 0.001
            step_log = "transfer_data ---- loop: {}   block_sequence_counter:{}".format(loop,
                                                                                        block_sequence_counter)
            response_result = self.check_and_print_response_result(step_log)
            if response_result == True:
                continue
            elif response_result == False:
                logger.info("Receive NRC")
                break
            elif response_result == None:
                logger.info("Time out!!!  Message is not  received ")
                break
        return response_result

    def verify_utherticity(self, data: list):
        self.client_sim.send_data([0x31, 0x01, 0x02, 0x12] + data)

    def activate_sbl(self, data: list):
        self.client_sim.send_data([0x31, 0x01, 0x03, 0x01] + data)

    def transfer_data_test(self):
        self.client_sim.send_data([0x36, 0x01, 0x00, 0x00])

    def transfer_data(self, file_path, usr_block_length=1000000000):
        # Rely on  request_download
        if self.file_size:
            block_length = self.client_sim.uds_client.max_bl - 2
            with open(file_path, "rb") as f:
                if (usr_block_length - 2) < block_length:
                    block_length = usr_block_length
                # head_address = 0
                self.end_address = 0
                block_sequence_counter = 0
                loop = 0
                while self.end_address < self.file_size:
                    if block_sequence_counter == 255:
                        loop += 1
                        block_sequence_counter = 0
                    elif block_sequence_counter < 255:
                        block_sequence_counter += 1
                    else:
                        block_sequence_counter = 0
                    block_data = f.read(block_length)

                    self.client_sim.send_data([0x36] + [block_sequence_counter] + list(block_data))

                    # i = 0
                    # while (self.client_sim.positive_ack is None) and (i<2):
                    #     sleep(0.001)
                    #     i += 0.001
                    step_log = "transfer_data ---- loop: {}   block_sequence_counter:{}".format(loop,
                                                                                                block_sequence_counter)
                    response_result = self.check_and_print_response_result(step_log)
                    if response_result == True:
                        self.end_address += block_length
                    elif response_result == False:
                        logger.info("Receive NRC")
                        break
                    elif response_result == None:
                        logger.info("Time out!!!  Message is not  received ")
                        break
        else:
            with open(file_path, "rb") as f:
                block_length = os.path.getsize(file_path)
                block_data = f.read(block_length)
                self.client_sim.send_data([0x36] + [0x01] + list(block_data))
            logger.error("file_size is {}".format(self.file_size))

    def request_transfer_exit(self):
        self.client_sim.send_data([0x37])

    # Specific diagnostic functions
    def check_programming_preconditions(self):
        self.routine_control([0x01], [0x02, 0x03])

    def request_fota_mode(self, zz=[0x01]):
        self.routine_control([0x01], [0xA1, 0x00], zz)

    def request_enter_fota_mode(self):
        self.request_fota_mode([0x01])

    def request_exit_fota_mode(self):
        self.request_fota_mode([0x02])

    def request_enter_fota_failed(self):
        self.request_fota_mode([0x03])

    def request_exit_fota_failed(self):
        self.request_fota_mode([0x04])

    def request_download_image_routine(self):
        file_path_and_name = "SA/flash.json"
        file_path_and_name_Length_list = list(len(file_path_and_name).to_bytes(1, byteorder='big'))
        file_path_and_name_raw = bytes(file_path_and_name, encoding="utf-8")
        file_path_and_name_raw_list = list(file_path_and_name_raw)
        zz = file_path_and_name_Length_list + file_path_and_name_raw_list
        self.routine_control([0x01], [0x33, 0xBE], zz=zz)

    def erase_memory(self, file_path):
        self.file_size = os.path.getsize(file_path)
        logger.info("file_size is {}".format(self.file_size))
        self.first_address = 0

        if self.file_size < 4 * 1024 * 1024 * 1024:
            # length_format = [0x44]
            self.memory_address = list(self.first_address.to_bytes(4, byteorder='big'))
            self.memory_size = list(self.file_size.to_bytes(4, byteorder='big'))
        else:
            # length_format = [0x88]
            self.memory_address = list(self.first_address.to_bytes(8, byteorder='big'))
            self.memory_size = list(self.file_size.to_bytes(8, byteorder='big'))

        # old
        # self.routine_control([0x01], [0xFF, 0x00], zz = [0x44] + self.memory_address + self.memory_size)
        # jidu
        self.routine_control([0x01], [0xFF, 0x00], zz=self.memory_address + self.memory_size)

    def erase_memory_vbf(self, memory_address: list, memory_size: list):
        self.routine_control([0x01], [0xFF, 0x00], zz=memory_address + memory_size)

    def pregramming_dependencies(self):
        self.routine_control([0x01], [0xFF, 0x01])

    def write_fingerprint(self):
        self.write_data_by_identifier(0xF15A, "123456789")

    def io_shortTermadjustment(self):
        self.client_sim.send_data([0x2F, 0x33, 0xC1, 0x03, 0x00, 0x00])

    def start_obd_firewall_disable(self, zz=[0x78]):
        self.routine_control([0x01], [0x33, 0x86], zz)

    def stop_obd_firewall_disable(self):
        self.routine_control([0x02], [0x33, 0x86])

    def request_status_obd_firewall_disable(self):
        self.routine_control([0x03], [0x33, 0x86])

    # ========================== Special ==============================================
    def transfer_data_special(self, file_path, usr_block_length=1000000000):
        # Rely on  request_download
        if self.file_size:
            block_length = self.client_sim.uds_client.max_bl - 2
            with open(file_path, "rb") as f:
                if (usr_block_length - 2) < block_length:
                    block_length = usr_block_length
                # head_address = 0
                self.end_address = 0
                block_sequence_counter = 0
                loop = 0
                while self.end_address < self.file_size:
                    if block_sequence_counter == 255:
                        loop += 1
                        block_sequence_counter = 0
                    elif block_sequence_counter < 255:
                        block_sequence_counter += 1
                    else:
                        block_sequence_counter = 0
                    block_data = f.read(block_length)

                    sleep(0.2)
                    self.client_sim.send_data_special([0x36] + [block_sequence_counter] + list(block_data))

                    # i = 0
                    # while (self.client_sim.positive_ack is None) and (i<2):
                    #     sleep(0.001)
                    #     i += 0.001
                    step_log = "transfer_data ---- loop: {}   block_sequence_counter:{}".format(loop,
                                                                                                block_sequence_counter)
                    response_result = self.check_and_print_response_result_eth_special(step_log)
                    if response_result == True:
                        self.end_address += block_length
                    elif response_result == False:
                        logger.info("Receive NRC")
                        break
                    elif response_result == None:
                        logger.info("Time out!!!  Message is not  received ")
                        break
        else:
            with open(file_path, "rb") as f:
                block_length = os.path.getsize(file_path)
                block_data = f.read(block_length)
                self.client_sim.send_data_special([0x36] + [0x01] + list(block_data))
            logger.error("file_size is {}".format(self.file_size))

    def tester_present_special(self):
        # thread
        self.client_sim.send_data_func_cycle_special_thread([0x3E, 0x80])

    def check_and_print_response_result_eth_special(self, diagnostic_action="Diagnostic Action"):
        '''
        用来判断发送请求后，是否接收到正响应，返回值 true 表示接收响应成功，false 表示接收正响应失败
        @param diagnostic_action: 用来描述当前动作的
        @return:
        '''
        # check time fix to 10s
        check_response = self.client_sim.check_response(timeout=P6_CLIENT_ENHANCED_TIMEOUT)

        if check_response == True:
            logger.info("======  {} >>>>>> Pass      ======".format(diagnostic_action))
        elif check_response == False:
            logger.info("======  {} >>>>>> Fail      ======".format(diagnostic_action))
        elif check_response == None:
            logger.info("======  {} >>>>>> Response Time out      ======".format(diagnostic_action))
        return check_response

    # =======================================================================================================
    def read_version_or_check(self, check_data=None, read_timeout=None):
        """
        读取 ecu 软件号，并根据参数判断是否需要校验，
        @param check_data: 默认为 None 不校验，则返回（True，版本号），否则返回（校验结果，版本号）
        """
        # 读取版本号
        if read_timeout is None:
            self.information_check_f1ae()
            recv_data_list = self.return_udsdata_and_check_and_print_response_result(" 发送 f1ae 获取版本号")
        else:
            start_time = time.time()
            while True:
                self.information_check_f1ae()
                # sleep(0.5)
                recv_data_list = self.return_udsdata_and_check_and_print_response_result(" 发送 f1ae 获取版本号")
                if time.time() - start_time > read_timeout:
                    logger.error("读取版本号超时")
                    assert False, "读取版本号超时"
                # 不为正响应
                if not self.get_positive_ack():
                    sleep(0.5)
                    continue
                else:
                    break

        data_list = recv_data_list[3:]
        # 转化为16进制字符串
        data_hex = bytes(data_list).hex()
        # 判断是bgm 还是tcam
        if self.doip_id == 0x1001:
            # bgm   02 6160110110 41 41 43  296011005520 4158
            fr = chr(int(data_hex[0:2], 16))
            mid = data_hex[2:12]
            ver_str = data_hex[12:18]
            ver = ''.join([chr(int(ver_str[i:i + 2], 16)) for i in range(0, len(ver_str), 2)])
            mcu_ver = (mid + ver).upper()
            # boot 的 版本号
            boot_str = data_hex[18:]
            boot_head = boot_str[:10]
            boot_foot = boot_str[10:]
            bot = ''.join([chr(int(boot_foot[i:i + 2], 16)) for i in range(0, len(boot_foot), 2)])
            boot_ver = (boot_head + bot).upper()
            logger.info(f'获取的 bgm 版本为: {mcu_ver} 和 boot 版本为: {boot_ver}')
        # elif self.client_sim.server_doip_id == 0x1011:
        else:
            # tcam
            # 第一个字节  1ASCII+5BCD+3ASCII
            fr = chr(int(data_hex[0:2], 16))
            mid = data_hex[2:12]
            ver_str = data_hex[12:]
            ver = ''.join([chr(int(ver_str[i:i + 2], 16)) for i in range(0, len(ver_str), 2)])
            mcu_ver = (mid + ver).upper()
            boot_ver = 'None'
            logger.info(f'获取的tcam版本为{mcu_ver} ')
        # 如果不校验，则直接返回 true 和 版软件号
        if check_data is None:
            return True, mcu_ver
        elif isinstance(check_data, str):
            temp = check_data.upper().replace(' ', '')
            mcu_ver = mcu_ver.replace(' ', '')
            boot_ver = boot_ver.replace(' ', '')
            if temp.startswith("6"):
                ret_value = mcu_ver == temp
            else:
                ret_value = boot_ver == temp

        elif isinstance(check_data, (list, tuple)):
            temp = list(check_data)
            ret_value = mcu_ver == temp
        else:
            logger.error("check_data 参数的格式不对")
            ret_value = False

        return ret_value, mcu_ver

    def read_mcu_version_or_check(self, check_data=None):
        """
        读取mcu 版本号，并根据参数判断是否需要校验
        @param check_data: 默认为 None 不校验，返回版本，否则返回校验结果
        """

        sleep(0.5)
        # 读取版本号
        self.information_check_f1f0()
        sleep(0.5)
        recv_data_list = self.return_udsdata_and_check_and_print_response_result("获取 mcu 版本号")

        data_list = recv_data_list[3:]
        # 转化为16进制字符串
        data_hex = bytes(data_list).hex()
        # 第一个字节  1ASCII+5BCD+3ASCII
        fr = chr(int(data_hex[0:2], 16))
        mid = data_hex[2:12]
        ver_str = data_hex[-4:]
        ver = chr(int(ver_str[0:2], 16)) + chr(int(ver_str[2:4], 16))
        mcu_ver = (fr + mid + ver).upper()
        logger.info(f"Mcu Version：{mcu_ver}")
        if check_data is None:
            return mcu_ver
        elif isinstance(check_data, str):
            temp = check_data.upper()
            return mcu_ver == temp
        elif isinstance(check_data, (list, tuple)):
            temp = list(check_data)
            return temp == data_list
        else:
            logger.error(f"check_data 参数的格式不对")
            return None

    def read_boot_version_or_check(self, check_data=None):
        """
        读取 boot 版本号，并根据参数判断是否需要校验
        @param check_data: 默认为 None 不校验，返回版本，否则返回校验结果
        """
        # 读取版本号
        self.information_check_f1a5()
        recv_data_list = self.return_udsdata_and_check_and_print_response_result("获取 boot 版本号")

        data_list = recv_data_list[3:]
        # 转化为16进制字符串
        data_hex = bytes(data_list).hex()
        # 5BCD+3ASCII
        mid = data_hex[:10]
        ver_str = data_hex[-4:]
        ver = chr(int(ver_str[0:2], 16)) + chr(int(ver_str[2:4], 16))
        boot_ver = (mid + ver).upper()
        logger.info(f"Boot Version：{boot_ver}")
        if check_data is None:
            return boot_ver
        elif isinstance(check_data, str):
            temp = check_data.upper()
            return boot_ver == temp
        elif isinstance(check_data, (list, tuple)):
            temp = list(check_data)
            return temp == data_list
        else:
            logger.error(f"check_data 参数的格式不对")
            return None

    def read_switch_version_or_check(self, check_data=None):
        """
        读取 switch 版本号，并根据参数判断是否需要校验
        @param check_data: 默认为 None 不校验，返回版本，否则返回校验结果
        """
        # 读取版本号
        self.information_check_fd50()
        recv_data_list = self.return_udsdata_and_check_and_print_response_result("获取 switch 版本号")

        data_list = recv_data_list[3:]
        # 转化为16进制字符串
        data_hex = bytes(data_list).hex()

        new_data = data_hex[6:]
        ver_str = new_data[-12:]
        bytes_list = [chr(int(ver_str[i:i + 2], 16)) for i in range(0, len(ver_str), 2)]
        ver = ''.join(bytes_list)
        switch_ver = ver.upper()
        logger.info(f"Switch Version：{switch_ver}")
        if check_data is None:
            return switch_ver
        elif isinstance(check_data, str):
            temp = check_data.upper()
            return switch_ver == temp
        elif isinstance(check_data, (list, tuple)):
            temp = list(check_data)
            return temp == data_list
        else:
            logger.error(f"check_data 参数的格式不对")
            return None

    def information_check_f1f0(self):
        '''
        # 获取mcu 版本号
        @return:
        '''

        self.client_sim.send_data([0x22, 0xF1, 0xF0])

    def information_check_f1a5(self):
        '''
         # 获取 boot 版本号
        @return:
        '''

        self.client_sim.send_data([0x22, 0xF1, 0xA5])

    def information_check_fd50(self):
        '''
         # 获取 switch 版本号
        @return:
        '''
        self.client_sim.send_data([0x22, 0xFD, 0x50])



    def information_check_d134(self):
        """切换car mode为XX"""
        self.client_sim.send_data([0x22, 0xD1, 0x34])

    def information_check_dd0a(self):
        """
        # 读 使用模式状态
        @return:
        """

        self.client_sim.send_data([0x22, 0xDD, 0x0A])

    def io_control_usage_mode_control(self, mode_type):
        '''
        控制 使用模式  mode_type 取值如下：
            0x00=Abandoned
            0x01=Inactive
            0x02=Convenience
            0x0B=Active
            0x0D=Driving
        @param mode_type:
        @return:
        '''
        send_data = [0x2F, 0xDD, 0x0A, 0x03, mode_type]
        self.client_sim.send_data(send_data)

    def io_control_usage_mode_cancel_control(self):
        '''
         清除 使用模式
        @return:
        '''
        send_data = [0x2F, 0xDD, 0x0A, 0x00]
        self.client_sim.send_data(send_data)

    def io_control_car_mode_control(self, mode_type):
        '''
        控制 切换 car  mode_type 取值如下：
            0x00=Abandoned
            0x01=Inactive
            0x02=Convenience
            0x0B=Active
            0x0D=Driving
        @param mode_type:
        @return:
        '''
        send_data = [0x2F, 0xD1, 0x34, 0x03, mode_type]
        self.client_sim.send_data(send_data)

    def io_control_car_mode_cancel_control(self):
        '''
         清除 使用模式
        @return:
        '''
        send_data = [0x2F, 0xD1, 0x34, 0x00]
        self.client_sim.send_data(send_data)


    def change_usage_mode(self, mode_type: int, do_assert=True, **kwargs):
        '''
          切换usage mode为XX,
        @param mode_type:
             /** 废弃 */ @value(0) ABANDONED,
            /** 未激活 */ @value(1) INACTIVE,
            /** 充电 */ @value(2) CONVENIENCE,
            /** 激活 */ @value(11) ACTIVE,
            /** 驾驶 */ @value(13) DRIVING
        @param do_assert: 若为True 则表示切换失败则会报错，否则返回切换后的模式
        @return:
        '''
        # 读取did
        self.information_check_dd0a()
        # 接受数据
        result = self.return_udsdata_and_check_and_print_response_result("Send dd0a to get result")[3:]
        #
        curr_mode = result[0]
        if curr_mode == mode_type:
            return curr_mode

        # 检查当前会话，判断是否需要重新进入
        self.diagnostic_session_check()
        result = self.return_udsdata_and_check_and_print_response_result("Send f186 to get result")[3:]
        curr_status = result[-1]
        if curr_status != 0x03:
            # 进入扩展会话
            self.enter_extended_session()
            result = self.return_udsdata_and_check_and_print_response_result("Send 1003 to get result")
            if do_assert and result[0] != 0x50:
                assert 0, f'enter_extended_session 失败'
            self.security_access_level_l2()
        else:
            # 判断是否需要解锁
            self.client_sim.send_data([0x27, 0x03])
            result = self.return_udsdata_and_check_and_print_response_result("Send 0x27, 0x03 to get result")
            curr_le = result[2:]
            if curr_le != [0x00, 0x00, 0x00]:
                # 三级 27 解锁
                self.security_access_level_l2()
        # 设置使用模式
        self.io_control_usage_mode_control(mode_type)
        result = self.return_udsdata_and_check_and_print_response_result("Send dd0a to set usage mode")
        curr_status = result[0]
        if do_assert and curr_status != 0x6F:
            assert 0, f'切换Usage Mode失败, 当前为{curr_mode}'
        logger.info("切换模式以后，立马去读可能读到以前模式")
        # sleep(0.5)
        self.information_check_dd0a()
        # 接受数据
        result = self.return_udsdata_and_check_and_print_response_result("Send dd0a to get result")[3:]
        curr_mode = result[0]
        if do_assert:
            assert curr_mode == mode_type, f'切换Usage Mode失败, 当前为{curr_mode}'
        return curr_mode

    def quit_usage_mode(self,do_assert=True, **kwargs):
        '''
          退出 usagemode 控制，返回 退出控制以后的 模式
        @return:
        '''
        # 检查当前会话，判断是否需要重新进入
        self.diagnostic_session_check()
        result = self.return_udsdata_and_check_and_print_response_result("Send f186 to get result")[3:]
        curr_status = result[-1]
        if curr_status != 0x03:
            # 进入扩展会话
            self.enter_extended_session()
            result = self.return_udsdata_and_check_and_print_response_result("Send 1003 to get result")
            if do_assert and result[0] != 0x50:
                assert 0, f'enter_extended_session 失败'
            self.security_access_level_l2()
        else:
            # 判断是否需要解锁
            self.client_sim.send_data([0x27, 0x03])
            result = self.return_udsdata_and_check_and_print_response_result("Send 0x27, 0x03 to get result")[3:]
            curr_le = result[2:]
            if curr_le != [0x00, 0x00, 0x00]:
                # 三级 27 解锁
                self.security_access_level_l2()
        # 退出模式
        self.io_control_usage_mode_cancel_control()
        result = self.return_udsdata_and_check_and_print_response_result("退出usage")
        if do_assert and result[0] != 0x6F:
            assert 0, f'退出Usage Mode失败'
        self.information_check_dd0a()
        # 接受数据
        result = self.return_udsdata_and_check_and_print_response_result("Send dd0a to get result")[3:]
        curr_mode = result[0]
        return curr_mode

    def change_car_mode(self, mode_type: int, do_assert=True, **kwargs):
        '''
        切换 car mode
        @param mode_type: 切换的 模式
                    0 : NORMAL
                    1 : TRANSPORT
                    2 : FACTORY
                    3 : CRASH
                    5 : DYNO
        @param do_assert: 若为True 则表示切换失败则会报错，否则返回切换后的模式
        @return:
        '''
        # 读取did
        self.information_check_d134()
        # 接受数据
        result = self.return_udsdata_and_check_and_print_response_result("Send d134 to get result")[3:]
        curr_mode = result[0]
        if curr_mode == mode_type:
            return curr_mode
        # 检查当前会话，判断是否需要重新进入
        self.diagnostic_session_check()
        result = self.return_udsdata_and_check_and_print_response_result("Send f186 to get result")[3:]
        curr_status = result[-1]
        if curr_status != 0x03:
            # 进入扩展会话
            self.enter_extended_session()
            result = self.return_udsdata_and_check_and_print_response_result("Send 1003 to get result")
            if do_assert and result[0] != 0x50:
                assert 0, f'enter_extended_session 失败'
            self.security_access_level_l2()
        else:
            # 判断是否需要解锁
            self.client_sim.send_data([0x27, 0x03])
            result = self.return_udsdata_and_check_and_print_response_result("Send 0x27, 0x03 to get result")
            curr_le = result[2:]
            if curr_le != [0x00, 0x00, 0x00]:
                # 三级 27 解锁
                self.security_access_level_l2()
        # 设置 car 模式
        self.io_control_car_mode_control(mode_type)
        result = self.return_udsdata_and_check_and_print_response_result("Send d134 to set car mode")
        if do_assert and result[0] != 0x6F:
            assert 0, f"切换CarMode失败， 当前为{curr_mode}"
        # 不加延时立马去读，会读取切换前的模式
        logger.info("切换模式以后，立马去读可能读到以前模式")
        sleep(0.5)
        # 读取did
        self.information_check_d134()
        # 接受数据
        result = self.return_udsdata_and_check_and_print_response_result("Send d134 to get result")[3:]
        curr_mode = result[0]
        if do_assert:
            assert curr_mode == mode_type, f"切换CarMode失败， 当前为{curr_mode}"
        return curr_mode

    def quit_car_mode(self,do_assert=True, **kwargs):
        '''
       退出 car mode 控制，返回 退出控制以后的 模式
        @return:
        '''
        # 进入扩展会话
        # 检查当前会话，判断是否需要重新进入
        self.diagnostic_session_check()
        result = self.return_udsdata_and_check_and_print_response_result("Send f186 to get result")[3:]
        curr_status = result[-1]
        if curr_status != 0x03:
            # 进入扩展会话
            self.enter_extended_session()
            result = self.return_udsdata_and_check_and_print_response_result("Send 1003 to get result")
            if do_assert and result[0] != 0x50:
                assert 0, f'enter_extended_session 失败'
            self.security_access_level_l2()
        else:
            # 判断是否需要解锁
            self.client_sim.send_data([0x27, 0x03])
            result = self.return_udsdata_and_check_and_print_response_result("Send 0x27, 0x03 to get result")[3:]
            curr_le = result[2:]
            if curr_le != [0x00, 0x00, 0x00]:
                # 三级 27 解锁
                self.security_access_level_l2()

        self.io_control_car_mode_cancel_control()
        result = self.return_udsdata_and_check_and_print_response_result("退出 car mode")
        if do_assert and result[0] != 0x6F:
            assert 0, f'退出 car Mode失败'
        # 读取did
        self.information_check_d134()
        # 接受数据
        result = self.return_udsdata_and_check_and_print_response_result("Send d134 to get result")[3:]
        curr_mode = result[0]
        return curr_mode

    def read_ccp(self):
        '''
        读取 ccp  返回 ccp，字符串和 列表
        去除 62F106  和 最后两个字节的crc 校验位
        @return:
        '''
        self.information_check_f106()
        result = self.return_udsdata_and_check_and_print_response_result("发送 22F106 读取ccp")
        ret_data = bytes(result).hex()[6:-4]
        return ret_data, result[3:-2]

    def write_single_ccp(self, ccp_index: int, value: int):
        """
        写入单个ccp数据，写入第几个字节
        :param ccp_index: ccp序号，如#10, index从1开始
        :param value: 写入值
        :return: None
        """
        curr_ccp_str, ccp_list = self.read_ccp()
        curr_value = ccp_list[ccp_index - 1]
        if curr_value != value:
            # 更新ccp 值
            ccp_list[ccp_index - 1] = value
            # crc
            crc = hex(calc_crc_f106(ccp_list))[2:].zfill(4)
            crc_list = DataTypeHanding.hexstr_to_inlist(crc)
            # 进入扩展会话
            self.enter_extended_session()
            sleep(0.1)
            # 三级 27 解锁
            self.security_access_level_l3()
            # 写入ccp
            send_data = [0x2e, 0xF1, 0X06] + ccp_list + crc_list
            self.send_data(send_data)
            result = self.return_udsdata_and_check_and_print_response_result("写入ccp")
            # [0X6E,0XF1,0X06]
            return True if result[0] == 0x6E else False
        return True

    def write_multi_ccp(self, ccp_dict: dict):
        """
        写入多个ccp数据，如果读取的和写入的值相同，则不进行写入
        :param ccp_dict: 写入的ccp，如{10：2, 20: 3}
        :return:
        """
        try:
            import copy
            crc_list=[]
            curr_ccp_str, ccp_list = self.read_ccp()
            curr_ccp_value = copy.deepcopy(ccp_list)
            logger.info(f'写之前读取的ccp={bytes(ccp_list).hex()}')
            for key, value in ccp_dict.items():
                ccp_list[key - 1] = value
            if curr_ccp_value != ccp_list:
                logger.info(f'写入的的ccp={bytes(ccp_list).hex()}')
                # 生成 crc
                crc = hex(calc_crc_f106(ccp_list))[2:].zfill(4)
                crc_list = DataTypeHanding.hexstr_to_inlist(crc)

                # 检查当前会话，判断是否需要重新进入
                self.diagnostic_session_check()
                result = self.return_udsdata_and_check_and_print_response_result("Send f186 to get result")[3:]
                curr_status = result[-1]
                if curr_status != 0x03:
                    # 进入扩展会话
                    self.enter_extended_session()
                    sleep(0.1)
                    # 三级 27 解锁
                    self.security_access_level_l3()
                else:
                    # 三级 27 解锁
                    self.security_access_level_l3()

                # # 进入扩展会话
                # self.enter_extended_session()
                # sleep(0.1)
                # # 三级 27 解锁
                # self.security_access_level_l3()
                # 写入ccp
                send_data = [0x2e, 0xF1, 0X06] + ccp_list + crc_list
                self.send_data(send_data)
                result = self.return_udsdata_and_check_and_print_response_result("写入ccp")
                # [0X6E,0XF1,0X06]
                if result[0] == 0x6E:
                    return True,ccp_list + crc_list
                else:
                    assert False
            else:
                return True,[]
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/diagnostic_odx_client_simulator_app.py")
            return False,[]

    def write_ccp(self, ccp_data):
        """
        写入ccp数据
        :param ccp_data: 可以是列表,或者是字符串
        :return:
        """
        
        self.update_serverdoipid(0x1002)
        if isinstance(ccp_data, str):
            ccp_data = ccp_data.replace(' ', "")
            ccp_data_list = [int(ccp_data[i:i + 2], 16) for i in range(0, len(ccp_data), 2)]
        elif isinstance(ccp_data, (list, tuple)):
            ccp_data_list = list(ccp_data)
        else:
            assert 0, "ccp 数据格式不对，本应为列表或者字符串"
        logger.info(f'写入的的ccp={bytes(ccp_data_list).hex()}')
        # # 生成 crc
        # crc = hex(calc_crc_f106(ccp_data_list))[2:].zfill(4)
        # crc_list = DataTypeHanding.hexstr_to_inlist(crc)
        # 进入扩展会话
        self.enter_extended_session()
        sleep(0.1)
        # 三级 27 解锁
        self.security_access_level_l3()
        # 写入ccp
        #send_data = [0x2e, 0xF1, 0X06] + ccp_data_list + crc_list
        send_data = [0x2e, 0xF1, 0X06] + ccp_data_list 

        self.send_data(send_data)
        result = self.return_udsdata_and_check_and_print_response_result("写入ccp")
        # [0X6E,0XF1,0X06]
        return True if result[0] == 0x6E else False

    def information_check_f106(self):
        '''
        诊断读取ccp数据
        @return:
        '''
        self.client_sim.send_data([0x22, 0xF1, 0x06])
    
    def information_check_f1ee(self):
        '''
         # 
        @return:
        '''
        self.client_sim.send_data([0x22, 0xF1, 0xee])
        
    def information_check_db02(self):
        '''
         # 
        @return:
        '''
        self.client_sim.send_data([0x22, 0xDB, 0x02])


    def get_usge_mode(self, **kwargs):
        '''
        获取 usage mode
             /** 废弃 */ @value(0) ABANDONED,
            /** 未激活 */ @value(1) INACTIVE,
            /** 充电 */ @value(2) CONVENIENCE,
            /** 激活 */ @value(11) ACTIVE,
            /** 驾驶 */ @value(13) DRIVING
        @return:
        '''
        doipid = kwargs.get('doipid', 0x1002)
        self.update_serverdoipid(doipid)
        # 读取did
        self.information_check_dd0a()
        # 接受数据
        result = self.return_udsdata_and_check_and_print_response_result("Send dd0a to get result")[3:]
        #
        curr_mode = result[0]
        return curr_mode

    def get_car_mode(self, **kwargs):
        '''
        获取 car mode
            0 : NORMAL
            1 : TRANSPORT
            2 : FACTORY
            3 : CRASH
            5 : DYNO
        @return:
        '''
        doipid = kwargs.get('doipid', 0x1002)
        self.update_serverdoipid(doipid)
        # 读取did
        self.information_check_d134()
        # 接受数据
        result = self.return_udsdata_and_check_and_print_response_result("Send d134 to get result")[3:]
        curr_mode = result[0]
        return curr_mode

    def get_exhibition_mode(self, **kwargs):
        '''
        获取展车模式
         返回 True 是展车模式，返回False 则不是
        @return:
        '''
        doipid = kwargs.get('doipid', 0x1002)
        self.update_serverdoipid(doipid)
        # 读取 模式
        self.send_data([0x22, 0xD1, 0X35])
        result = self.return_udsdata_and_check_and_print_response_result("向1002发送  0x22, 0xD1,0X35")[3:]
        curr_mode = result[0]
        if curr_mode == 1:
            return True
        else:
            return False

    def set_exhibition_mode(self, do_assert=True, **kwargs):
        '''
        进入展车模式
        前置条件
            1.FR:36-0-1:!=13 UsgModSts1_UsgModDriving
            2.FR:55-0-1:EpbStsEpbSts=3_AllAppld
            
        返回 True 是设置展车模式成功，返回 False 设置失败
        @return:
        '''
        doipid = kwargs.get('doipid', 0x1002)
        self.update_serverdoipid(doipid)
        
        ipdu= kwargs.get('ipdu',None)
        if ipdu:
            ipdu.set(
                ipdu.backbonefr.BcmVddmBackBoneFr00,
                'EpbStsEpbSts',
                3,
            )

        ret = self.get_exhibition_mode()
        if ret:
            return ret

        # 检查当前会话，判断是否需要重新进入
        self.diagnostic_session_check()
        result = self.return_udsdata_and_check_and_print_response_result("Send f186 to get result")[3:]
        curr_status = result[-1]
        if curr_status != 0x03:
            # 进入扩展会话
            self.enter_extended_session()
            result = self.return_udsdata_and_check_and_print_response_result("Send 1003 to get result")
            if do_assert and result[0] != 0x50:
                assert 0, f'enter_extended_session 失败'
            self.security_access_level_l3()
        else:
            # 判断是否需要解锁
            self.client_sim.send_data([0x27, 0x05])
            result = self.return_udsdata_and_check_and_print_response_result("Send 0x27, 0x03 to get result")
            curr_le = result[2:]
            if curr_le != [0x00, 0x00, 0x00]:
                # 三级 27 解锁
                self.security_access_level_l3()
        # 设置使用模式
        self.client_sim.send_data([0x2e, 0xd1, 0x35, 0x01])
        result = self.return_udsdata_and_check_and_print_response_result("Send dd0a to set usage mode")
        curr_status = result[0]
        if do_assert and curr_status != 0x6E:
            assert 0, f'设置展车模式失败'
        # sleep(0.5)

        # 接受数据
        ret = self.get_exhibition_mode()
        if do_assert:
            assert ret, f'设置展车模式失败'
        return ret

    def set_unexhibition_mode(self, do_assert=True, **kwargs):
        '''
        退出展车模式

        返回 True 是退出展车模式成功，返回 False 退出失败
        @return:
        '''
        doipid = kwargs.get('doipid', 0x1002)
        self.update_serverdoipid(doipid)
        ipdu= kwargs.get('ipdu',None)
        if ipdu:
            ipdu.set(
                ipdu.backbonefr.BcmVddmBackBoneFr00,
                'EpbStsEpbSts',
                3,
            )
            
        ret = self.get_exhibition_mode()
        if not ret:
            return not ret

        # 检查当前会话，判断是否需要重新进入
        self.diagnostic_session_check()
        result = self.return_udsdata_and_check_and_print_response_result("Send f186 to get result")[3:]
        curr_status = result[-1]
        if curr_status != 0x03:
            # 进入扩展会话
            self.enter_extended_session()
            result = self.return_udsdata_and_check_and_print_response_result("Send 1003 to get result")
            if do_assert and result[0] != 0x50:
                assert 0, f'enter_extended_session 失败'
            self.security_access_level_l3()
        else:
            # 判断是否需要解锁
            self.client_sim.send_data([0x27, 0x05])
            result = self.return_udsdata_and_check_and_print_response_result("Send 0x27, 0x03 to get result")
            curr_le = result[2:]
            if curr_le != [0x00, 0x00, 0x00]:
                # 三级 27 解锁
                self.security_access_level_l3()
        # 设置使用模式
        self.client_sim.send_data([0x2e, 0xd1, 0x35, 0x00])
        result = self.return_udsdata_and_check_and_print_response_result("Send dd0a to set usage mode")
        curr_status = result[0]
        if do_assert and curr_status != 0x6e:
            assert 0, f'设置展车模式失败'
        # sleep(0.5)

        # 接受数据
        ret = self.get_exhibition_mode()
        if do_assert:
            assert not ret, f'设置展车模式失败'
        return not ret

    def get_soft_version(self, **kwargs):
        '''
        发送 F1 AE 获取软件版本号
        @param kwargs:
        @return:
        '''
        doipid = kwargs.get("doipid", None)
        if doipid:
            self.update_serverdoipid(doipid)
        self.send_data([0x22, 0xF1, 0XAE])
        recv_data_list = self.return_udsdata_and_check_and_print_response_result(" 发送 f1ae 获取软件版本号")
        if recv_data_list and recv_data_list[0] == 0x62:
            data_list = recv_data_list[3:]
            # 需要区分下 bgm  62 F1 AE 02 61 60 11 01 10 20 46 4B 29 60 11 01 10 20 41 49
            #  62 F1 AE 01 61 20 11 01 10 20 4C 4C
            # 转化为16进制字符串
            data_hex = bytes(data_list).hex()
            fr = chr(int(data_hex[0:2], 16))
            mid = data_hex[2:12]
            ver_str = data_hex[12:18]
            ver = ''.join([chr(int(ver_str[i:i + 2], 16)) for i in range(0, len(ver_str), 2)])
            mcu_ver = (mid + ver).upper()
            logger.info(f'获取的 软件版本为: {mcu_ver}')
            if len(data_hex) > 18:
                # boot 的 版本号
                boot_str = data_hex[18:]
                boot_head = boot_str[:10]
                boot_foot = boot_str[10:]
                bot = ''.join([chr(int(boot_foot[i:i + 2], 16)) for i in range(0, len(boot_foot), 2)])
                boot_ver = (boot_head + bot).upper()
                logger.info(f'获取的 bgm 版本为: {mcu_ver} 和 boot 版本为: {boot_ver}')
                return mcu_ver, boot_ver
            return mcu_ver
        else:
            logger.error("读取软件版本号失败")
            mcu_ver = None

        return mcu_ver

    def get_hard_version(self, **kwargs):
        '''
        获取硬件版本号
        @param kwargs:
        @return:   8895036217  A
        '''
        doipid = kwargs.get("doipid", None)
        if doipid:
            self.update_serverdoipid(doipid)
        # 发送 指令
        self.send_data([0x22, 0xF1, 0XAA])
        recv_data_list = self.return_udsdata_and_check_and_print_response_result(" 发送 f1ae 获取硬件版本号")
        if recv_data_list and recv_data_list[0] == 0x62:

            data_list = recv_data_list[3:]
            # 转化为16进制字符串 62 F1 AA   88 95 03 62 14 20 20 46
            data_hex = bytes(data_list).hex()
            ver1 = data_hex[:10]
            ver2 = data_hex[10:]
            hard_ver = ver1 + ''.join([chr(int(ver2[i:i + 2], 16)) for i in range(0, len(ver2), 2)])
            logger.info(f"获取的硬件号为{hard_ver}")
            return hard_ver
        else:
            logger.error("读取版本号失败")
            hard_ver = None

        return hard_ver



if __name__ == "__main__":
    # work dir: ecu_simulator
    # cmd: python3 sdk/diagnostic_odx_client_simulator_app.py

    doip_client = Diagnostic_Odx_Client_Sim_App(diag_mode="doip", server_ip="172.20.9.12", server_doip_id=0x1001)
    doip_client.diagnostic_client_sim_start()
    sleep(1)
    doip_client.tester_present()
    sleep(1)
    doip_client.enter_extended_session()
    sleep(1)
    doip_client.diagnostic_client_sim_close()
    sleep(2)
    print("end")


    # doip_client = Diagnostic_Odx_Client_Sim_App(do_can=False)
    # doip_client.diagnostic_client_sim_start()
    # sleep(1)
    # doip_client.tester_present()
    # sleep(1)
    # doip_client.enter_extended_session()
    # sleep(1)
    # doip_client.security_access_level()
    # sleep(1)
    # doip_client.diagnostic_client_sim_close()
    # sleep(2)
    # print("end")
