# -*- coding: utf-8 -*-
"""
@File        : DiagTestBase.py
@Author      : wenyu.liang_ext@jiduauto.com
@Time        : 2022/11/17
@Description :

"""
import re
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
from xat_ecu.legacy.sdk.i_signal_i_pdu import ISignalIPdu
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.nuc_app import get_obd_ip
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.interface.tcam.tcam_ssh import TCAM_SSH
from xat_ecu.legacy.common.logmanagment.logmanager import *
from xat_ecu.legacy.sdk.get_obd_ip import get_announcement_ip
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *
import shutil
from xat_ecu.legacy.driver.ssh_interface import command_send
from datetime import datetime, timedelta

def check_tcam_time_is_sync():
    status, outmsg = command_send(device_name="TCAM", cmd="date +%s", connect_type="obd", timeout=5)
    tcam_time = 0
    try:
        tcam_time = int(outmsg)
    except Exception as e:
        logger.warning(f"获取tcam时间错误：{e}")
    ncu_time = int(time.time())
    if abs(ncu_time - tcam_time) > 30:
        raise AssertionError(f"ncu时间不同步，获取到ncu时间为:{ncu_time}")
    logger.info(f"tcam时间同步...")


def check_tcam_network_is_alive():
    status, outmsg = command_send(device_name="TCAM", cmd="ping -w 120 www.baidu.com", connect_type="obd")
    match_data = re.findall(r".*icmp_seq=\d+ ttl=\d+ time=\d+.*", outmsg)
    if not match_data:
        logger.warning(f"网络不通，获取到的信息是:{outmsg}")
        raise AssertionError(f"网络不通，获取到的信息是:{outmsg}")
    logger.info(f"tcam网络通畅...")


def check_tcam_network_and_time_sync():
    check_tcam_time_is_sync()
    time.sleep(90)
    check_tcam_network_is_alive()

def caculor_timeout(start_time,end_time,sec_value):
    start_time1 = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
    end_time1 = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")
    difference = end_time1 - start_time1
    sixty_seconds = timedelta(seconds=sec_value)
    Standard_value = timedelta(seconds=117)
    result_timedelta = difference + sixty_seconds - Standard_value
    # 将timedelta对象转换为秒
    result_in_seconds = result_timedelta.total_seconds()
    if result_in_seconds > 10:
        print(f"当前计算出来的差值为：{result_in_seconds} config_service 进程起来超过10s")
        return False
    else:
        print(f"当前计算出来的差值为：{result_in_seconds}")
        return True

