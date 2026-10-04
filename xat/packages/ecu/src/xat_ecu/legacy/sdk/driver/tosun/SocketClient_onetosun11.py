import random

from libTSCANAPI import *

import socket
import struct
import time
from time import sleep
from types import *


class TLIBFlexrayHW(Structure):
    _pack_ = 1
    _fields_ = [("FHWIdx", c_int32),
                ("StopNet", c_int32),
                ("LogFlag", c_int32),
                ("AMsg", TLIBFlexray),
                ]

    def __str__(self):
        return str(self.FHWIdx) + "  " + str(self.AMsg)


PLIBFlexrayHW = POINTER(TLIBFlexrayHW)


class TLIBCANFDHW(Structure):
    _pack_ = 1
    _fields_ = [("FHWIdx", c_int32),
                ("CyclicTime", c_float),
                ("LogFlag", c_int32),
                ("AMsg", TLIBCANFD),
                ]

    def __str__(self):
        return str(self.FHWIdx) + "  " + str(self.AMsg)


PLIBCANFDHW = POINTER(TLIBCANFDHW)


class TosunBus():
    def __init__(self, host='127.0.0.1', port=8003):
        # set the host and port number
        self.host = host
        self.port = port

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
        # print(can_tx_frame_HW)

        self.client_socket.sendto(can_tx_frame_HW, (self.host, self.port - 1))
        # self.client_socket_can.sendto(can_tx_frame_HW, ("127.0.0.1",8002))

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
        print(fr_tx_frame_HW)

        self.client_socket.sendto(fr_tx_frame_HW, (self.host, self.port - 1))
        # self.client_socket_fr.sendto(fr_tx_frame_HW, ("127.0.0.1",8000))

    def recv(self):
        msg, addr = self.client_socket.recvfrom(1024)
        if (len(msg) >= 316):
            # Msg = cast(msg, PLIBFlexrayHW).contents
            # print(Msg)
            pass
        else:
            Msg_HW = cast(msg, PLIBCANFDHW).contents
            Msg = Msg_HW.AMsg

        return Msg

    def close(self):
        self.client_socket.close()
        print("=================测试结束========================")


def test_001():
    # linux 下的 RX 测试  20ms 周期
    tosun_can = TosunBus()

    cycletime = 10000
    time1 = 0
    i = 0
    j_10 = 0
    j_50 = 0
    j_50_list = []
    j_50_time_list = []
    while i < 18000:
        Msg = tosun_can.recv()

        if Msg.FIdxChn == 9 and Msg.FIdentifier == 0x10:
            # print(Msg)

            # tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x11, 9)
            if time1:
                i += 1
                time2 = Msg.FTimeUs
                time3 = time2 - time1

                if time3 < cycletime * 0.9 or time3 > cycletime * 1.1:
                    print(time3)
                    j_10 += 1

                    if time3 < cycletime * 0.5 or time3 > cycletime * 1.5:
                        j_50 += 1
                        j_50_list.append(time3)
                        j_50_time_list.append((time3, time2))

                time1 = Msg.FTimeUs
            else:
                time1 = Msg.FTimeUs

    print(f"偏差超过10%率： {j_10 / i}")
    print(f"偏差超过50%率： {j_50 / i}")
    print(f"偏差超过50% 具体偏差值列表： {j_50_list}")
    print(f"偏差超过50% 具体偏差值和当前时间戳列表： {j_50_time_list}")

    tosun_can.close()


def test_002():
    # linux 下的 RX 测试  9路 bus  10ms 周期
    tosun_can = TosunBus()

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

                if time3 < 9000 or time3 > 11000:
                    print(time3)
                    j_10 += 1

                    if time3 < 5000 or time3 > 15000:
                        j_50 += 1
                        j_50_list.append(time3)
                        j_50_time_list.append((time3, time2))

                time1 = Msg.FTimeUs
            else:
                time1 = Msg.FTimeUs

    print(f"偏差超过10%率： {j_10 / i}")
    print(f"偏差超过50%率： {j_50 / i}")
    print(f"偏差超过50% 具体偏差值列表： {j_50_list}")
    print(f"偏差超过50% 具体偏差值和当前时间戳列表： {j_50_time_list}")

    tosun_can.close()


def test_007_1():
    # linux TC1034 TC1018下的 TXRX 测试
    tosun_can = TosunBus()

    i = 0
    while i < 10000:
        tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x11, 9)
        sleep(0.01)
        i += 1

    tosun_can.close()


def test_007_2():
    # linux TC1034 TC1018下的 TXRX 测试
    tosun_can = TosunBus(port=8001)

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

                if time3 < 9000 or time3 > 11000:
                    print(time3)
                    j_10 += 1

                    if time3 < 5000 or time3 > 15000:
                        j_50 += 1
                        j_50_list.append(time3)
                        j_50_time_list.append((time3, time2))

                time1 = Msg.FTimeUs
            else:
                time1 = Msg.FTimeUs

    print(f"偏差超过10%率： {j_10 / i}")
    print(f"偏差超过50%率： {j_50 / i}")
    print(f"偏差超过50% 具体偏差值列表： {j_50_list}")
    print(f"偏差超过50% 具体偏差值和当前时间戳列表： {j_50_time_list}")

    tosun_can.close()


def test_ltg():
    tosun_can = TosunBus()
    for index in range(1000):
        lis=[0x10, 0x08]+[random.randint(0,255) for _ in range(6)]
        lis2 = [0x21]+[random.randint(0, 255) for _ in range(7)]
        tosun_can.can_send("can",lis, 0x611, 0)
        print(f"第{index}次---send-{' '.join([hex(i)[2:].zfill(2) for i in lis]).upper()}------------")
        t = time.time()
        while time.time() - t < 2:
            Msg = tosun_can.recv()
            # print("Msg", Msg)
            if Msg.FIdxChn == 0 and Msg.FIdentifier == 0x711 and list(Msg.FData)[0] == 0x30:
                print("ltg", list(Msg.FData))
                print(f'第{index}次---send lis2-{" ".join([hex(i)[2:].zfill(2) for i in lis2])}------------')
                tosun_can.can_send("can", lis2, 0x611, 0)
                break
        else:
            print('11111')
            os.system("ps -ef | grep IniMap| awk '{print $2}' | xargs kill -9")
            break

    tosun_can.close()


def test_stop():
    # linux stop can fr 测试
    tosun_can = TosunBus()

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
    tosun_can = TosunBus()

    sleep(2)

    tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x53F, 9, cycle_time=0, LogFlag=1)
    print("====== stop can log  ======= ")

    sleep(50)

    tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x53F, 9, cycle_time=0, LogFlag=0)
    print("====== start can log  ======= ")

    sleep(2)

    tosun_can.close()


def test_crc_cntr():
    # linux stop can fr log 测试
    tosun_can = TosunBus()

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

    while True:
        tosun_can.fr_send(55, 1,
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0])
        sleep(0.001)
    # tosun_can.fr_send(55, 1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    # sleep(10)


def test_fr_stop():
    tosun_can = TosunBus(port=8001)

    sleep(2)

    tosun_can.fr_send(55, 1,
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      StopNet=1)
    sleep(10)

    tosun_can.fr_send(55, 1,
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    sleep(10)
    # tosun_can.fr_send(55, 1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    # sleep(10)


if __name__ == "__main__":
    # test_001()
    # test_002()
    # test_007_1()
    # test_007_2()
    # test_stop()
    # test_stoplog()
    # test_crc_cntr()
    # test_fr_send()
    # test_fr_stop()
    test_ltg()
