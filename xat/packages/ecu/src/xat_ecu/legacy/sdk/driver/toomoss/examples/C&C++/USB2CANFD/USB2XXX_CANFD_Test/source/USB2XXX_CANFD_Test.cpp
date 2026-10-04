  /*
  ******************************************************************************
  * @file     : USB2XXX_CANFD_Test.cpp
  * @Copyright: TOOMOSS 
  * @Revision : ver 1.0
  * @Date     : 2019/12/19 9:33
  * @brief    : USB2XXX CANFD test demo
  ******************************************************************************
  * @attention
  *
  * Copyright 2009-2019, TOOMOSS
  * http://www.toomoss.com/
  * All Rights Reserved
  * 
  ******************************************************************************
  */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "offline_type.h"
#include "usb_device.h"
#include "usb2canfd.h"
/*
在运行程序前，请先将两个通道对接，也就是CAN1_H接CAN2_H，CAN1_L接CAN2_L
本程序实现CAN1发送数据，CAN2接收数据功能
若是向其他设备进行数据收发，注意波特率一定要匹配上
*/
int main(int argc, const char* argv[])
{
    DEVICE_INFO DevInfo;
    int DevHandle[10];
    int SendCANIndex = 0;//发送CAN通道号
    int ReceiveCANIndex = 1;//接收CAN通道号
    bool state;
    int ret;
    //扫描查找设备
    ret = USB_ScanDevice(DevHandle);
    if(ret <= 0){
        printf("No device connected!\n");
        return 0;
    }
    //打开设备
    state = USB_OpenDevice(DevHandle[0]);
    if(!state){
        printf("Open device error!\n");
        return 0;
    }
    char FunctionStr[256]={0};
    //获取固件信息
    state = DEV_GetDeviceInfo(DevHandle[0],&DevInfo,FunctionStr);
    if(!state){
        printf("Get device infomation error!\n");
        return 0;
    }else{
        printf("Firmware Info:\n");
	    printf("Firmware Name:%s\n",DevInfo.FirmwareName);
        printf("Firmware Build Date:%s\n",DevInfo.BuildDate);
        printf("Firmware Version:v%d.%d.%d\n",(DevInfo.FirmwareVersion>>24)&0xFF,(DevInfo.FirmwareVersion>>16)&0xFF,DevInfo.FirmwareVersion&0xFFFF);
        printf("Hardware Version:v%d.%d.%d\n",(DevInfo.HardwareVersion>>24)&0xFF,(DevInfo.HardwareVersion>>16)&0xFF,DevInfo.HardwareVersion&0xFFFF);
	    printf("Firmware Functions:%s\n",FunctionStr);
    }
    CANFD_INIT_CONFIG CANFDConfig;
    //填充初始化相关参数
    ret = CANFD_GetCANSpeedArg(DevHandle[0],&CANFDConfig,500000,2000000);
    if(ret != CANFD_SUCCESS){
        printf("CANFD Get Speed Error!\n");
        return 0;
    }else{
        printf("CANFD Get Speed Success!\n");
    }
    //初始化配置CAN
    CANFDConfig.ISOCRCEnable = 1;//使能ISOCRC
    CANFDConfig.ResEnable = 1;   //使能内部终端电阻（若总线上没有终端电阻，则必须使能终端电阻才能正常传输数据）
    ret = CANFD_Init(DevHandle[0],SendCANIndex,&CANFDConfig);//初始化发送通道
    if(ret != CANFD_SUCCESS){
        printf("CANFD Init Error!\n");
        return 0;
    }else{
        printf("CANFD Init Success!\n");
    }
    ret = CANFD_Init(DevHandle[0],ReceiveCANIndex,&CANFDConfig);//初始化接收通道
    if(ret != CANFD_SUCCESS){
        printf("CANFD Init Error!\n");
        return 0;
    }else{
        printf("CANFD Init Success!\n");
    }
    //启动CAN数据接收
    ret = CANFD_StartGetMsg(DevHandle[0], ReceiveCANIndex);
    if (ret != CANFD_SUCCESS){
        printf("Start receive CANFD failed!\n");
        return 0;
    }else{
        printf("Start receive CANFD Success!\n");
    }
    //发送CAN数据
    CANFD_MSG CanMsg[5];
    for (int i = 0; i < 5; i++){
        CanMsg[i].Flags = CANFD_MSG_FLAG_FDF;//bit[0]-BRS,bit[1]-ESI,bit[2]-FDF,bit[6..5]-Channel,bit[7]-RXD
        CanMsg[i].DLC = 16;
        CanMsg[i].ID = i|CANFD_MSG_FLAG_IDE;//配置为扩展帧
        for (int j = 0; j < CanMsg[i].DLC; j++){
            CanMsg[i].Data[j] = j;
        }
    }
    int SendedMsgNum = CANFD_SendMsg(DevHandle[0], SendCANIndex, CanMsg, 5);
    if (SendedMsgNum >= 0){
        printf("Success send frames:%d\n", SendedMsgNum);
    }else{
        printf("Send CAN data failed!\n");
        return 0;
    }
    //接收数据
    //延时
#ifndef OS_UNIX
    Sleep(50);
#else
    usleep(50*1000);
#endif
    //读取接收数据缓冲中的数据
    CANFD_MSG CanMsgBuffer[1024];
    int GetMsgNum = CANFD_GetMsg(DevHandle[0], ReceiveCANIndex, CanMsgBuffer, 1024);
    if (GetMsgNum > 0){
        for (int i = 0; i < GetMsgNum; i++){
            printf("CanMsg[%d].ID = 0x%08X\n", i, CanMsgBuffer[i].ID & CANFD_MSG_FLAG_ID_MASK);
            printf("CanMsg[%d].TimeStamp = %d\n", i, CanMsgBuffer[i].TimeStamp);
            printf("CanMsg[%d].Data = ", i);
            for (int j = 0; j < CanMsgBuffer[i].DLC; j++)
            {
                printf("0x%02X ", CanMsgBuffer[i].Data[j]);
            }
            printf("\n");
        }
    }else if (GetMsgNum < 0){
        printf("Get CAN data error!\n");
    }
    //停止接收数据
    ret = CANFD_StopGetMsg(DevHandle[0], SendCANIndex);
    if (ret != CANFD_SUCCESS){
        printf("Stop receive CANFD failed!\n");
        return 0;
    }else{
        printf("Stop receive CANFD Success!\n");
    }
    return 0;
}

