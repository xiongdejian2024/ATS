# -*- coding: utf-8 -*-
"""
@File        : ecu_simulator.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2020-08-25 23:59
@Description : (Ecu_Sim)simulate the ecu behavior using pcan
"""

from pickletools import long1
from xat_ecu.legacy.sdk.driver.lin_lib.lin import Lin
import time
import errno
import subprocess
import threading
from threading import Thread
from copy import deepcopy
from xat_ecu.legacy.common.logger import *
from xat_ecu.legacy.sdk.ecu_sim_const import ECUSimConst
import can
from time import sleep
from enum import IntEnum



class EcuSim:

    def __init__(self, tbcfg):
        self.sim_ecu_info_list = []
        self.logfile_timestamp = time.strftime("%Y.%m.%d_%H.%M.%S")
        self.can_mapping = tbcfg.get('can_bus')

    def helper_start_ecu(self, ecu='CDC', scenario=ECUSimConst.SETUP_DO_NOT_SIMULATE_NRC, logpath="logs/fod/", restart_flag=""):
        """Simulate ECUs using the UDS-stack
        compiled uds-stack binary is copied to "tools/uds_stack/uds-stack"
        For FOD, we simulate all CAN and LIN
        """
        try:
            import os
            os.makedirs(logpath)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        outfile = logpath + "{}_{}SIM_{}.txt".format(str(ecu).upper(), restart_flag, self.logfile_timestamp)
        try:
            os.mknod(outfile)
            logger.info(outfile)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        try:
            context = {
                'can_id': ECUSimConst.ECU_DIAG_CAN_MAP_TABLE[ecu][ECUSimConst.DIAG_REQ_ID_IDX],
                'can_port': self.can_mapping.get(ECUSimConst.ECU_DIAG_CAN_MAP_TABLE[ecu][ECUSimConst.CAN_PORT_IDX]),
                'interfaces': 1,
                'log_level': 2,
                'mpc_addr': '127.0.0.1',
                'scenario': scenario
            }
            import os
            logger.info(os.getcwd())
            project_path = os.getcwd().split('project')[0]
            uds_path = os.path.join(project_path, 'tools', 'uds_stack', 'uds-stack')
            command = uds_path + " -D {can_id} -C {can_port} -F {interfaces} -v" \
                      " {log_level} -M {mpc_addr} -R None -S {scenario}".format(**context)
            with open(outfile, "w+") as file:
                return subprocess.Popen(command, shell=True, stderr=file, stdout=file)
        except KeyError as error:
            print(error)
            raise

    def start_ecu_list(self, ecus, scenario=ECUSimConst.SETUP_DO_NOT_SIMULATE_NRC, logpath="logs/fod/"):
        for ecu in ecus:
            if ecu != 'CGW':
                self.sim_ecu_info_list.append([ecu, self.helper_start_ecu(ecu,
                                scenario=ECUSimConst.SETUP_DO_NOT_SIMULATE_NRC, logpath=ECUSimConst.FOD_LOG_DIRECTORY)])

        #start the process monitor thread here
        self.monitor_thread = threading.Thread(target=self.monitor_all_ecus, name='ecu_sim_monitor',daemon=True)
        self.monitor_thread.start()

    def monitor_all_ecus(self):
        time.sleep(30)
        while self.sim_ecu_info_list != []:
            try:
                templist = self.sim_ecu_info_list[:]
                for elem in templist:
                    if elem[1].poll() != None:
                        logging.warning("Identified that {} with PID {} went down. Hence restarting it".format(elem[0], str(elem[1].pid)))
                        current_scenario = ECUSimConst.ECU_DIAG_CAN_MAP_TABLE[elem[0]][ECUSimConst.ECU_BEHAVIOUR]
                        self.sim_ecu_info_list.remove(elem)
                        restart_flag_and_timestamp = "RESTARTED_{}_".format(time.strftime("%Y.%m.%d_%H.%M.%S"))
                        self.sim_ecu_info_list.append([elem[0], self.helper_start_ecu(elem[0],
                                            scenario=current_scenario, logpath=ECUSimConst.FOD_LOG_DIRECTORY, restart_flag=restart_flag_and_timestamp)])
                templist = []
                time.sleep(.5)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/tp/someiptp.py")
                logging.warning("Exception: {} caught".format(e))
        logger.info("monitor down")

    def terminate_all_ecus(self):
        #TODO: Killing the logqueue is added here temporarily
        os.system("killall uds-stack")
        self.sim_ecu_info_list = []
        try:
            self.monitor_thread.join()
        except:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/tp/someiptp.py")
            pass

    def set_ecu_behaviour_fod(self, mqttfodobj, ecu, behaviour=ECUSimConst.SETUP_DO_NOT_SIMULATE_NRC):
        mqtt_topic= "fod/{}/test/simulatenrc".format(int(ECUSimConst.ECU_DIAG_CAN_MAP_TABLE[ecu][ECUSimConst.DIAG_REQ_ID_IDX], 0))
        mqttfodobj.publish_async(mqtt_topic, message=str(behaviour))
        mqttfodobj.async_tx()
        ECUSimConst.ECU_DIAG_CAN_MAP_TABLE[ecu][ECUSimConst.ECU_BEHAVIOUR] = behaviour
    
    def set_ecu_behaviours_for_ecus_list(self, mqtt_nuc, ecu_cfg_dict):
        for ecu in ecu_cfg_dict.keys():
            if ecu != "CGW":
                self.set_ecu_behaviour_fod(mqtt_nuc, ecu, behaviour=ecu_cfg_dict[ecu])
                
    def set_ecu_reset_behavior_for_ecus_list(self, test_class_obj, test_type=ECUSimConst.ALL_ECUS_VALID_CONFIGURATION):
        mqtt_nuc = test_class_obj.mqtt_nuc
        test_class_obj.ecus_for_cfg_reset = deepcopy(test_class_obj.ecus_for_cfg)
        if test_type != ECUSimConst.ALL_ECUS_VALID_CONFIGURATION:
            test_class_obj.ecus_for_cfg_reset[list(test_class_obj.ecus_for_cfg_reset.keys())[-1]] = ECUSimConst.SETUP_SIMULATE_NRC
        for ecu in test_class_obj.ecus_for_cfg_reset.keys():
            if ecu != 'CGW':
                self.set_ecu_behaviour_fod(mqtt_nuc, ecu, test_class_obj.ecus_for_cfg_reset[ecu])
        logger.info("Reset Configuration Dict: {}, TestType: {}".format(test_class_obj.ecus_for_cfg_reset, test_type))


