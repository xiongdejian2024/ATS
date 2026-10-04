from libTSCANAPI import *

import socket
import struct
import time
from time import sleep
from types import *
from threading import Thread
from multiprocessing import Process


class TLIBFlexrayHW(Structure):
    _pack_ = 1
    _fields_ = [("FHWIdx", c_int32),
                ("StopNet",c_int32),
                ("LogFlag",c_int32),
                ("AMsg", TLIBFlexray),
    ]
    def __str__(self):
        return str(self.FHWIdx) +"  "+str(self.AMsg)
PLIBFlexrayHW = POINTER(TLIBFlexrayHW)   

class TLIBCANFDHW(Structure):
    _pack_ = 1
    _fields_ = [("FHWIdx", c_int32),
                ("CyclicTime",c_float),
                ("LogFlag",c_int32),
                ("AMsg", TLIBCANFD),
    ]
    def __str__(self):
        return str(self.FHWIdx) +"  "+str(self.AMsg)
PLIBCANFDHW = POINTER(TLIBCANFDHW) 


class TosunBus():
    def __init__(self, host='127.0.0.1', port=8003):
        # set the host and port number
        self.host = host
        self.port = port
        self.rx_exit_flag = None
        self.tx_exit_flag = None

        # create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # connection to host on the port.
        self.client_socket.bind((self.host, self.port))

    def can_send(
            self,
            busname: str,
            data: list,
            msg_id: int,
            AChnIdx: int,
            cycle_time=None,
            LogFlag=0,
    ):  
        
        # data = msg_obj["pdu_data"]
        # msg_id = msg_obj["msg_id"]
        # length = msg_obj["msg_length"]
        # cycle_time = msg_obj["msg_cycle"]

        FFDProperties = 3 if "canfd" in busname else 0
        can_tx_frame = TLIBCANFD(
            FIdxChn=AChnIdx,
            FDLC=len(data),
            FIdentifier=msg_id,
            FProperties=1,
            FFDProperties=FFDProperties,
            FData=data,
        )

        can_tx_frame_HW = TLIBCANFDHW()
        can_tx_frame_HW.FHWIdx = 0
        if cycle_time is None:
            cycle_time = 0
        can_tx_frame_HW.CyclicTime = cycle_time
        can_tx_frame_HW.LogFlag = LogFlag
        can_tx_frame_HW.AMsg = can_tx_frame
        print(can_tx_frame_HW)

        self.client_socket.sendto(can_tx_frame_HW, (self.host, self.port - 1))
        # self.client_socket.sendto(can_tx_frame_HW, ("172.0.0.1", 8002))

    def fr_send(
            self,
            slot_id: int,
            cyclecode: int,
            data: list,
            IdxChn=0,
            ChannelMask=1,
            # ChannelMask=7,
            dlc=32,
            StopNet=0,
    ):  # #ChannelMask=3 两通道    ChannelMask=1 通道A   ChannelMask=7 把buffer发完，不跳帧
        fr_tx_frame = TLIBFlexray()
        fr_tx_frame.FIdxChn = IdxChn
        fr_tx_frame.FSlotId = slot_id
        fr_tx_frame.FCycleNumber = cyclecode
        fr_tx_frame.FChannelMask = ChannelMask
        fr_tx_frame.FActualPayloadLength = dlc

        for index in range(dlc):
            try:
                fr_tx_frame.FData[index] = data[index]
            except IndexError:
                fr_tx_frame.FData[index] = 0

        fr_tx_frame_HW = TLIBFlexrayHW()
        fr_tx_frame_HW.FHWIdx = 0
        fr_tx_frame_HW.StopNet = StopNet
        fr_tx_frame_HW.LogFlag = 0
        fr_tx_frame_HW.AMsg = fr_tx_frame
        # print(fr_tx_frame_HW)

        self.client_socket.sendto(fr_tx_frame_HW, (self.host, self.port - 1))
        # self.client_socket.sendto(fr_tx_frame_HW, ("172.0.0.1", 8000))

    def recv(self):
        msg, addr = self.client_socket.recvfrom(1024)
        if len(msg) >= 312:
            Msg_HW = cast(msg, PLIBFlexrayHW).contents
            Msg = Msg_HW.AMsg
            # print(Msg)

        else:
            Msg_HW = cast(msg, PLIBCANFDHW).contents
            Msg = Msg_HW.AMsg

        return Msg
    
    def recv_check_thread(self, chn=9, msg_id=0x11):
        self.rx_exit_flag = False
        i = 0
        while not self.rx_exit_flag:
            Msg = self.recv()
            if Msg.FIdxChn == chn and Msg.FIdentifier == msg_id:
                print(Msg)
                i = i + 1
                if i > 36000:
                    print(i)
        print(f"Rx i = {i}")
        print("====================== rx thread end ==============================")

    def recv_check_thread_strat(self, chn=9, msg_id=0x11):
        recv_thread = Process(target=self.recv_check_thread ,name="recv_check_thread", args=(chn, msg_id, ), daemon=True)
        # recv_thread = Thread(target=self.recv_check_thread ,name="recv_check_thread", args=(chn, msg_id, ), daemon=True)
        recv_thread.start()

    def recv_check_thread_close(self):
        self.rx_exit_flag = True

    def tx_thread(self, cantype="canfd", data=[0, 0, 0, 0, 0, 0, 0, 0], chn=9, msg_id=0x11, max_i=10000, cycle_time=0.01):
        self.tx_exit_flag = False
        i = 0
        while (i < max_i) and (not self.tx_exit_flag):
            self.can_send(cantype, data, msg_id, chn)
            
            sleep(cycle_time)
            i += 1
            print(f"Tx i = {i}")
        print("====================== tx thread end ==============================")

    def tx_thread_strat(self, cantype="canfd", data=[0, 0, 0, 0, 0, 0, 0, 0], chn=9, msg_id=0x11, max_i=10000, cycle_time=0.01):
        tx_thread = Thread(target=self.tx_thread ,name="tx_thread", args=(cantype, data, chn, msg_id, max_i, cycle_time, ), daemon=True)
        tx_thread.start()

    def tx_thread_close(self):
        self.tx_exit_flag = True


    def close(self):
        self.client_socket.close()
        print("=================测试结束========================")


