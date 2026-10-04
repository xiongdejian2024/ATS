  /*
  ******************************************************************************
  * @file     : USB2XXX_CAN_SchTest.cpp
  * @Copyright: TOOMOSS 
  * @Revision : ver 1.0
  * @Date     : 2019/12/19 9:33
  * @brief    : USB2XXX CAN test demo
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
#include "usb_device.h"
#include "usb2can.h"
/*
在运行程序前，请先将CAN总线接到有效CAN节点上，波特率为500K
*/
int main(int argc, const char* argv[])
{
    DEVICE_INFO DevInfo;
    int DevHandle[10];
    int SendCANIndex = 0;//发送CAN通道号
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
    //初始化配置CAN
    CAN_INIT_CONFIG CANConfig;
    CANConfig.CAN_Mode = 0x80;//正常模式
    CANConfig.CAN_ABOM = 0;//禁止自动离线
    CANConfig.CAN_NART = 0;//使能报文重传
    CANConfig.CAN_RFLM = 0;//FIFO满之后覆盖旧报文
    CANConfig.CAN_TXFP = 1;//发送请求决定发送顺序
    //配置波特率
    CANConfig.CAN_BRP = 4;
    CANConfig.CAN_BS1 = 15;
    CANConfig.CAN_BS2 = 5;
    CANConfig.CAN_SJW = 2;
    ret = CAN_Init(DevHandle[0],SendCANIndex,&CANConfig);
    if(ret != CAN_SUCCESS){
        printf("Config CAN failed!\n");
        return 0;
    }else{
        printf("Config CAN Success!\n");
    }
    //准备CAN调度表数据
    const int MsgNum = 20;
    CAN_MSG CanMsg[MsgNum];
    for(int i=0;i<MsgNum;i++){
        CanMsg[i].ExternFlag = 0;
        CanMsg[i].RemoteFlag = 0;
        CanMsg[i].ID = i+1;
        CanMsg[i].DataLen = 8;
        CanMsg[i].TimeStamp = 20;//帧周期为20ms，必须设置
        for(int j=0;j<CanMsg[i].DataLen;j++){
            CanMsg[i].Data[j] = j;
        }
        CanMsg[i].Data[0] = i+1;
    }
    //总共3个调度表，第一个表里面包含3帧数据，第二个调度表包含6帧数据，第三个调度表包含11帧数据
    uint8_t MsgTabNum[3]={3,6,11};
    //第一个调度表循环发送数据，第二个调度表循环发送数据，第三个调度表只发送3次
    uint16_t SendTimes[3]={0xFFFF,0xFFFF,3};
    ret = CAN_SetSchedule(DevHandle[0],0,CanMsg,MsgTabNum,SendTimes,3);
    if(ret == CAN_SUCCESS){
        printf("Set CAN Schedule Success\n");
    }else{
        printf("Set CAN Schedule Error ret = %d\n", ret);
        return 0;
    }
    ret = CAN_StartSchedule(DevHandle[0],SendCANIndex,0,10,0);//发送第一个调度表
    if(ret == CAN_SUCCESS){
        printf("Start CAN Schedule 1 Success\n");
    }else{
        printf("Start CAN Schedule 1 Error ret = %d\n", ret);
        return 0;
    }
    getchar();
    ret = CAN_StartSchedule(DevHandle[0],SendCANIndex,1,10,0);//发送第二个调度表
    if(ret == CAN_SUCCESS){
        printf("Start CAN Schedule 2 Success\n");
    }else{
        printf("Start CAN Schedule 2 Error ret = %d\n", ret);
        return 0;
    }
    getchar();
    ret = CAN_StartSchedule(DevHandle[0],SendCANIndex,2,10,0);//发送第三个调度表
    if(ret == CAN_SUCCESS){
        printf("Start CAN Schedule 3 Success\n");
    }else{
        printf("Start CAN Schedule 3 Error ret = %d\n", ret);
        return 0;
    }
    getchar();
    ret = CAN_StopSchedule(DevHandle[0], SendCANIndex);
    if(ret == CAN_SUCCESS){
        printf("Stop CAN Schedule Success\n");
    }else{
        printf("Stop CAN Schedule Error ret = %d\n", ret);
        return 0;
    }
    return 0;
}

