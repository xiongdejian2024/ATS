"""
文件说明：USB2CANFD双通道CAN收发测试
更多帮助：www.toomoss.com
# 测试的是 UTA0503 固件：1.8.1
"""
from ctypes import *
import platform
from time import sleep
from usb_device import *
from usb2canfd import *
import time
import threading



if __name__ == '__main__':
    CAN1 = 0
    CAN2 = 1
    DevHandles = (c_uint * 20)()
    # Scan device
    ret = USB_ScanDevice(byref(DevHandles))
    if ret == 0:
        print("No device connected!")
        exit()
    else:
        print("Have %d device connected!" % ret)
    # Open device
    ret = USB_OpenDevice(DevHandles[0])
    if bool(ret):
        print("Open device success!")
    else:
        print("Open device faild!")
        exit()
    # Get device infomation
    USB2XXXInfo = DEVICE_INFO()
    USB2XXXFunctionString = (c_char * 256)()
    ret = DEV_GetDeviceInfo(
        DevHandles[0], byref(USB2XXXInfo), byref(USB2XXXFunctionString)
    )
    if bool(ret):
        print("USB2XXX device infomation:")
        print("--Firmware Name: %s" % bytes(USB2XXXInfo.FirmwareName).decode('ascii'))
        print(
            "--Firmware Version: v%d.%d.%d"
            % (
                (USB2XXXInfo.FirmwareVersion >> 24) & 0xFF,
                (USB2XXXInfo.FirmwareVersion >> 16) & 0xFF,
                USB2XXXInfo.FirmwareVersion & 0xFFFF,
            )
        )
        print(
            "--Hardware Version: v%d.%d.%d"
            % (
                (USB2XXXInfo.HardwareVersion >> 24) & 0xFF,
                (USB2XXXInfo.HardwareVersion >> 16) & 0xFF,
                USB2XXXInfo.HardwareVersion & 0xFFFF,
            )
        )
        print("--Build Date: %s" % bytes(USB2XXXInfo.BuildDate).decode('ascii'))
        print("--Serial Number: ", end='')
        for i in range(0, len(USB2XXXInfo.SerialNumber)):
            print("%08X" % USB2XXXInfo.SerialNumber[i], end='')
        print("")
        print(
            "--Function String: %s" % bytes(USB2XXXFunctionString.value).decode('ascii')
        )
    else:
        print("Get device infomation faild!")
        exit()
    # 初始化CAN
    CANConfig = CANFD_INIT_CONFIG()
    CANConfig.Mode = 0  # 1-自发自收模式，0-正常模式
    CANConfig.ISOCRCEnable = 1  # 0-禁止ISO CRC,1-使能ISO CRC
    CANConfig.RetrySend = 1
    CANConfig.ResEnable = 1
    # 配置波特率,波特率 = 40M/(BRP*(1+BS1+BS2))
    CANConfig.NBT_BRP = 1
    CANConfig.NBT_SEG1 = 59
    CANConfig.NBT_SEG2 = 20
    CANConfig.NBT_SJW = 2

    CANConfig.DBT_BRP = 1
    CANConfig.DBT_SEG1 = 14
    CANConfig.DBT_SEG2 = 5
    CANConfig.DBT_SJW = 2

    ret = CANFD_Init(DevHandles[0], CAN1, byref(CANConfig))
    if ret != CANFD_SUCCESS:
        print("Config CAN1 failed!")
        exit()
    else:
        print("Config CAN1 Success!")

    ret = CANFD_Init(DevHandles[0], CAN2, byref(CANConfig))
    if ret != CANFD_SUCCESS:
        print("Config CAN2 failed!")
        exit()
    else:
        print("Config CAN2 Success!")
    # 启动CAN接收数据
    ret = CANFD_StartGetMsg(DevHandles[0], CAN2)
    if ret != CANFD_SUCCESS:
        print("Start CAN2 failed!")
        exit()
    else:
        print("Start CAN2 Success!")
    # 发送CAN帧
    CanMsg = (CANFD_MSG * 5)()
    for i in range(0, 5):
        CanMsg[i].ID = i | CANFD_MSG_FLAG_IDE
        CanMsg[i].Flags = 0
        CanMsg[i].ID = i
        CanMsg[i].DLC = 8
        for j in range(0, CanMsg[i].DLC):
            CanMsg[i].Data[j] = (i << 4) | j

    # SendedNum = CANFD_SendMsg(DevHandles[0],CAN1,byref(CanMsg),5)
    # if SendedNum >= 0 :
    #     print("CAN1 success send frames:%d"%SendedNum)
    # else:
    #     print("Send CAN1 data failed!")

    ii = 0
    while ii < 100:
        CanMsg = (CANFD_MSG * 1)()
        CanMsg[0].Flags = 0
        CanMsg[0].ID = 0x409
        CanMsg[0].DLC = 8
        for j in range(0, CanMsg[0].DLC):
            CanMsg[0].Data[j] = (0 << 4) | j
        strat = time.time()
        SendedNum = CANFD_SendMsg(DevHandles[0], CAN1, byref(CanMsg), 1)
        end = time.time()
        a = end - strat
        print("--------------------{}-----------------------".format(a))

        if SendedNum >= 0:
            print("Success send frames:%d" % SendedNum)
        else:
            print("Send CAN data failed!")
        ii += 1
        sleep(0.25)

    # Delay
    sleep(0.5)
    # 读取CAN数据
    CanMsgBuffer = (CANFD_MSG * 10240)()
    CanNum = CANFD_GetMsg(DevHandles[0], CAN2, byref(CanMsgBuffer), 10240)
    if CanNum > 0:
        print("CAN2 CanNum = %d" % CanNum)
        for i in range(0, CanNum):
            print("CanMsg[%d].ID = %d" % (i, CanMsgBuffer[i].ID))
            print("CanMsg[%d].TimeStamp = %d" % (i, CanMsgBuffer[i].TimeStamp))
            print("CanMsg[%d].Data = " % i, end='')
            for j in range(0, CanMsgBuffer[i].DLC):
                print("%02X " % CanMsgBuffer[i].Data[j], end='')
            print("")
    elif CanNum == 0:
        print("No CAN2 data!")
    else:
        print("Get CAN2 data error!")
    # 停止CAN接收数据
    ret = CANFD_StopGetMsg(DevHandles[0], CAN2)
    if ret != CANFD_SUCCESS:
        print("Stop CAN2 failed!")
        exit()
    else:
        print("Stop CAN2 Success!")
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