def test_001():
    # linux 下的 RX 测试  20ms 周期
    tosun_can = TosunBus(port=8003)

    cycletime = 10000
    time1 = 0
    i = 0
    j_10 = 0
    j_50 = 0
    j_50_list = []
    j_50_time_list = []
    while i < 18000:
        Msg = tosun_can.recv()
        print(Msg)
    #     if Msg.FIdxChn == 9 and Msg.FIdentifier == 0x10:
    #         # print(Msg)

    #         # tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x11, 9)
    #         if time1:
    #             i += 1
    #             time2 = Msg.FTimeUs
    #             time3 = time2 - time1

    #             if time3 < cycletime*0.9 or time3 > cycletime*1.1:
    #                 print(time3)
    #                 j_10 += 1

    #                 if time3 < cycletime*0.5 or time3 > cycletime*1.5:
    #                     j_50 += 1
    #                     j_50_list.append(time3)
    #                     j_50_time_list.append((time3, time2))

    #             time1 = Msg.FTimeUs
    #         else:
    #             time1 = Msg.FTimeUs
    
    # print(f"偏差超过10%率： {j_10/i}")
    # print(f"偏差超过50%率： {j_50/i}")
    # print(f"偏差超过50% 具体偏差值列表： {j_50_list}")
    # print(f"偏差超过50% 具体偏差值和当前时间戳列表： {j_50_time_list}")

    tosun_can.close()