def get_log_data_whether_timeout():
        """
        检查log中的config_service是否超时
        """
        # 获取当前日期
        today = datetime.today().date()
        # 格式化日期为YYYYMMDD格式
        date_str = today.strftime("%Y%m%d")
        if not os.path.exists("./jet_log"):
            os.mkdir("./jet_log")
        outmsg = TCAM_SSH(connect_type='obd').type_commands("ls /mnt/sdcard/log/jetlog_message*")
        #使用正则表达式去除 ANSI 转义序列
        cleaned_list = [re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', item) for item in [i for i in outmsg.split("\n")]]
        # 现在筛选出清洁后的列表中的符合条件的字符串
        filtered_cleaned_list = [item for item in cleaned_list if item.startswith('/mnt') and item.endswith('.zst')]
        new_list = [j for i in filtered_cleaned_list for j in i.split(" ") if j != ""]
        pattern = r'\b2024-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}\b'
        get_time_message_list = []
        for i in new_list:
            if date_str in i:
                error_message = TCAM_SSH(connect_type='obd').type_commands(f'/oemapp/bin/zstdcat {i} | grep -E "Start res|jetlogd start|Booting Linux on physical CPU"')
                if error_message != "":
                    get_time_message_list.append((i,error_message.strip("")))

        if get_time_message_list:
            for i in get_time_message_list:
                sec_time = int(re.findall("{sec:(.*?),",i[1])[0])
                start_time = re.findall(pattern,i[1])[0]
                end_time = [re.findall(pattern,j) for j in i[1].split("\n") if "config_service" in j][0][0]
                logger.info(f"start_time 为：{start_time},end_time 为：{end_time},sec_tiem为：{sec_time}s")
                res = caculor_timeout(start_time,end_time,sec_time)
                if res is False:
                    with allure.step(f"config_server进程超过10s,文件为：{i[0]}"):
                        file_download(device_name="TCAM", local_path="./jet_log", remote_path=i[0])


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
        # #保存次数
        # self.count = kwargs.get("count",1)

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
        time.sleep(2)

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
                save_name = f"{self.save_name}{otherStyleTime}.pcap"
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
        # time.sleep(2)
        self.sniff_flag = True
        time.sleep(2)

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
        self.ssh_tcam = TCAM_SSH('obd') #只给压测刷写使用
        self.ipdu = ipdu
        self.nucapp = nucapp
        self.tc_config = tc_config
        self.logical_address = ''
        self.payload = ''
        self.ecu_name = ''
       
        try:
            self.tc_config['sec_con']['BGM'][3] = self.get_bgm_l7()
            self.tc_config['sec_con']['TCAM'][3] = self.get_tcam_l7()
        except Exception as e:
            logger.info(f"ERROR:{e}")
        
    def connect(self,logical_address,ecu_name='BGM',do_3e80=True):
        # self.wait_announcenmt()
        self.do_3e80 = do_3e80
        self.ecu_name = ecu_name
        self.tc_config["sd_tester_cfg"]['ecu_name'] = self.ecu_name
        self.sd_test = Sd_Tester(**self.tc_config)
        self.sd_test.update_serverdoipid(logical_address,self.ecu_name)
        time.sleep(1)
        self.logical_address = logical_address
        logger.info("当前逻辑地址:{}".format(hex(self.logical_address)))       
        sleep(0.5)      
        logger.info("==================== SdTester started ==========================")
        self.sd_test.diagnostic_client_sim_start()
        if self.do_3e80: 
            self.sd_test.tester_present()
        sleep(0.5)

    def close(self):
        if self.do_3e80:
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
            
        if not do_assert:
            pass
        else:
            if not result:
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
        
    def init_boot_per(self):
        try:
            logger.info("初始化进boot环境：车速设置为0 usagemod设置为abandoned carmode设置normal EpbStsEpbSts设置EpbSts_AllAppld")
            logger.info("开始设置车速为0")
            self.ipdu.set_vehspd(0)
            logger.info("开始EpbStsEpbSts为EpbSts_AllAppld")
            self.ipdu.set(getattr(getattr(self.ipdu, 'backbonefr'), 'BcmVddmBackBoneFr00'), 'EpbStsEpbSts', 3)
            logger.info("开始切换usagemode以及carmode")
            self.sd_test.update_serverdoipid(0x1002,'BGM')
            self.read_data_by_identifier(0xf186)
            p = self.get_payload()
            if p[-1:] == 2:
                logger.info("在boot下 无法切换usagemode以及carmode")
                
            else:
                logger.info("不在boot下 开始切换usagemode以及carmode")
                self.ipdu.backbonefr_bcmvddmbackbonefr00_vehmtnstvehmtnst_0_bcmvddmbackbonesignalipdu00_vehmtnst2_standstillval3()
                self.sd_test.change_car_mode(0)
                self.sd_test.change_usage_mode(0)
        except Exception as e:
            logger.info(f"初始化环境失败：ERROR：{e}")
        finally:
            self.sd_test.update_serverdoipid(self.logical_address,self.ecu_name)
            
    def enter_boot(self):
        self.send_data([0x10,0x02])
        self.sd_test.stop_tester_present()
        time.sleep(2)
        self.sd_test.tester_present()
        time.sleep(18)
        
    def exit_boot(self):
        self.send_data([0x10,0x01])
        self.sd_test.stop_tester_present()
        time.sleep(2)
        self.sd_test.tester_present()
        time.sleep(18)
        self.read_data_by_identifier(0xf186)
        p = self.get_payload()
        assert p == '62f18601'
    
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
    
    def get_bgm_log(self,my_local="."):
        logger.info("开始取BGM日志……………………………………………………")
        if not os.path.exists(my_local):
            os.makedirs(my_local)
        self.ssh_bgm.get_jetlogs(my_local)
        
    def get_tcam_log(self,my_local=".", connect_type='vlan'):
        logger.info("开始取TCAM日志……………………………………………………")
        if not os.path.exists(my_local):
            os.makedirs(my_local)
        self.ssh_tcam.get_log(my_local, connect_type=connect_type)
    
    def get_bgm_l7(self):
        Bgm_Constant_L7 =  self.ssh_bgm.get_l7_key()
        logger.info(f"获取到BGM L7 KEY： {Bgm_Constant_L7}")
        return Bgm_Constant_L7
    
    def get_tcam_l7(self):
        Tcam_Constant_L7 =  self.ssh_tcam.get_L7()
        logger.info(f"获取到TCAM L7 KEY： {Tcam_Constant_L7}")
        return Tcam_Constant_L7
    
    def clear_bgm_log(self):
        logger.info("开始清除BGM日志……………………………………………………")
        self.ssh_bgm.clear_log()
        
    def clear_tcam_log(self):
        logger.info("开始清除TCAM日志……………………………………………………")
        self.ssh_tcam.clear_log()
        self.session_control(3)
        time.sleep(1)
        self.reset(0x03,False)
        
    def get_bgm_version(self):
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
    
    def flash_bgm(self,keyinfo, file_url,standard=True,check_data=None,skip_step=[0],offline=True,sniff_packet=True,save_path='.'):
        try:
            self.close_fireware()
            self.sd_test.update_serverdoipid(0x1001)
            self.read_data_by_identifier(0xf18c)
            p1 = self.get_payload()
            self.sd_test.upgrade_ecu(keyinfo,file_url,standard,check_data,skip_step,offline,False,sniff_packet,save_path)
            self.sd_test.update_serverdoipid(0x1001)
            self.read_data_by_identifier(0xf18c)
            p2= self.get_payload()
            if p1==p2:
                logger.info('刷写前后 BGM的F18C序列号一致')
            else:
                assert p1 == p2 ,'刷写前后 BGM的F18C序列号不一致'
        except Exception as e:
            logger.info(f"BGM刷写失败：{e}")
            self.sd_test.update_serverdoipid(0x1002)
            self.read_data_by_identifier(0xF1EE)
            self.read_data_by_identifier(0xFED5)
            assert False
        finally:
            self.sd_test.update_serverdoipid(self.logical_address)
        
    def flash_tcam(self,keyinfo, file_url,standard=True,check_data=None,skip_step=[0],offline=True,sniff_packet=True,save_path='.'):
        try:
            if self.tc_config["sd_tester_cfg"]['ecu_name'] == "TCAM":
                sniff_packet = False
            else:
                self.close_fireware()
            self.sd_test.update_serverdoipid(0x1011)
            self.read_data_by_identifier(0xf18c)
            p1 = self.get_payload()
            self.sd_test.upgrade_ecu(keyinfo,file_url,standard,check_data,skip_step,offline,False,sniff_packet,save_path,restart_wait_time=90, read_timeout=10)
            self.sd_test.update_serverdoipid(0x1011)
            self.read_data_by_identifier(0xf18c)
            p2= self.get_payload()
            if p1==p2:
                logger.info('刷写前后 TCAM的F18C序列号一致')
            else:
                assert p1 == p2 ,'刷写前后 TCAM的F18C序列号不一致'
        except Exception as e:
            logger.info(f"TCAM刷写失败：{e}")
            assert False
        finally:
            self.sd_test.update_serverdoipid(self.logical_address)
            
    def reset(self,type,reconnect=True,do_assert=True):
        data = [0x11]+[int(hex(type),16)]
        if do_assert:
            self.send_data(data)
        else:
            self.send_data(data,False)
        self.sd_test.stop_tester_present()
        # time.sleep(10)
        time.sleep(1)
        if reconnect:
            if self.logical_address == 0x1011:
                logger.info("TCAM重启 等待3分钟。。。")
                time.sleep(170)
            self.sd_test.tester_present()
            time.sleep(2)
    
    def reset_wait(self,wait_time):
        t = time.time()
        while time.time() - t < wait_time:
            try:
                self.read_data_by_identifier(0xf186,False)
                if self.get_payload()[0:2] == '62':
                    logger.info(f"重启后延时{time.time() - t}s  读取到诊断响应:{self.get_payload()}")
                    break
                else:
                    logger.info(f"重启后延时{time.time() - t}s  未读取到诊断响应")
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
        
        time.sleep(0.07)
        self.read_data_by_identifier(0xf186)
        p = self.get_payload()
        assert p[-1] == str(session)
    
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
    
    def change_usagemode(self,mode):
        self.sd_test.change_usage_mode(mode)
    
    def change_carmode(self,mode):
        self.sd_test.change_car_mode(mode)

    def catch_announcenent(self):
        bufsize = 1024
        addr = ('', 13400)
        udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpServer.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        udpServer.settimeout(60)
        udpServer.bind(addr)
        logger.info("Waiting for connection....")
        while True:
            try:
                data,client_info = udpServer.recvfrom(bufsize)
                if b'\x02\xfd\x00\x04' and b'\x10\x01'  in data:
                    strhex = ''
                    hexlist = []
                    for i in list(data):
                        if len(hex(i)) % 2 == 0:
                            hexlist.append(hex(i))
                        else:
                            hexlist.append('0x0' + hex(i)[2:])
                    for i in hexlist:
                        strhex += i[2:]
                    after = time.time()
                    ip=client_info[0]
                    logger.info(f"client={client_info} packagdata={strhex}")
                    logger.info("获取到ip:{}".format(ip))
                    break
            except socket.timeout:
                udpServer.close()
                logger.info("超时未收到车辆公告")
                break
        udpServer.close()
        return after
    
    def reset_0x1082(self,reconnect=True):
        self.sd_test.send_data([0x10,0x82])
        # self.close()
        self.sd_test.stop_tester_present()
        time.sleep(1)
        if reconnect:
            self.sd_test.tester_present()
            #self.connect(self.logical_address)
            
    def sniff_start_proccess(self,flie_path,count):
        now_time = time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime(int(time.time())))
        iface=self.tc_config['bus']['eth_obd']
        file_name=f'第{count}次测试_上位机抓包_{now_time}.pcap'
        if not os.path.exists(flie_path):
            os.makedirs(flie_path)
        file_path = os.path.join(flie_path,file_name)
        subprocess.Popen(f'tcpdump -i {iface} -w {file_path} -s 128',shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("抓包开始 等待5s")
        time.sleep(5)
        
    def sniff_stop_process(self):
        logger.info("抓包结束 等待5s")
        time.sleep(5)
        subprocess.Popen("ps -ef | grep tcpdump| awk '{print $2}' | xargs kill -9",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def close_fireware(self):
        try:
            self.sd_test.update_serverdoipid(0x1001)
            self.session_control(1)
            self.read_data_by_identifier(0xB165)
            p = self.get_payload()
            if p[6:] == '02':
                logger.info("防火墙已关闭")
            else:
                logger.info("防火墙打开状态，关闭防火墙")
                self.session_control(3)
                self.security_access_level(7)
                self.routing_control(0xA040, 0x01, data=0x02FF.to_bytes(2, 'big'))
                self.read_data_by_identifier(0xB165)
                p = self.get_payload()
                assert p[6:] == '02','关闭防火墙失败'
        except Exception as e:
            logger.info(f"关闭防火墙失败 ERROR:{e}")
        finally:
            self.sd_test.update_serverdoipid(self.logical_address)
            
    def get_mcu_cpuload(self):
        try:
            self.sd_test.update_serverdoipid(0x1002)
            self.read_data_by_identifier(0xDB02)
            p = self.get_payload()
            cpuload1 = p[6:8]
            cpuload2 = p[8:10]
            cpuload3 = p[10:12]
            cpuload4 = p[12:14]
            logger.info(f'50ms内mcu当前负载：{cpuload1}%  50ms内mcu峰值负载：{cpuload2}% 500ms内mcu当前负载：{cpuload3}% 500ms内mcu峰值负载：{cpuload4}%')
        except Exception as e:
            logger.info(f"ERROR：{e}")
        finally:
            self.sd_test.update_serverdoipid(self.logical_address)
            
def delete_log_file(log_path,exp_log_num=10):
    """Keep latest log files according exp_log_num value"""
    try:
        log_list = os.listdir(log_path)
        log_list = sorted(log_list, key=lambda x:os.path.getmtime(os.path.join(log_path, x)))
        log_list.reverse()
        if len(log_list) > 10:
            logger.info("日志文件夹文件大于10个 删除多余文件")
            num = 0
            for f in log_list:
                num += 1
                if num >= exp_log_num:
                    log_file = log_path + '/' + f
                    if os.path.isdir(log_file):
                        shutil.rmtree(log_file)
        else:
            logger.info("日志文件夹文件小于等于10个 不需要删除多余文件")
    except Exception as e:
            logger.info("ERROR: Delete log files failed!!! {e}")