  /*
  ******************************************************************************
  * @file     : USB2XXXLINTest.cpp
  * @Copyright: usbxyz 
  * @Revision : ver 1.0
  * @Date     : 2014/12/19 9:33
  * @brief    : USB2XXX LIN test demo
  ******************************************************************************
  * @attention
  *
  * Copyright 2009-2014, usbxyz.com
  * http://www.usbxyz.com/
  * All Rights Reserved
  * 
  ******************************************************************************
  */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "ldf_parser.h"
#include "usb_device.h"
#include "usb2lin_ex.h"

#define PRINT_LDF_INFO  1

int main(int argc, const char* argv[])
{
    int DevHandle[20];
    int ret = USB_ScanDevice(DevHandle);
    if (!USB_OpenDevice(DevHandle[0])) {
        printf("打开设备失败！\n");
        return 0;
    }
    printf("DevHandle = %08X\n", DevHandle[0]);
    long long LDFHandle = LDF_ParserFile(DevHandle[0],1,1, "example.ldf");
    if(LDFHandle == NULL)
    {
        printf("解析LDF文件失败\n");
        return 0;
    }
    printf("ProtocolVersion = %d\n", LDF_GetProtocolVersion(LDFHandle));
    printf("LINSpeed = %d\n", LDF_GetLINSpeed(LDFHandle));
    char MasterName[64];
    LDF_GetMasterName(LDFHandle, MasterName);
    printf("Master Name = %s\n", MasterName);
    int FrameLen = LDF_GetFrameQuantity(LDFHandle);
    for (int i = 0;i < FrameLen;i++) {
        char FrameName[64];
        if (LDF_PARSER_OK == LDF_GetFrameName(LDFHandle, i, FrameName)) {
            char PublisherName[64];
            LDF_GetFramePublisher(LDFHandle, FrameName, PublisherName);
            if (strcmp(MasterName, PublisherName) == 0) {
                //当前帧为主机发送数据帧
                printf("[MW]Frame[%d].Name=%s  Publisher=%s\n", i, FrameName, PublisherName);
            }
            else {
                //当前帧为主机读数据帧
                printf("[MR]Frame[%d].Name=%s  Publisher=%s\n", i, FrameName, PublisherName);
            }
            int SignalNum = LDF_GetFrameSignalQuantity(LDFHandle, FrameName);
            for (int j = 0;j < SignalNum;j++) {
                char SignalName[64];
                if (LDF_PARSER_OK == LDF_GetFrameSignalName(LDFHandle, FrameName, j, SignalName)) {
                    printf("\tSignal[%d].Name=%s\n", j, SignalName);
                }
            }
        }
    }
    //主机读操作，读取从机返回的数据值
    char ValueStr[64] = {0};
    LDF_ExeFrameToBus(LDFHandle, "ID_DATA",1);
    LDF_GetSignalValueStr(LDFHandle, "ID_DATA", "Supplier_ID", ValueStr);
    printf("ID_DATA.Supplier_ID=%s\n", ValueStr);
    LDF_GetSignalValueStr(LDFHandle, "ID_DATA", "Machine_ID", ValueStr);
    printf("ID_DATA.Machine_ID=%s\n", ValueStr);
    LDF_GetSignalValueStr(LDFHandle, "ID_DATA", "Chip_ID", ValueStr);
    printf("ID_DATA.Chip_ID=%s\n", ValueStr);
    //主机写操作，发送数据给从机
    LDF_SetSignalValue(LDFHandle, "LIN_CONTROL", "Reg_Set_Voltage", 13.5);
    LDF_SetSignalValue(LDFHandle, "LIN_CONTROL", "Ramp_Time", 3);
    LDF_SetSignalValue(LDFHandle, "LIN_CONTROL", "Cut_Off_Speed", 4);
    LDF_SetSignalValue(LDFHandle, "LIN_CONTROL", "Exc_Limitation", 15.6);
    LDF_SetSignalValue(LDFHandle, "LIN_CONTROL", "Derat_Shift", 2);
    LDF_SetSignalValue(LDFHandle, "LIN_CONTROL", "MM_Request", 2);
    LDF_SetSignalValue(LDFHandle, "LIN_CONTROL", "Reg_Blind", 1);
    //执行调度表
    LDF_ExeSchToBus(LDFHandle, "Nissan",1);
    LDF_GetSignalValueStr(LDFHandle, "LIN_STATE", "MM_State", ValueStr);
    printf("LIN_STATE.MM_State=%s\n", ValueStr);
    LDF_GetSignalValueStr(LDFHandle, "LIN_STATE", "Exc_Duty_Cycle", ValueStr);
    printf("LIN_STATE.Exc_Duty_Cycle=%s\n", ValueStr);
    LDF_GetSignalValueStr(LDFHandle, "LIN_STATE", "Exc_Current", ValueStr);
    printf("LIN_STATE.Exc_Current=%s\n", ValueStr);
    LDF_GetSignalValueStr(LDFHandle, "LIN_STATE", "iStARS_Voltage", ValueStr);
    printf("LIN_STATE.iStARS_Voltage=%s\n", ValueStr);
	return 0;
}