def test_002():
    # linux 下的 RX 测试  9路 bus  10ms 周期
    tosun_can = TosunBus(port=8003)

    time1 = 0
    i = 0
    j_10 = 0
    j_50 = 0
    j_50_list = []
    j_50_time_list = []
    while i < 10000:
        Msg = tosun_can.recv()

        if Msg.FIdxChn == 0 and Msg.FIdentifier == 0x11:
            # print(Msg)

            # tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x11, 9)
            if time1:
                i += 1
                time2 = Msg.FTimeUs
                time3 = time2 - time1

                if time3 <9000 or time3 > 11000:
                    print(time3)
                    j_10 += 1

                    if time3 < 5000 or time3 > 15000:
                        j_50 += 1
                        j_50_list.append(time3)
                        j_50_time_list.append((time3, time2))

                time1 = Msg.FTimeUs
            else:
                time1 = Msg.FTimeUs
    
    print(f"偏差超过10%率： {j_10/i}")
    print(f"偏差超过50%率： {j_50/i}")
    print(f"偏差超过50% 具体偏差值列表： {j_50_list}")
    print(f"偏差超过50% 具体偏差值和当前时间戳列表： {j_50_time_list}")

    tosun_can.close()

def test_007_1():
    # linux TC1034 TC1018下的 TXRX 测试
    tosun_can = TosunBus(port=8003)

    i = 0
    while i < 10000:
        tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x11, 9)
        sleep(0.01)
        print("11111111111111111111111111111")
        i += 1


    tosun_can.close()

def test_007_2():
    # linux TC1034 TC1018下的 TXRX 测试
    tosun_can = TosunBus(port=8003)

    time1 = 0
    i = 0
    j_10 = 0
    j_50 = 0
    j_50_list = []
    j_50_time_list = []
    while i < 10000:
        Msg = tosun_can.recv()

        if Msg.FIdxChn == 9 and Msg.FIdentifier == 0x50:
            print(Msg)

            # tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x11, 9)
            if time1:
                i += 1
                time2 = Msg.FTimeUs
                time3 = time2 - time1

                if time3 <9000 or time3 > 11000:
                    print(time3)
                    j_10 += 1

                    if time3 < 5000 or time3 > 15000:
                        length = Msg.FDLC
                        length = DLC_DATA_BYTE_CNT[length] 
                        # logger.info(length)
                        data = Msg.FData[:length]
                        j_50 += 1
                        j_50_list.append(time3)
                        j_50_time_list.append((time3, time2, data))
                        break

                time1 = Msg.FTimeUs
            else:
                time1 = Msg.FTimeUs
    
    print(f"偏差超过10%率： {j_10/i}")
    print(f"偏差超过50%率： {j_50/i}")
    print(f"偏差超过50% 具体偏差值列表： {j_50_list}")
    print(f"偏差超过50% 具体偏差值和当前时间戳列表： {j_50_time_list}")

    tosun_can.close()

def test_stop():
    # linux stop can fr 测试
    tosun_can = TosunBus(port=8003)

    sleep(10)

    tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x53F, 9, cycle_time=-1)
    print("====== stop can frme send  ======= ")
    sleep(10)

    tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x53F, 9, cycle_time=1)
    print("======   恢复 can frme send  ======= ")

    sleep(5)


    tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x53F, 9, cycle_time=-2)
    print("====== stop can bus send  ======= ")
    sleep(30)

    tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x53F, 9, cycle_time=1)
    print("======   恢复 can bus send  ======= ")

    sleep(5)

    tosun_can.close()

def test_stoplog():
    # linux stop can fr log 测试
    tosun_can = TosunBus(port=8003)

    sleep(2)

    tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x53F, 9, cycle_time=0, LogFlag=1)
    print("====== stop can log  ======= ")


    sleep(30)

    tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x53F, 9, cycle_time=0, LogFlag=0)
    print("====== start can log  ======= ")

    sleep(2)

    tosun_can.close()