# Lin Diagnosis TP
class Lin_Tp:   
    @staticmethod    
    def construct_tx_signal_frames(lin_nad,data):
        msg_length = len(data)   # msg_length <= 6
        signal = [msg_length]
        
        while len(data) > 0:
            signal.append(data.pop(0))
        # add "FF"
        ff_length = 6 - msg_length 
        signal = signal + [0xFF]*ff_length
        
        # add lin node address
        signal = [lin_nad] + signal
        return signal
    
    @staticmethod     
    def construct_tx_multi_frames(lin_nad,data):
        msg_length = len(data)   # msg_length <= 4095 and msg_length >6
        first_header = 0x1000 | msg_length
        first = [(first_header >> 8)]
        first.append(first_header & 0xff)

        while len(first) < 7 and len(data) > 0:
            first.append(data.pop(0))
        tx_frames = [[lin_nad] + first]

        idx = 0
        for i in range(msg_length//6):
            idx += 1
            consecutive_frame = [0x20 | idx]
            while len(consecutive_frame) < 7 and len(data) > 0:
                consecutive_frame.append(data.pop(0))
            consecutive_frame = [lin_nad] + consecutive_frame
            tx_frames.append(consecutive_frame)
            if idx == 0xF:
                idx = -1
        # add "FF"
        ff_length = 8 - len(tx_frames[-1])
        consecutive_frame_last = tx_frames[-1] + [0xFF]*ff_length
        tx_frames[-1] = consecutive_frame_last
        return tx_frames

    @staticmethod 
    def deconstruct_rx_signal_frames(msg):
        lin_nad = msg[0]
        length = 0xf & msg[1]
        data = msg[2:]
        return length, data
    
    @staticmethod     
    def deconstruct_rx_first_frame(msg):
        length = ((0xf & msg[1]) << 8) | msg[2]
        lin_nad = msg[0]
        data = msg[3:]
        return length, data

    @staticmethod 
    def deconstruct_rx_consecutive_frame(msg):
        lin_nad = msg[0]
        index = msg[1] & 0xf
        data = msg[2:]
        return index, data


# Can Diagnosis TP
class CanTP:
       
    @staticmethod    
    def construct_tx_signal_frames(data):
        msg_length = len(data)   # msg_length <= 7
        signal = [msg_length]
        
        while len(data) > 0:
            signal.append(data.pop(0))
        # add "AA"
        aa_length = 7 - msg_length 
        signal = signal + [0xAA]*aa_length
        return signal
    
    @staticmethod     
    def construct_tx_multi_frames(data):
        msg_length = len(data)   # msg_length <= 4095 and msg_length >7
        first_header = 0x1000 | msg_length
        first = [(first_header >> 8)]
        first.append(first_header & 0xff)

        while len(first) < 8 and len(data) > 0:
            first.append(data.pop(0))
        tx_frames = [first]

        idx = 0
        for i in range(msg_length//7):
            idx += 1
            consecutive_frame = [0x20 | idx]
            while len(consecutive_frame) < 8 and len(data) > 0:
                consecutive_frame.append(data.pop(0))
            tx_frames.append(consecutive_frame)
            if idx == 0xF:
                idx = -1
        # add "AA"
        aa_length = 8 - len(tx_frames[-1])
        consecutive_frame_last = tx_frames[-1] + [0xAA]*aa_length
        tx_frames[-1] = consecutive_frame_last
        return tx_frames

    @staticmethod 
    def construct_tx_flow_frame(fc_flag=0, block_size=8, st=20):
        tx_flow_control_frame = [0x30 | fc_flag]
        tx_flow_control_frame.append(block_size)
        tx_flow_control_frame.append(st)
        aa_length = 5
        tx_flow_control_frame = tx_flow_control_frame + [0xAA]*aa_length
        return tx_flow_control_frame
    
    @staticmethod 
    def deconstruct_rx_signal_frames(msg):
        # msg is Message.data
        #frame_type = msg[0] >> 4
        length = 0xf & msg[0]
        data = msg[1:]
        return length, data
    
    @staticmethod     
    def deconstruct_rx_first_frame(msg):
        # msg is Message.data
        #frame_type = msg[0] >> 4
        length = ((0xf & msg[0]) << 8) | msg[1]
        data = msg[2:]
        return length, data

    @staticmethod 
    def deconstruct_rx_consecutive_frame(msg):
        #frame_type = msg[0] >> 4
        index = msg[0] & 0xf
        data = msg[1:]
        return index, data

    @staticmethod 
    def deconstruct_rx_flow_frame(msg):
        #frame_type = ((0xf << 4) & msg[0]) >> 4
        fc_flag = msg[0] & 0xf
        block_size = msg[1]
        st = msg[2]
        return fc_flag, block_size, st
    
    # @staticmethod 
    # def construct_tx_data(sid,did,data):
    #     tx_data = sid + did + data
    #     if len(tx_data)<8 :
    #         return self.construct_tx_signal_frames(tx_data)
    #     else:
    #         return self.construct_tx_multi_frames(tx_data)
    #     pass
    
    @staticmethod
    def crc8( data, div = 0x11D):
        '''
        **CRC8 algorithm used is defined by SAE (refer to SAE-J1850), using the division
        polynomial x8+x4+x3+x2+1    div = 0x11D
        :data is list , such as [0x11,0x22]
        '''
        t_crc = 0xFF
        i = 0
        while i < len(data):
            t_crc ^= data[i]
            b = 0
            while b < 8:
                if (t_crc & 0x80) != 0:
                    t_crc <<= 1
                    t_crc ^= div
                else:
                    t_crc <<= 1
                b += 1
            i += 1
        t_crc ^= 0xFF
        return t_crc	
    
    def diagnostics_tx_data(self,data):
        pass


class Diagnostic_Sid(IntEnum):
    DIAGNOSTICSESSIONCONTROL = 0X10
    ECURESET = 0X11
    CLEARDIAGNOSTICINFORMATION = 0X14
    READDTCINFORMATION = 0X19
    READDATABYIDENTIFIER = 0X22
    SECURITYACCESS = 0X27
    COMMUNICATIONCONTROL = 0X28
    WRITEDATABYIDENTIFIER = 0X2E
    INPUTOUTPUTCONTROLBYIDENTIFIER = 0X2F
    ROUTINECONTROL = 0X31
    REQUESTDOWNLOAD = 0X34
    TRANSFERDATA = 0X36
    REQUESTTRANSFEREXIT = 0X37
    TESTERPRESENT = 0X3E
    CONTROLDTCSETTINGS =0X85

       
class Ecu_Sim():
    """
    Ecu_Sim
    At present, a case
    Parameter solidification, follow-up will be updated
    """

    def __init__(self, ecu_canid, channel, bus_type = "can", bitrate=500000, p_n_res = True, data_info = [] , nrc_code = 0x22 , dtc_code = [] ,
                 routine_control_p_data = {}):
        """
        Initialize a SocketCan object.
        :param ecu_canid: can id of ecu,such as '0x644'     type : int
        :param channel: channel interface, such as 'can0', 'can1'    type : str
        :param bitrate: bitrate of socket can, default is 500000
        :param p_n_res: Positive Response or Negative Response,such as Ture,False   type:bool
        :param data_info : Response date ,such as [0x32,0x45,0x37]         type:list or dict
        :param dtc_code : such as  {'C16A904': [86, 169, 4, 15] ,'C16AA04': [86, 170, 4, 15]}      type : dict 
                            [86, 169, 4, 15] is DTC code and  status Of DTC      
                            DTC code ,such as 'B150111'   
        :param routine_control_p_data : routine control positive data (include rid , routine_type , rsr)  ,      type:dict 
                            such as  {"08BA": { 1 : [0x00] , 3 : [0x02]}}
                            rid: "08BA" is  HV PowerDown 
                            routine_type:  are Fixed
                                        1  ---- "start routine"
                                        2  ---- "stop rountine"
                                        3  ---- "rountine results"   
                            rsr: [0x00],[0x02],[0xA0,0x01] Specific ECU may have different implementation         
        """
        # threading.Thread.__init__(self)
        self.ecu_canid = ecu_canid    # can id of ecu, such as '0x644' 
        self.lin_nad = ecu_canid & 0xff    # lin ecu node address
        self.res_ecu_canid = self.ecu_canid + 0x80
        self.channel = channel        # channel name, such as 'can0'
        self.bitrate = bitrate 
        self.p_n_res = p_n_res        # Positive Response or Negative Response,such as True,False
        self.data_info = data_info    # Positive Response DID date ,such as [0x32,0x45,0x37] type:list     
                                      #or type:dict (Default is recommended)  
        self.nrc_code = nrc_code
        self.dtc_code = dtc_code
        self.all_dtc_code_data = []
        self.bus_type = bus_type
        self.diagnostic_session = 0x01
        self.non_default_diagnostic_session_time = 0
        self.non_default_diagnostic_session_flag = False
        self.seed = [0,0,0,0]
        self.p_data = []
        self.routine_control_p_data = routine_control_p_data

    def run(self):
        """
        
        """
        if self.bus_type == "can":
            self.rx_bus = can.interface.Bus(bustype='socketcan', channel=self.channel,bitrate=self.bitrate)
            self.rx_bus.set_filters([{"can_id": self.ecu_canid, "can_mask": 0xffff}])
            #logger.info(self.ecu_canid)
            self.notifier = can.Notifier(self.rx_bus, [self.can_rx_tx_msg])
        elif self.bus_type == "lin":
            self.rx_bus = can.interface.Bus(bustype='socketcan_native', channel=self.channel,bitrate=self.bitrate)
            self.rx_bus.set_filters([{"can_id": 0x3c, "can_mask": 0xfc}])
            self.notifier = can.Notifier(self.rx_bus, [self.lin_rx_tx_msg])
            

    def close(self):
        """
        Close Ecu_Sim by stopping notifier and interface_bus 
        """
        try:
            self.notifier.stop()
            self.rx_bus.socket.close()
            self.rx_bus.shutdown()
        except AttributeError:
            logger.error('Ecu_Sim close error: {}'.format(self.ecu_canid))
    
  
    def can_rx_tx_msg(self,msg):
        #logger.info("msg is {}".format(msg))
        rx_multi_frame_num = 0
        i = 0
        
        frame_type = msg.data[0] >> 4
        #logger.info("frame_type is {}".format(frame_type))
        
        can_id_3  = msg.arbitration_id >> 8
        if can_id_3 != 6:
            logger.info("Unfiltered messages when ECU_sim starts")
        else:    
            if frame_type == 0 :
                length, data = CanTP.deconstruct_rx_signal_frames(msg.data)
                self.sid = data[0]
                self.get_sub_data = data[1:length]
                if self.p_n_res:
                    self.diagnostic_services_p_data(self.sid,self.get_sub_data)
                    if self.p_data != [] :    
                        if len(self.p_data) <= 7:
                            self.data = CanTP.construct_tx_signal_frames(self.p_data)
                            # logger.info(self.data)
                            msg = can.Message(arbitration_id=self.res_ecu_canid, data=self.data, is_extended_id=False)
                            self.rx_bus.send(msg)
                        elif len(self.p_data) > 7:
                            self.frame_num = len(self.p_data) //7
                            #logger.info("frame length is {}".format(self.frame_num + 1))
                            if self.frame_num > 0 :
                                self.data = CanTP.construct_tx_multi_frames(self.p_data)
                                # logger.info(self.data)
                                msg = can.Message(arbitration_id=self.res_ecu_canid, data=self.data[0], is_extended_id=False)
                                self.rx_bus.send(msg)
                else:
                    self.diagnostic_services_n_data()
                    self.data = CanTP.construct_tx_signal_frames(self.n_data)
                    logger.info(self.data)
                    msg = can.Message(arbitration_id=self.res_ecu_canid, data=self.data, is_extended_id=False)
                    self.rx_bus.send(msg)

            elif frame_type == 1 :
                # The flow frame uses the default value temporarily
                length, data = CanTP.deconstruct_rx_first_frame(msg.data)
                if length <= 7 :
                    logger.error("data length of rx_first_frame is error, it is less than 8")
                elif length > 7:
                    rx_multi_frame_num = length // 7
                    logger.info("The number of this multi frame is {}".format(self.frame_num + 1))
                self.data = CanTP.construct_tx_flow_frame()
                msg = can.Message(arbitration_id = self.res_ecu_canid, data=self.data, is_extended_id=False)
                self.rx_bus.send(msg)

            elif frame_type == 2:
                # Temporary fixed use (block_size = 8)
                if rx_multi_frame_num > 1 :
                    if i < 7 :
                        # index , data = CanTP.deconstruct_rx_consecutive_frame(msg.data)
                        rx_multi_frame_num -= 1
                        i += 1
                    elif i == 7 :
                        self.data = CanTP.construct_tx_flow_frame()
                        msg = can.Message(arbitration_id = self.ecu_canid, data=self.data, is_extended_id=False) 
                        self.rx_bus.send(msg)
                        rx_multi_frame_num -= 1                        
                        i = 0
                elif rx_multi_frame_num == 1:
                    i = 0 
                    rx_multi_frame_num = 0
                    logger.info("It is detected that all consecutive frames have been sent")
                else :
                    i = 0 
                    rx_multi_frame_num = 0
                    logger.error("The total number of multiple frames exceeded the expectation")                         

            elif frame_type == 3:
                fc_flag, block_size, st = CanTP.deconstruct_rx_flow_frame(msg.data)
                if fc_flag == 0:
                    # ContinueToSend
                    if block_size == 0:
                        #The BS parameter value zero (0) shall be used to indicate to the sender that 
                        #no more FC frames shall besent during the transmission of the segmented message.
                        bs = self.frame_num
                    else:    
                        self.frame_num = self.frame_num - block_size
                        if self.frame_num <= 0:                
                            bs = self.frame_num + block_size
                        else:
                            bs = block_size   
                    for i in range(bs):
                        #logger.info("i value is {}".format(i))
                        msg = can.Message(arbitration_id=self.res_ecu_canid, data=self.data[i+1], is_extended_id=False)
                        self.rx_bus.send(msg)
                        if st == 0:
                            sleep(0.005)    # Tentative 5ms
                            logger.info("Tx Message interval is 5ms")
                        elif st > 0 and st < 0x80 :
                            # SeparationTime (STmin) range: 0 ms – 127 ms 
                            sleep(st/1000)
                            logger.info("Tx Message interval is {}ms".format(st))   
                        elif st >= 0xF1 and st <= 0xF9:
                            #SeparationTime (STmin) range: 100 μs – 900 μs
                            #However, compass can only send messages at a maximum speed of about 500us, 
                            #so messages are sent at 1ms intervals
                            sleep(0.001)
                            #logger.info("Tx Message interval is 1ms")
                        else:
                            assert False,"This range of Tsmin values is reserved by this part of ISO 15765"
                elif fc_flag == 1:  
                    logger.info("Wait for a new FlowControl")
                elif fc_flag == 2:
                    assert False,"Exceeds the buffer size of the receiving entity"
                else:
                    assert False,"This range of FS values is reserved by this part of ISO 15765"
                    
    def lin_rx_tx_msg(self,msg):
        #logger.info("lin msg is {}".format(msg))

        frame_type = msg.data[1] >> 4
        #logger.info("lin frame_type is {}".format(frame_type))
        pid = msg.arbitration_id
        # logger.info("pid is {}".format(pid))
        # logger.info("self.lin_nad is {}".format(self.lin_nad))
        # logger.info("msg.data[0] is {}".format(msg.data[0]))
        
        if  self.lin_nad == msg.data[0]:
        # Screening different Lin ECU           
            if pid == 0x3c :
                logger.info("lin Diagnosis resquest")
                if frame_type == 0 :
                    length, data = Lin_Tp.deconstruct_rx_signal_frames(msg.data)
                    self.sid = data[0]
                    self.get_sub_data = data[1:length]
                    if self.p_n_res:
                        self.diagnostic_services_p_data(self.sid,self.get_sub_data)
                        if self.p_data != [] :  
                            if len(self.p_data) <= 6:
                                self.data = Lin_Tp.construct_tx_signal_frames(self.lin_nad , self.p_data)
                                logger.info(self.data)
                                msg = can.Message(arbitration_id = 0x7d, data=self.data, is_extended_id=False)
                                self.rx_bus.send(msg)
                                self.frame_num = 0
                            elif len(self.p_data) > 6:
                                self.frame_num = len(self.p_data) //6
                                self.i = 0
                                #logger.info("frame length is {}".format(self.frame_num + 1))
                                self.data = Lin_Tp.construct_tx_multi_frames(self.lin_nad , self.p_data)
                                # logger.info(self.data)
                                msg = can.Message(arbitration_id = 0x7d, data=self.data[self.i], is_extended_id=False)
                                self.rx_bus.send(msg)                                
                    else:
                        self.diagnostic_services_n_data()
                        self.data = Lin_Tp.construct_tx_signal_frames(self.lin_nad , self.n_data)
                        logger.info(self.data)
                        msg = can.Message(arbitration_id = 0x7d, data=self.data, is_extended_id=False)
                        self.rx_bus.send(msg)
                                
                elif frame_type == 1 :
                    # If there is a requirement to be added
                    #length, data = Lin_Tp.deconstruct_rx_first_frame(msg.data)
                    pass

                elif frame_type == 2:
                    # If there is a requirement to be added
                    pass
        
            if pid == 0x3d:
                if self.frame_num > 0 :
                    self.i = self.i + 1 
                    self.frame_num = self.frame_num - 1
                    #logger.info("self.i value is {}".format(self.i))
                    msg = can.Message(arbitration_id= 0x7d, data=self.data[self.i], is_extended_id=False)
                    self.rx_bus.send(msg)

                elif self.frame_num == 0:
                    logger.info("lin msg send finished")
    
    def diagnostic_services_n_data(self):
        self.n_data = [0x7F] + [self.sid] + self.nrc_code
        #logger.info(self.n_data)
                
    def diagnostic_services_p_data(self,sid,get_sub_data):
        if sid == Diagnostic_Sid.READDATABYIDENTIFIER:
            self.read_data_by_identifier_p_data(get_sub_data)
        elif sid == Diagnostic_Sid.DIAGNOSTICSESSIONCONTROL:
            self.diagnostic_session_control_p_data(get_sub_data)
        elif sid == Diagnostic_Sid.TESTERPRESENT:
            self.tester_present_p_data(get_sub_data)
        elif sid == Diagnostic_Sid.SECURITYACCESS:
            self.security_access_p_data(get_sub_data)    
        elif sid == Diagnostic_Sid.WRITEDATABYIDENTIFIER:
            self.write_data_by_identifier_p_data(get_sub_data)
        elif sid == Diagnostic_Sid.ECURESET:
            self.ecu_reset(get_sub_data)
        elif sid == Diagnostic_Sid.READDTCINFORMATION:
            self.read_dtc_information(get_sub_data)
        elif sid == Diagnostic_Sid.CLEARDIAGNOSTICINFORMATION:
            self.clear_diagnostic_information(get_sub_data)
        elif sid == Diagnostic_Sid.ROUTINECONTROL:
            self.routine_control(get_sub_data)    
        else:
            # serviceNotSupported (NRC is 0x11)
            self.p_data = [0x7F,sid,0x11]
            logger.error("{} serviceNotSupported".format(sid))
                
    def read_data_by_identifier_p_data(self,get_sub_data):
        # SID is 0x22
        sid = Diagnostic_Sid.READDATABYIDENTIFIER
        sub_id = [get_sub_data[0],get_sub_data[1]]
        if isinstance(self.data_info,dict):
            data_key = ((hex((sub_id[0] << 8)+sub_id[1]))[2:]).upper()
            if len(data_key) < 4 :
                data_key = "0"*(4 - len(data_key)) + data_key
            if isinstance(self.data_info[data_key], str):
                self.p_data = [sid + 0x40] + sub_id +  list(bytes(self.data_info[data_key],"ascii"))
            elif isinstance(self.data_info[data_key], list):
                self.p_data = [sid + 0x40] + sub_id +  self.data_info[data_key]
        elif isinstance(self.data_info,list):
            self.p_data = [sid + 0x40] + sub_id + self.data_info
        # logger.info(self.p_data)
        
    def diagnostic_session_control_p_data(self,get_sub_data):
        # SID is 0x10
        sid = Diagnostic_Sid.DIAGNOSTICSESSIONCONTROL
        sub_id = get_sub_data[0]
        
        # Timing P2server value is provided in 1ms resolution  (0x32)
        # Timing P2*server value is provided in 10ms resolution  (0xC8)
        self.p_data = [sid + 0x40] + [sub_id] + [0x00,0x32,0x00,0xC8]
        self.diagnostic_session = sid
        if sid != 0x01:
            if self.non_default_diagnostic_session_flag:
                self.non_default_diagnostic_session_time = 0
            else:
                self.non_default_diagnostic_session = Thread(target=self.non_default_diagnostic_session_5s)
                self.non_default_diagnostic_session.start()
                self.non_default_diagnostic_session_flag = True
                logger.info("enter non default diagnostic session")
        else :
            self.non_default_diagnostic_session_time = 5
            logger.info("enter default diagnostic session")
        
    def non_default_diagnostic_session_5s(self):
        while self.non_default_diagnostic_session_time < 5:
            sleep(0.1)
            self.non_default_diagnostic_session_time += 0.1
        self.diagnostic_session = 0x10
        self.non_default_diagnostic_session_flag = False
        self.non_default_diagnostic_session_time = 0
        logger.info("exit non default diagnostic session")
    
    def tester_present_p_data(self,get_sub_data):
        # SID is 0x3E
        sid = Diagnostic_Sid.TESTERPRESENT
        sub_id = get_sub_data[0]
        if sub_id == 0x80:
            self.non_default_diagnostic_session_time = 0
            logger.info("receive keeping session")
        else:
            self.p_data = [sid + 0x40] + [sub_id]
            
    def security_access_p_data(self,get_sub_data):
        # SID is 0x27
        sid = Diagnostic_Sid.SECURITYACCESS
        sub_id = get_sub_data[0]
        if sub_id in [0x01,0x03,0x05,0x07]:
            random4 = os.urandom(4)
            # self.seed = list(random4)
            self.seed = [0xB8 , 0xED , 0x62 ,0xE8]
            self.p_data = [sid + 0x40] + [sub_id] + self.seed
        elif sub_id in [0x02,0x04,0x06,0x08]:
            get_calculatedKey = list(get_sub_data[1:5])
            self.get_calculated_key()
            logger.info("seed is {0} , get_calculatedKey is {1} , self.calculatedKey is {2}".format(self.seed , get_calculatedKey , self.calculatedKey))
            if get_calculatedKey == self.calculatedKey:
                self.p_data = [sid + 0x40] + [sub_id]
            else:
                self.p_data = [sid + 0x40] + [sub_id]
                logger.info("Force simulation to pass security level")
            
    def crc8(self, data):
        t_crc = 0xFF
        i = 0
        SEED_LENGTH = 6
        while i < SEED_LENGTH:
            t_crc ^= data[i]
            b = 0
            while b < 8:
                if (t_crc & 0x80) != 0:
                    t_crc <<= 1
                    t_crc ^= 0x11D
                else:
                    t_crc <<= 1
                b += 1
            i += 1
        return ~t_crc
    
    def get_calculated_key(self):
        # The difference(ecu_id & SecurityAccessLevel) was not made
        # Take no account of SECURITY_ACCESS_AES (0x09,0x0A)
        seed = self.seed
        crc_byte = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        buf_byte = [seed[0], seed[1], seed[2], seed[3],0,0]
        logger.info(
            "Compute key from= 0x%02X,0x%02X,0x%02X,0x%02X,0x%02X,0x%02X" % (buf_byte[0], buf_byte[1], buf_byte[2],
                                                                                buf_byte[3], buf_byte[4], buf_byte[5]))
        crc_byte[0] = self.crc8(buf_byte) & 0xFF

        buf_byte[0] = crc_byte[0]
        crc_byte[1] = self.crc8(buf_byte) & 0xFF

        buf_byte[0] = seed[0]
        buf_byte[1] = crc_byte[1]
        crc_byte[2] = self.crc8(buf_byte) & 0xFF

        buf_byte[1] = seed[1]
        buf_byte[2] = crc_byte[2]
        crc_byte[3] = self.crc8(buf_byte) & 0xFF

        buf_byte[2] = seed[2]
        buf_byte[3] = crc_byte[3]
        crc_byte[4] = self.crc8(buf_byte) & 0xFF

        buf_byte[3] = seed[3]
        buf_byte[4] = crc_byte[4]
        crc_byte[5] = self.crc8(buf_byte) & 0xFF

        buf_byte[4] = 0
        buf_byte[5] = crc_byte[5]
        crc_byte[6] = self.crc8(buf_byte) & 0xFF

        self.calculatedKey = [0, 0, 0, 0]
        if (crc_byte[6] == 0) and (crc_byte[5] == 0) and (crc_byte[4] == 0) and (crc_byte[3] == 0):
            self.calculatedKey[0] = crc_byte[1] & 0xFF
            self.calculatedKey[1] = crc_byte[2] & 0xFF
            self.calculatedKey[2] = crc_byte[3] & 0xFF
            self.calculatedKey[3] = crc_byte[4] & 0xFF
        else:
            self.calculatedKey[0] = crc_byte[3] & 0xFF
            self.calculatedKey[1] = crc_byte[4] & 0xFF
            self.calculatedKey[2] = crc_byte[5] & 0xFF
            self.calculatedKey[3] = crc_byte[6] & 0xFF
        logger.info(
            "CRC Bytes= 0x%02X,0x%02X,0x%02X,0x%02X,0x%02X,0x%02X,0x%02X" % (crc_byte[0], crc_byte[1], crc_byte[2],
                                                                                crc_byte[3], crc_byte[4], crc_byte[5],
                                                                                crc_byte[6]))
        logger.info("Calculated key= 0x%02X,0x%02X,0x%02X,0x%02X" % (self.calculatedKey[0], self.calculatedKey[1],
                                                                        self.calculatedKey[2],
                                                                        self.calculatedKey[3]))	
        
    def write_data_by_identifier_p_data(self,get_sub_data):
        # SID is 0x2E
        # self.data_info is dict
        # The specific relationship between did and non_default_diagnostic_session  will be updated later
        sid = Diagnostic_Sid.WRITEDATABYIDENTIFIER
        if self.non_default_diagnostic_session:
            sub_id = [get_sub_data[0],get_sub_data[1]]
            data_key = ((hex((sub_id[0] << 8)+sub_id[1]))[2:]).upper()
            if len(data_key) < 4 :
                data_key = "0"*(4 - len(data_key)) + data_key
            data = get_sub_data[2:]
            self.data_info[data_key] = data
            self.p_data = [sid + 0x40] + sub_id
        else:
            self.p_data = [0x7F,sid,0x22]     # Negative response
            logger.error("ECU is not in non_default_diagnostic_session ; NRC (0x22) :conditions Not Correct")
            
    def ecu_reset(self,get_sub_data):
        # SID is 0x11
        sid = Diagnostic_Sid.ECURESET
        sub_id = get_sub_data[0]
        self.p_data = [sid + 0x40] + [sub_id]
        
    def read_dtc_information(self,get_sub_data):
        # SID is 0x19
        dtc_status_availability_mask = [0x0F]
        sid = Diagnostic_Sid.READDTCINFORMATION
        sub_id = get_sub_data[0]
        self.all_dtc_code_data = []  
        if sub_id == 0x0A :
            for dtc_code_data in self.dtc_code.values():
                self.all_dtc_code_data = self.all_dtc_code_data + dtc_code_data
            self.p_data = [sid + 0x40] + [sub_id] + dtc_status_availability_mask + self.all_dtc_code_data
        elif sub_id == 0x01 :
            # provisional  dtc_status_availability_mask is 0x0F
            # DTCFormatIdentifier is ISO15031-6DTCFormat (0x00)
            dtc_format_identifier = [0x00]
            dtc_status_mask = get_sub_data[1]
            i = 0
            for dtc_code_data in self.dtc_code.values():
                if (dtc_code_data[-1:] & 0x0F & dtc_status_mask) :
                    i += 1
            dtc_count_h = i >> 8
            dtc_count_l = i & 0xFF
            dtc_count = [dtc_count_h] + [dtc_count_l]
            self.p_data = [sid + 0x40] + [sub_id] + dtc_status_availability_mask + dtc_format_identifier + dtc_count 
        elif sub_id == 0x02 :
            # provisional  dtc_status_availability_mask is 0x0F
            dtc_status_mask = get_sub_data[1]
            dtc_and_status_record = []
            for dtc_code_data in self.dtc_code.values():
                if (dtc_code_data[-1] & 0x0F & dtc_status_mask) :
                    dtc_and_status_record = dtc_and_status_record + dtc_code_data
            self.p_data = [sid + 0x40] + [sub_id] + dtc_status_availability_mask + dtc_and_status_record
    
    def clear_diagnostic_information(self,get_sub_data):
        # SID is 0x14
        sid = Diagnostic_Sid.CLEARDIAGNOSTICINFORMATION
        sub_id = list(get_sub_data)
        if sub_id == [0xFF , 0xFF , 0xFF] :
            self.p_data = [sid + 0x40]
        else:
            self.p_data = [0x7F , 0x14 , 0x31]
            logger.error("{} is request out range".format(sub_id))
            
    def routine_control(self,get_sub_data):
        # SID is 0x31
        sid = Diagnostic_Sid.ROUTINECONTROL
        routine_type = get_sub_data[0]
        rid = list(get_sub_data[1:3])

        data_key = ((hex((rid[0] << 8)+rid[1]))[2:]).upper()
        if len(data_key) < 4 :
            data_key = "0"*(4 - len(data_key)) + data_key
        rid_keys = self.routine_control_p_data.keys()
        if data_key in rid_keys:
            routine_type_keys = self.routine_control_p_data[data_key].keys()
            if routine_type in routine_type_keys :
                self.p_data = [sid + 0x40] + [routine_type] + rid + self.routine_control_p_data[data_key][routine_type]
            else :
                self.p_data = [sid + 0x40] + [routine_type] + rid
        else :
            self.p_data = [sid + 0x40] + [routine_type] + rid
                    
            
                
            
            

            
            
                    
            
            
        


            

        
            

            
    
            
        
            
            
        
