"""
文件说明：USB2CANFD双通道CAN收发测试
更多帮助：www.toomoss.com
宋雷测试用
"""
from ctypes import *
import platform
from time import sleep
from usb_device import *
from usb2canfd import *
import time
import threading
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def send_msg(can_msg, can, times=1):
    for i in range(0, times):
        SendedNum = CANFD_SendMsg(DevHandles[0], can, byref(can_msg), 1)
        time.sleep(0.1)
        if SendedNum >= 0 :
            # logger.info("Send CAN1 data successfully!")
            continue
        else:
            logger.info("Send CAN1 data failed!")

CanMsg_nm = (CANFD_MSG*1)()
CanMsg_nm.ID = 0x501
CanMsg_nm.Flags = 0
CanMsg_nm.DLC = 8
for i in range(0, CanMsg_nm[0].DLC):
    CanMsg_nm[0].Data[i] = 0xFF
CanMsg_nm[0].Data[0] = 0x01
CanMsg_nm[0].Data[1] = 0x40

CanMsg_usagemode = (CANFD_MSG*1)()
CanMsg_usagemode[0].ID = 0x120
CanMsg_usagemode[0].Flags = 0
CanMsg_usagemode[0].DLC = 8
for i in range(0, CanMsg_usagemode[0].DLC):
    CanMsg_usagemode[0].Data[i] = 0x0
CanMsg_usagemode[0].Data[3] = 0x01
CanMsg_usagemode[0].Data[4] = 0x01

CanMsg_rvi = (CANFD_MSG*1)()
CanMsg_rvi[0].ID = 0x180
CanMsg_rvi[0].Flags = 4
CanMsg_rvi[0].DLC = 16
for i in range(0, CanMsg_rvi[0].DLC):
    CanMsg_rvi[0].Data[i] = i

CanMsg_rviresp = (CANFD_MSG*1)()
CanMsg_rviresp[0].ID = 0x561
CanMsg_rviresp[0].Flags = 0
CanMsg_rviresp[0].DLC = 8
for i in range(0, CanMsg_rviresp[0].DLC):
    CanMsg_rviresp[0].Data[i] = 0x00
CanMsg_rviresp[0].Data[0] = 0x80