def test_crc_cntr():
    # linux stop can fr log 测试
    tosun_can = TosunBus(port=8003)

    sleep(2)
    #  0x269    A2 24 18 24 71 24 00 00                                                                                                                                                                           

    tosun_can.can_send("canfd", [0, 0x2F, 0, 0, 0, 0, 0, 0], 0x269, 0, cycle_time=0)
    print("====== set cntr error  ======= ")


    sleep(20)

    tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x269, 0, cycle_time=0)
    print("====== 恢复 cntr  ======= ")

    sleep(10)

    tosun_can.can_send("canfd", [0xFF, 0, 0, 0, 0, 0, 0, 0], 0x269, 0, cycle_time=0)
    print("====== set crc error  ======= ")

    sleep(20)

    tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x269, 0, cycle_time=0)
    print("====== 恢复 crc error  ======= ")

    sleep(10)

    tosun_can.close()

def test_fr_send():
    tosun_can = TosunBus(port=8001)

    sleep(2)

    # while True:
    #     tosun_can.fr_send(55, 1, [0xFF, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    #     sleep(0.005)
    tosun_can.fr_send(57, 87, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xFF])
    # sleep(0.5)
    start_time = time.time()
    sleep(0.5)
    # print(start_time)
    while True:
        Msg = tosun_can.recv()
        if Msg.FSlotId == 57 and Msg.FCycleNumber == 23:
            print(Msg)
            tosun_can.fr_send(57, 87, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xFE])
            print(time.time())
    # tosun_can.fr_send(55, 1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    # sleep(10)

def test_fr_stop():
    tosun_can = TosunBus(port=8001)

    sleep(2)


    tosun_can.fr_send(55, 1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], StopNet=1)
    sleep(10)

    tosun_can.fr_send(55, 1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    sleep(10)
    # tosun_can.fr_send(55, 1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    # sleep(10)

def test_007_3():
    # linux TC1034 TC1018下的 TXRX 测试
    # tosun_fr = TosunBus(port=8001)
    tosun_can = TosunBus(port=8003)

    msg_cycle = 15000

    time1 = 0
    i = 0
    j_10 = 0
    j_50 = 0
    j_50_list = []
    j_50_time_list = []
    while i < 10000:
        Msg = tosun_can.recv()
        if Msg is None:
            continue

        # if Msg.FIdxChn == 0 and Msg.FIdentifier == 0x40:
        #     print(Msg)
        #     # pass

    #     print(Msg)
    #     if Msg.FIdxChn == 0 and Msg.FIdentifier == 0x40:
    #         # print(Msg)

    #         # tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x11, 9)
    #         if time1:
    #             i += 1
    #             time2 = Msg.FTimeUs
    #             time3 = time2 - time1

    #             if time3 < 0.9*msg_cycle or time3 > 1.1*msg_cycle:
    #                 print(time3)
    #                 j_10 += 1

    #                 if time3 < 0.5*msg_cycle or time3 > 1.5*msg_cycle:
    #                     j_50 += 1
    #                     j_50_list.append(time3)
    #                     j_50_time_list.append((time3, time2))

    #             time1 = Msg.FTimeUs
    #         else:
    #             time1 = Msg.FTimeUs
    
    # print(f"偏差超过10%率： {j_10/i}")
    # print(f"偏差超过50%率： {j_50/i}")
    # print(f"偏差超过50% 具体偏差值列表： {j_50_list}")
    # print(f"偏差超过50% 具体偏差值和当前时间戳列表： {j_50_time_list}")

    tosun_can.close()


def test_canlog_stop():
    # linux stop canlog 多次测试
    tosun_can = TosunBus(port=8003)

    sleep(2)
    
    # os.system("rm -rf /root/quansun_new/ecu-simulator/xat_ecu/legacy/sdk/driver/tosun/libTSCANAPI/linux/6.asc")
    # sleep(1)

    tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x53F, 9, cycle_time=0, LogFlag=0)
    print("====== start can log  ======= ")

    tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x53F, 9, cycle_time=0, LogFlag=1)
    print("====== stop can log  ======= ")


    sleep(10)

    tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x53F, 9, cycle_time=0, LogFlag=0)
    print("====== start can log  ======= ")

    sleep(5)

    tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x53F, 9, cycle_time=0, LogFlag=1)
    print("====== stop can log  ======= ")


    sleep(10)

    tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x53F, 9, cycle_time=0, LogFlag=0)
    print("====== start can log  ======= ")

    sleep(5)

    tosun_can.close()

