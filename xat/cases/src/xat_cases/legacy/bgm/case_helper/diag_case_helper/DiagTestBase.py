# -*- coding: utf-8 -*-
"""
@File        : test_uds_bgm_app.py
@Author      : o_wenyu.liang_ext@jiduauto.com
@Time        : 2022/11/17
@Description :

"""
import time
import pytest
import allure
import sys, os


project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat','ecu_simulator','interface')
sys.path.append(work_path_2)

work_path_3 = os.path.join(os.getcwd().split("sat")[0], 'sat','ecu_simulator','driver')
sys.path.append(work_path_3)


import binascii
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
 

from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.sdk.ecu_simulator_app import Ecu_Sim_App
from xat_ecu.legacy.interface.nuc_app import get_obd_ip
from xat_ecu.legacy.driver.ssh_client import SSHClient
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.common.logmanagment.logmanager import *
from xat_ecu.legacy.config.path import CONFIG_DIR_PATH
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig
from xat_ecu.legacy.sdk.get_obd_ip import get_announcement_ip
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *


# from ecu_simulator.sdk.get_obd_ip import get_announcement_ip

class SniffPacket:
    def __init__(self, **kwargs):
        # 停止抓包标志位
        self.sniff_flag = False
        # 所抓网口 名字
        self.iface = kwargs.get("iface", None)
        # 是否保存
        self.save_enable = kwargs.get("save_enable", True)
        # 保存路径
        self.save_path = kwargs.get("save_path", '/root/obd_doip_dump')
        # 保存名字
        self.save_name = kwargs.get("save_name", 'obd_doip_')
        #保存次数
        self.count = kwargs.get("count",1)
        pass

    def set_iface(self, iface):
        self.iface = iface

    def set_save_path(self, save_path):
        self.save_path = save_path

    def set_save_name(self, save_name):
        self.save_name = save_name

    def start_sniff(self, **kwargs):
        '''
        开启抓包线程
        @param kwargs:
        @return:
        '''
        t = threading.Thread(target=self.__sniff_func)
        t.setDaemon(True)
        t.start()
        time.sleep(3)

    def __sniff_func(self):
        logger.info(f"开始抓取{self.iface}网口的以太报文！")
        recv_packet = sniff(count=0,
                            store=1,
                            offline=None,
                            prn=None,
                            filter=None,
                            L2socket=None,
                            timeout=None,
                            opened_socket=None,
                            stop_filter=self.stop_filter,
                            iface=self.iface)

        # 保存 文件
        if self.save_enable:
            otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))
            try:
                save_name = f"第{self.count}次测试_{self.save_name}{otherStyleTime}.pcap"
                if not os.path.exists(self.save_path):
                    os.makedirs(self.save_path)
                file_path = os.path.join(self.save_path, save_name)
                logger.info(f"保存obd口抓包文件路径为===>>>{file_path}")
                wrpcap(file_path, recv_packet)
            except Exception as e:
                wrpcap(f"doip_{otherStyleTime}.pcap", recv_packet)
                logger.error(f"{str(e)}")

    def stop_filter(self, packet):
        return self.sniff_flag

    def stop_sniff(self):
        time.sleep(3)
        self.sniff_flag = True

class Flashtime:
    def __init__(self):
        self.running = True

    def print_time(self):
        before_time = time.time()
        while self.running:
            time.sleep(5)
            after_time = time.time()
            sec = after_time - before_time
            m, s = divmod(sec, 60)
            logger.info("目前已刷写时间:{}min {}s".format(m,s))
    
    def start_time(self):
        t = threading.Thread(target=self.print_time)
        t.setDaemon(True)
        t.start()

    def stop_time(self):
        self.running = False
       