if __name__ == '__main__': 
    CAN1 = 0
    CAN2 = 1
    DevHandles = (c_uint * 20)()
    # Scan device
    ret = USB_ScanDevice(byref(DevHandles))
    if(ret == 0):
        print("No device connected!")
        exit()
    else:
        print("Have %d device connected!"%ret)
    # Open device
    ret = USB_OpenDevice(DevHandles[0])
    if(bool(ret)):
        print("Open device success!")
    else:
        print("Open device faild!")
        exit()
    # Get device infomation
    USB2XXXInfo = DEVICE_INFO()
    USB2XXXFunctionString = (c_char * 256)()
    ret = DEV_GetDeviceInfo(DevHandles[0],byref(USB2XXXInfo),byref(USB2XXXFunctionString))
    if(bool(ret)):
        print("USB2XXX device infomation:")
        print("--Serial Number: ",end='')
        for i in range(0, len(USB2XXXInfo.SerialNumber)):
            print("%08X"%USB2XXXInfo.SerialNumber[i],end='')
        print("")
        print("--Function String: %s"%bytes(USB2XXXFunctionString.value).decode('ascii'))
    else:
        print("Get device infomation faild!")
        exit()
    # 初始化CAN
    CANConfig = CANFD_INIT_CONFIG()
    CANConfig.Mode = 0          # 1-自发自收模式，0-正常模式
    CANConfig.ISOCRCEnable = 1  # 0-禁止ISO CRC,1-使能ISO CRC
    CANConfig.RetrySend = 1
    CANConfig.ResEnable = 1
    # 配置波特率,波特率 = 40M/(BRP*(1+BS1+BS2))
    CANConfig.NBT_BRP = 1;
    CANConfig.NBT_SEG1 = 59;
    CANConfig.NBT_SEG2 = 20;
    CANConfig.NBT_SJW = 2;

    CANConfig.DBT_BRP = 1;
    CANConfig.DBT_SEG1 = 14;
    CANConfig.DBT_SEG2 = 5;
    CANConfig.DBT_SJW = 2;

    ret = CANFD_Init(DevHandles[0],CAN1,byref(CANConfig))
    if(ret != CANFD_SUCCESS):
        print("Config CAN1 failed!")
        exit()
    else:
        print("Config CAN1 Success!")

    ret = CANFD_Init(DevHandles[0],CAN2,byref(CANConfig))
    if(ret != CANFD_SUCCESS):
        print("Config CAN2 failed!")
        exit()
    else:
        print("Config CAN2 Success!")
    # 启动CAN接收数据
    ret = CANFD_StartGetMsg(DevHandles[0],CAN2)
    if(ret != CANFD_SUCCESS):
        print("Start CAN2 failed!")
        exit()
    else:
        print("Start CAN2 Success!")
    # 发送CAN帧
    t = threading.Thread(target=send_msg, args=(CanMsg_nm, CAN1, 100000))
    t.start()
    t0 = threading.Thread(target=send_msg, args=(CanMsg_usagemode, CAN1, 100000))
    t0.start()

    # 读取CAN数据
    CanMsgBuffer = (CANFD_MSG*10240)()
    while True:
        CanNum = CANFD_GetMsg(DevHandles[0], CAN1, byref(CanMsgBuffer), 10240)
        # print("CAN1 CanNum = %d" % CanNum)
        if CanNum > 0:
            print("CAN1 CanNum = %d"%CanNum)
            for i in range(0,CanNum):
                if CanMsgBuffer[i].ID == 0x562:
                    logger.info("Here to send RVI chanllenge")
                    send_msg(CanMsg_rvi, 1)
                elif CanMsgBuffer[i].ID == 0x563:
                    logger.info("CAN Data: {0} #  {1} ".format(CanMsgBuffer[i].ID, CanMsgBuffer[i].Data))
                elif CanMsgBuffer[i].ID == 0x17F:
                    logger.info("Got the RVI response: {0} # {1}".format(CanMsgBuffer[i].ID, CanMsgBuffer[i].Data))
                    logger.info("Send RVI verify result: ")
                    send_msg(CanMsg_rviresp, 1)
        elif CanNum == 0:
            # logger.info("Get CAN1 no data!")
            continue
        else:
            logger.info("Get CAN1 data error!")
    # 停止CAN接收数据
    # ret = CANFD_StopGetMsg(DevHandles[0],CAN2)
    # if(ret != CANFD_SUCCESS):
    #     print("Stop CAN2 failed!")
    #     exit()
    # else:
    #     print("Stop CAN2 Success!")
'''
    # 发送CAN帧
    CanMsg = (CAN_MSG*5)()
    for i in range(0,5):
        CanMsg[i].ExternFlag = 0
        CanMsg[i].RemoteFlag = 0
        CanMsg[i].ID = i
        CanMsg[i].DataLen = 8
        for j in range(0,CanMsg[i].DataLen):
            CanMsg[i].Data[j] = (i<<4)|j
    SendedNum = CAN_SendMsg(DevHandles[0],CAN2,byref(CanMsg),5)
    if SendedNum >= 0 :
        print("CAN2 success send frames:%d"%SendedNum)
    else:
        print("Send CAN2 data failed!")
    # Delay
    sleep(0.5)
    # 读取CAN数据
    CanMsgBuffer = (CAN_MSG*10240)()
    CanNum = CAN_GetMsg(DevHandles[0],CAN1,byref(CanMsgBuffer))
    if CanNum > 0:
        print("CAN2 CanNum = %d"%CanNum)
        for i in range(0,CanNum):
            print("CanMsg[%d].ID = %d"%(i,CanMsgBuffer[i].ID))
            print("CanMsg[%d].TimeStamp = %d"%(i,CanMsgBuffer[i].TimeStamp))
            print("CanMsg[%d].Data = "%i,end='')
            for j in range(0,CanMsgBuffer[i].DataLen):
                print("%02X "%CanMsgBuffer[i].Data[j],end='')
            print("")
    elif CanNum == 0:
        print("No CAN1 data!")
    else:
        print("Get CAN1 data error!")
'''