def test_001_new():
    # linux 下的 RX 测试  主线程测试  一发一收
    tosun_can = TosunBus()

    cycletime = 10000
    time1 = 0
    i = 0
    j_10 = 0
    j_50 = 0
    j_50_list = []
    j_50_time_list = []
    while i < 100000:
        tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x11, 9)
        while True:
            Msg = tosun_can.recv()
            if Msg.FIdxChn == 9 and Msg.FIdentifier == 0x11:
                # print(Msg)
                print(i+1)
                break
        sleep(0.01)
        i += 1
        # Msg = tosun_can.recv()
        # print(Msg)
    #     if Msg.FIdxChn == 9 and Msg.FIdentifier == 0x10:
    #         print(Msg)

    #         # tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x11, 9)
    #         if time1:
    #             i += 1
    #             time2 = Msg.FTimeUs
    #             time3 = time2 - time1

    #             if time3 < cycletime*0.9 or time3 > cycletime*1.1:
    #                 print(time3)
    #                 j_10 += 1

    #                 if time3 < cycletime*0.5 or time3 > cycletime*1.5:
    #                     j_50 += 1
    #                     j_50_list.append(time3)
    #                     j_50_time_list.append((time3, time2))

    #             time1 = Msg.FTimeUs
    #         else:
    #             time1 = Msg.FTimeUs
    
    # print(f"偏差超过10%率： {j_10/i}")
    # print(f"偏差超过50%率： {j_50/i}")
    # print(f"偏差超过50% 具体偏差值列表： {j_50_list}")
    # print(f"偏差超过50% 具体偏差值和当前时间戳列表： {j_50_time_list}")

    sleep(3)
    tosun_can.close()
    print("======================end==============================")

def test_001_new_rx_thread():
    # linux 下的 线程测试  一发一收    线程收/进程收
    tosun_can = TosunBus()

    cycletime = 10000
    time1 = 0
    i = 0
    j_10 = 0
    j_50 = 0
    j_50_list = []
    j_50_time_list = []
    tosun_can.recv_check_thread_strat(9, 0x11)
    while i < 36500:
        tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0xFF], 0x11, 9)
        
        sleep(0.01)
        i += 1
        # print(f"i = {i}")
    print(f"Tx i = {i}")
    sleep(1)
    tosun_can.recv_check_thread_close()
    sleep(1)
    tosun_can.close()
    print("======================end==============================")

def test_001_new_tx_thread():
    # linux 下的 线程测试  一发一收    线程发
    tosun_can = TosunBus()

    cycletime = 10000
    time1 = 0
    i = 0
    j_10 = 0
    j_50 = 0
    j_50_list = []
    j_50_time_list = []
    tosun_can.tx_thread_strat(cantype="canfd", data=[0, 0, 0, 0, 0, 0, 0, 0], chn=9, msg_id=0x11, max_i=1000, cycle_time=0.01)
    while i < 1000:
        Msg = tosun_can.recv()
        if Msg.FIdxChn == 9 and Msg.FIdentifier == 0x11:
            # print(Msg)
            i = i+1
            print(f"Rx i = {i}")
        # print(Msg)

    sleep(1)
    tosun_can.tx_thread_close()
    sleep(1)
    tosun_can.close()
    print("======================end==============================")


if __name__=="__main__":
    # test_001()
    # test_002()
    test_007_1()
    # test_007_2()
    # test_stop()
    # test_stoplog()
    # test_crc_cntr()
    # test_fr_send()
    # test_fr_stop()
    # test_007_3()
    # test_canlog_stop()
    # test_001_new()
    # test_001_new_rx_thread()
    # test_001_new_tx_thread()
    