class DiagTestBase:
    def __init__(self,ipdu,nucapp,tc_config):
        self.ssh_bgm = BGM_SSH()
        self.ssh_tcam = TCAM_SSH()
        self.ipdu = ipdu
        self.nucapp = nucapp
        self.tc_config = tc_config
        self.logical_address = ''
        self.payload = ''
        self.ecu_name = ''
        
        # Code Location
        tb_path = os.path.join(CONFIG_DIR_PATH, "willow_tcam_flash_config.yaml")
        tb_config = ParseTBConfig(tb_path)
        self.sd_test_tcam_tb_config = tb_config.yaml_content
        
        tb_path = os.path.join(CONFIG_DIR_PATH, "willow_bgm_flash_config.yaml")
        tb_config = ParseTBConfig(tb_path)
        self.sd_test_bgm_tb_config = tb_config.yaml_content
        
        if self.tc_config['sec_con']:
            self.tc_config['sec_con']['BGM'][3] = self.Get_Bgm_L7_Constant()
            
    def connect(self,logical_address,ecu_name='BGM',do_3E_80=True):
        self.wait_announcenmt()
        self.ecu_name = ecu_name
        self.sd_test = Sd_Tester(**self.tc_config)
        self.sd_test.update_serverdoipid(logical_address,ecu=self.ecu_name)
        time.sleep(1)
        self.logical_address = logical_address
        logger.info("当前逻辑地址:{}".format(hex(self.logical_address)))       
        sleep(0.5)      
        logger.info("==================== SdTester started ==========================")
        self.sd_test.diagnostic_client_sim_start()
        if do_3E_80 == True: 
            self.sd_test.tester_present()
        sleep(0.5)

    def close(self,do_close_3E_80=True):
        if do_close_3E_80:
            self.sd_test.stop_tester_present()
            sleep(1)
        self.sd_test.diagnostic_client_sim_close()
        sleep(0.5)
        logger.info("==================== SdTester stopped ==========================")

    def send_data(self,data,do_assert=True):
        if isinstance(data,int):
            data_str = hex(data)[2:].replace(' ', "")
            data_list = [int(data_str[i:i + 2], 16) for i in range(0, len(data_str), 2)]
            self.sd_test.send_data(data_list)
        elif isinstance(data,list):
            self.sd_test.send_data(data)
        elif isinstance(data,str):
            data_list = [int(data[i:i + 2], 16) for i in range(0, len(data), 2)]
            self.sd_test.send_data(data_list)
        
        self.payload = self.sd_test.return_udsdata_and_check_and_print_response_result()
        result = self.sd_test.check_and_print_response_result()
        
        if do_assert == False:
            pass
        else:
            if result == False or result == None:
                raise ValueError
        
    def get_payload(self):
        data_str_list=[]
        for elemnt in self.payload:
            if len(hex(elemnt)[2:]) == 1:
                elemnt = '0' + hex(elemnt)[2:]
            else:
                elemnt = hex(elemnt)[2:]
            data_str_list.append(elemnt)
        
        data_str = "".join(data_str_list)
        return data_str        
        
    def init_enter_boot_enviroment(self):
        self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
        self.ipdu.set(getattr(getattr(self.ipdu,'backbonefr'),'BcmVddmBackBoneFr06'),'VehSpdLgtA_0_BcmVddmBackBoneSignalIPdu06',0)
        # time.sleep(1)
        self.ipdu.set(getattr(getattr(self.ipdu,'backbonefr'),'BcmVddmBackBoneFr06'),'VehSpdLgtQf_0_BcmVddmBackBoneSignalIPdu06',3)
        
        self.sd_test.update_serverdoipid(0x1002,self.ecu_name)
        self.sd_test.change_usage_mode(0)
        self.sd_test.change_car_mode(0)
        self.sd_test.update_serverdoipid(self.logical_address,self.ecu_name)
            
    def enter_boot(self):
        self.send_data([0x10,0x02])
        self.close()
        time.sleep(1)
        self.connect(0x1002)
        
    def exit_boot(self):
        self.send_data([0x10,0x01])
        self.close()
        time.sleep(1)
        self.connect(0x1002)
    
    def communication_control(self,control_did,control_type=None):
        data='28'
        if len(hex(control_did)[2:]) % 2 == 0:
            data = data +  hex(control_did)[2:]
        else:
            data = data + '0' + hex(control_did)[2:]
        
        if control_type == None:
            pass
        else:
            if len(hex(control_type)[2:]) % 2 == 0:
                data = data +  hex(control_type)[2:]
            else:
                data = data + '0' + hex(control_type)[2:]
        self.send_data(data)
    
    def Get_Bgm_Log(self,my_local="."):
        logger.info("开始取BGM日志……………………………………………………")
        if not os.path.exists(my_local):
            os.makedirs(my_local)
        self.ssh_bgm.get_log(my_local)
        
    def Get_Tcam_Log(self,my_local="."):
        logger.info("开始取TCAM日志……………………………………………………")
        if not os.path.exists(my_local):
            os.makedirs(my_local)
        self.ssh_tcam.get_log(my_local)
        
    def Get_Bgm_L7_Constant(self):
        Bgm_Constant_L7 =  self.ssh_bgm.get_l7_key()
        return Bgm_Constant_L7
    
    def Get_Tcam_L7_Constant(self):
        Tcam_Constant_L7 =  self.ssh_tcam.get_L7()
        return Tcam_Constant_L7
    
    def Clear_BGM_Log(self):
        logger.info("开始清除BGM日志……………………………………………………")
        self.ssh_bgm.clear_log()
        
    def Clear_TCAM_Log(self):
        logger.info("开始清除TCAM日志……………………………………………………")
        self.ssh_tcam.clear_log()
        self.session_control(3)
        time.sleep(1)
        self.reset(0x03,False)
        
    def Get_BGM_Version(self):
        self.connect(0x1001)        
        switch_version = self.sd_test.read_switch_version_or_check()
        ecu_verison = self.sd_test.read_version_or_check()
        self.sd_test.update_serverdoipid(0x1002)
        mcu_verison = self.sd_test.read_mcu_version_or_check()
        boot_version = self.sd_test.read_boot_version_or_check()
       
        logger.info("==================== Version Information ==========================")
        logger.info("switch_version:{}".format(switch_version))
        logger.info("mcu_verison:{}".format(mcu_verison))
        logger.info("boot_version:{}".format(boot_version))
        logger.info("ecu_verison:{}".format(ecu_verison))
        logger.info("==================== Version Information ==========================")

        self.close()
        
        logger.info("==================== SdTester stopped ==========================")
        return switch_version,mcu_verison,boot_version,ecu_verison
    
    def Flash_Bgm(self,keyinfo, file_url, standard=True,check_data=None,path="."):
        try:
            self.read_data_by_identifier(0xf18c)
            payload1 = self.get_payload()
            self.sd_test.upgrade_ecu(keyinfo,file_url,standard=standard,check_data=check_data,offline=True)
            self.read_data_by_identifier(0xf18c)
            payload2 = self.get_payload()
            with allure.step("SN号复位测试"):
                if payload1 !='62f18c00000000' and payload2 !='62f18c00000000':                
                    if payload1 != payload2 :
                        logger.info("刷写前后F18C值改变！")
                        raise ValueError
                    else:
                        logger.info("刷写前后F18C值没有改变且不为零！")
                else:
                    logger.info("f18c读出值为全0")
                    raise ValueError
        except Exception as e:
            self.reset_wait(30)
            self.sd_test.update_serverdoipid(0x1002)
            self.read_data_by_identifier(0xF1EE)
            self.read_data_by_identifier(0xFED5)
            self.Get_Bgm_Log(path)
            assert False
        
    def Flash_Tcam(self, keyinfo, file_url, standard=True, check_data=None,path="."):
        try:
            self.sd_test.upgrade_ecu(keyinfo,file_url,standard=standard,check_data=check_data)
        except:
            self.reset_wait(360)
            self.Get_Bgm_Log(path)
            self.Get_Tcam_Log(path)
            assert False
            
    def reset(self,type,reconnect=True):
        data = [0x11]+[int(hex(type),16)]
        self.sd_test.send_data(data)
        self.close()
        if reconnect:
            if self.logical_address == 0x1011:
                self.reset_wait(360)
            else:
                self.reset_wait(30)
            self.connect(self.logical_address)
    
    def reset_wait(self,wait_time):
        t = time.time()
        while time.time() - t < wait_time:
            try:
                self.read_data_by_identifier(0xf186,False)
                if self.get_payload()[0:2] == '62':
                    logger.info(f"重启后延时{time.time() - t}s  读取到诊断响应:{self.get_payload()}")
                    break
                time.sleep(2)
            except Exception as e:
                    logger.info(f"重启后延时{time.time() - t}s未读取到诊断响应》》{str(e)}")
    
    def read_data_by_identifier(self,did,do_assert=True):
        data = '22'
        if len(hex(did)[2:]) %2 == 0 :
            data = data +  hex(did)[2:]
        else:
            data = data + '0' + hex(did)[2:]
            
        self.send_data(data,do_assert)
    
    def read_data_by_dtc(self,dtc,dtc_type=None):
        data = '19'
        if len(hex(dtc)[2:]) %2 == 0:
            data = data +  hex(dtc)[2:]
        else:
            data = data + '0' + hex(dtc)[2:]
        
        if dtc_type ==None:
            pass
        else:
            if len(hex(dtc_type)[2:]) %2 == 0:
                data = data +  hex(dtc_type)[2:]
            else:
                data = data + '0' + hex(dtc_type)[2:]
            
        self.send_data(data)
    
    def clear_dtc(self):
        self.send_data([0x14,0xFF,0xFF,0xFF])
         
    def session_control(self,session):
        if session == 1:
            self.send_data([0x10,0x01])
        elif session == 2:
            if self.logical_address == 0x1002:
                self.enter_boot()
            else:
                self.send_data([0x10,0x02])
        elif session == 3:
            self.send_data([0x10,0x03])
    
    def security_access_level(self,level):
        if level == 1:
            self.sd_test.security_access_level(1)
        elif level == 3:
            self.sd_test.security_access_level(2)
        elif level == 5:
            self.sd_test.security_access_level(3)
        elif level == 7:
            self.sd_test.security_access_level(4)
        elif level == 11:
            self.sd_test.security_access_level(6)
            
        if self.sd_test.assert_security_access():
            pass
        else:
            raise ValueError
            
    def control_dtc_setting(self,setting):
        data = '85'
        if len(hex(setting)[2:]) %2 == 0:
            data = data +  hex(setting)[2:]
        else:
            data = data + '0' + hex(setting)[2:]
            
        self.send_data(data)
        
    def io_control(self,io_did,io_type,io_mask=None):
        data = '2F'
        if len(hex(io_did)[2:]) %2 == 0:
            data = data +  hex(io_did)[2:]
        else:
            data = data + '0' + hex(io_did)[2:]
            
        if len(hex(io_type)[2:]) %2 == 0:
            data = data +  hex(io_type)[2:]
        else:
            data = data + '0' + hex(io_type)[2:]
            
        if io_mask == None:
            pass
        else:
            for elemnet in io_mask:
                if len(hex(elemnet)[2:]) %2  == 0:
                    data = data +  hex(elemnet)[2:]
                else:
                    data = data + '0' + hex(elemnet)[2:]
                    
        self.send_data(data)

        # if io_type == 0x00:
        #     time.sleep(3)
        # else:
        #     time.sleep(1)
        time.sleep(1)
        
    def write_data_by_identifier(self,did,write_data,do_assert=True):
        send_data = '2E'
        
        if len(hex(did)[2:]) % 2 == 0:
            send_data = send_data +  hex(did)[2:]
        else:
            send_data = send_data + '0' + hex(did)[2:]
    
        send_data = send_data +  write_data
        self.send_data(send_data,do_assert)
        time.sleep(1)
        
    def routing_control(self,routing_did,routing_type,data=None):
        data_send = '31'
        
        if len(hex(routing_type)[2:])%2 == 0:
            data_send = data_send +  hex(routing_type)[2:]
        else:
            data_send = data_send + '0' + hex(routing_type)[2:]
            
        if len(hex(routing_did)[2:])%2 == 0:
            data_send = data_send +  hex(routing_did)[2:]
        else:
            data_send = data_send + '0' + hex(routing_did)[2:]
     
        if data == None:
            pass
        else:                
            hex_data = binascii.b2a_hex(data)
            str_data = str(hex_data,encoding='utf-8')
            data_send = data_send + str_data
        
        self.send_data(data_send)
        time.sleep(1)
        
    def test_persent(self):
        self.send_data([0x3E,0x00])
    
    def wait_announcenmt(self):
        obdip = get_announcement_ip()
        i = 0
        while obdip == None:
            if i > 60 :
                break
            time.sleep(0.5)
            obdip = get_announcement_ip()
            logger.info("重连等待{}s".format(i))
            i = i + 0.5
        
        logger.info("获取到BGM ip:{}".format(obdip))
        # time.sleep(10)
    
    def change_usagemode(self,mode):
        self.sd_test.change_usage_mode(mode)
    
    def change_carmode(self,mode):
        self.sd_test.change_car_mode(mode)

    def catch_announcenent(self):
        bufsize = 1024
        addr = ('', 13400)
        udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpServer.settimeout(60)
        udpServer.bind(addr)
        logger.info("Waiting for connection....")
        while True:
            try:
                data,client_info = udpServer.recvfrom(bufsize)
                if b'\x02\xfd\x00\x04' in data:
                    after = time.time()
                    ip=client_info[0]
                    logger.info("获取到ip:{}".format(ip))
                    break
            except socket.timeout:
                logger.info("超时未收到车辆公告")
                break
        return after
    
    def reset_0x1082(self,reconnect=True):
        self.sd_test.send_data([0x10,0x82])
        self.close()
        time.sleep(1)
        if reconnect:
            self.connect(self.logical_address)
    
    def start_save_log(self,is_bgmdump=False,is_sniff=False,is_save_bgm_log=False,is_save_tcam_log=False,test_count=0,is_clear_bgm_log=False,is_clear_tcam_log=False,path="."):
        self.is_bgmdump = is_bgmdump
        self.is_save_bgm_log = is_save_bgm_log
        self.is_save_tcam_log = is_save_bgm_log
        self.is_sniff = is_sniff
        self.path = path
        self.save_name = f'第{test_count}次测试_bgm内部eth0.9抓包_'
        
        if self.is_bgmdump:
            self.file_path,save_name = self.ssh_bgm.start_bgm_tcpdump(name=self.save_name,iface="eth0.9")
            logger.info("self.file_path={}".format(self.file_path))
 
        if self.is_sniff:
            self.sniff_start(self.path,test_count)
        
        if is_clear_bgm_log:
            self.Clear_BGM_Log()
        
        if is_clear_tcam_log:
            self.Clear_TCAM_Log()
    
    def stop_save_log(self):
        if self.is_bgmdump:
            self.ssh_bgm.stop_bgm_tcpdump()
            self.ssh_bgm.scp_bgm_file_to_local(bgm_file_pah=self.file_path,local_path=self.path)
            # self.ssh_bgm.scp_bgm_log_to_local(bgm_log_name=self.save_name,log_path=self.path)
            
        if self.is_save_bgm_log:
            self.Get_Bgm_Log(self.path)
        
        if self.is_save_tcam_log:
            self.Get_Tcam_Log(self.path)
            
        if self.is_sniff:
            self.sniff_stop()
            
    def sniff_start(self,flie_path,count):
        now_time = time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime(int(time.time())))
        iface=self.tc_config['bus']['eth_obd']
        file_name=f'第{count}次测试_上位机抓包_{now_time}.pcap'
        if not os.path.exists(flie_path):
            os.makedirs(flie_path)
        file_path = os.path.join(flie_path,file_name)
        subprocess.Popen(f'tcpdump -i {iface} -w {file_path} -s 128',shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("抓包开始 等待60s")
        time.sleep(60)
        
    def sniff_stop(self):
        logger.info("抓包结束 等待60s")
        time.sleep(60)
        subprocess.Popen("ps -ef | grep tcpdump| awk '{print $2}' | xargs kill -9",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    