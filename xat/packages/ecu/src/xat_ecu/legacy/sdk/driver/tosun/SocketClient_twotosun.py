from libTSCANAPI import *

import socket
import struct


class TLIBFlexrayHW(Structure):
    _pack_ = 1
    _fields_ = [("FHWIdx", c_int32),
                ("AMsg", TLIBFlexray),
    ]
    def __str__(self):
        return str(self.FHWIdx) +"  "+str(self.AMsg)
PLIBFlexrayHW = POINTER(TLIBFlexrayHW)   


class TLIBCANFDHW(Structure):
    _pack_ = 1
    _fields_ = [("FHWIdx", c_int32),
                ("CyclicTime",c_float),
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
            cycle_time=0,
    ):  

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
        can_tx_frame_HW.CyclicTime = cycle_time
        can_tx_frame_HW.AMsg = can_tx_frame

        self.client_socket.sendto(can_tx_frame_HW, (self.host, self.port - 1))
        # print(can_tx_frame)

    def recv(self):
        msg, addr = self.client_socket.recvfrom(1024)
        if(len(msg)>= 308):
            # Msg = cast(msg, PLIBFlexrayHW).contents
            # print(Msg)
            pass
        elif(len(msg) == 88):
            Msg_HW = cast(msg, PLIBCANFDHW).contents
            Msg = Msg_HW.AMsg

        return Msg


    def close(self):
        self.client_socket.close()
        print("=================测试结束========================")


if __name__=="__main__":
    tosun_can = TosunBus()
    tosun_can2 = TosunBus(port=8001)

    while True:
        Msg = tosun_can.recv()

        if Msg.FIdxChn == 9 and Msg.FIdentifier == 0x21:
            print(Msg)

            tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x11, 9)

        Msg2 = tosun_can2.recv()
        if Msg2.FIdxChn == 9 and Msg2.FIdentifier == 0x11:
            print(Msg2)

            # tosun_can.can_send("canfd", [0, 0, 0, 0, 0, 0, 0, 0], 0x11, 9)

    

    tosun_can.close()
    



