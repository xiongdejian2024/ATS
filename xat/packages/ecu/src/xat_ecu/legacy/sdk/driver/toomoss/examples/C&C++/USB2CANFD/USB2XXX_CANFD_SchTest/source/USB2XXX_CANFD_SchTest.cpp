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
在运行程序前，请先将CAN总线接到有效CAN节点上，仲裁域波特率为500K，数据域波特率为2M
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
    //初始化配置CAN
    CANFD_INIT_CONFIG CANFDConfig;
    //填充初始化相关参数
    ret = CANFD_GetCANSpeedArg(DevHandle[0],&CANFDConfig,500000,2000000);
    if(ret != CANFD_SUCCESS){
        printf("CANFD Get Speed Error!\n");
        return 0;
    }else{
        printf("CANFD Get Speed Success!\n");
    }
    CANFDConfig.ISOCRCEnable = 1;//使能ISOCRC
    CANFDConfig.ResEnable = 1;   //使能内部终端电阻（若总线上没有终端电阻，则必须使能终端电阻才能正常传输数据）
    ret = CANFD_Init(DevHandle[0],SendCANIndex,&CANFDConfig);//初始化发送通道
    if(ret != CANFD_SUCCESS){
        printf("CANFD Init Error!\n");
        return 0;
    }else{
        printf("CANFD Init Success!\n");
    }
    ret = CANFD_Init(DevHandle[0],ReceiveCANIndex,&CANFDConfig);
    if(ret != CANFD_SUCCESS){
        printf("CANFD Init Error!\n");
        return 0;
    }else{
        printf("CANFD Init Success!\n");
    }
    //准备CAN调度表数据
    const int AllMsgNum = 20;
    CANFD_MSG CanMsg[AllMsgNum];
    for (int i = 0; i < AllMsgNum; i++){
        CanMsg[i].Flags = 0;//bit[0]-BRS,bit[1]-ESI,bit[2]-FDF,bit[6..5]-Channel,bit[7]-RXD
        CanMsg[i].DLC = 8;
        CanMsg[i].ID = 0x123|CANFD_MSG_FLAG_IDE;
        for (int j = 0; j < CanMsg[i].DLC; j++){
            CanMsg[i].Data[j] = j;
        }
        CanMsg[i].Data[0] = i;
        CanMsg[i].TimeStamp = 100;//每帧间隔100ms
    }
    //总共1个调度表，表里面包含20帧数据
    uint8_t MsgTabNum[1]={AllMsgNum};
    //调度表循环发送数据
    uint16_t SendTimes[1]={0xFFFF};
    ret = CANFD_SetSchedule(DevHandle[0], SendCANIndex,CanMsg,MsgTabNum,SendTimes,1);//列表循环发送
    if(ret == CANFD_SUCCESS){
        printf("Set CAN Schedule Success\n");
    }else{
        printf("Set CAN Schedule Error ret = %d\n", ret);
        return 0;
    }
    ret = CANFD_StartSchedule(DevHandle[0],SendCANIndex,0,10,0);//发送第一个调度表
    if(ret == CANFD_SUCCESS){
        printf("Start CAN Schedule 1 Success\n");
    }else{
        printf("Start CAN Schedule 1 Error ret = %d\n", ret);
        return 0;
    }
    
    //启动另外一个通道检测调度表模式发送出来的数据
#if 0
    ret = CANFD_StartGetMsg(DevHandle[0],ReceiveCANIndex);
    if(ret == CANFD_SUCCESS){
        printf("Start CAN  Success\n");
    }else{
        printf("Start CAN  Error ret = %d\n", ret);
        return 0;
    }
    int t=1000;
    while(t--){
        CANFD_MSG CanMsgBuffer[1024];
        //printf("ret = %d\n",CANFD_GetMsg(DevHandle[0],1,MsgBuffer,1024));
        int GetMsgNum = CANFD_GetMsg(DevHandle[0],SendCANIndex,CanMsgBuffer,1024);
        if (GetMsgNum > 0){
            for (int i = 0; i < GetMsgNum; i++){
                printf("CanMsg[%d].ID = 0x%08X\n", i, CanMsgBuffer[i].ID & CANFD_MSG_FLAG_ID_MASK);
                //printf("CanMsg[%d].TimeStamp = %d\n", i, CanMsgBuffer[i].TimeStamp);
                printf("CanMsg[%d].Data = ", i);
                for (int j = 0; j < CanMsgBuffer[i].DLC; j++)
                {
                    printf("0x%02X ", CanMsgBuffer[i].Data[j]);
                }
                printf("\n");
            }
        }
        Sleep(10);
        //测试数据发送
        for(int i=0;i<5;i++){
            CanMsg[i].ID = (i<<8)|(i<<4)|i;
        }
        int SendedMsgNum = CANFD_SendMsg(DevHandle[0], SendCANIndex, CanMsg, 5);
        if (SendedMsgNum >= 0){
            printf("Success send frames:%d\n", SendedMsgNum);
        }else{
            printf("Send CAN data failed!\n");
            return 0;
        }
        SendedMsgNum = CANFD_SendMsg(DevHandle[0], ReceiveCANIndex, CanMsg, 5);
        if (SendedMsgNum >= 0){
            printf("Success send frames:%d\n", SendedMsgNum);
        }else{
            printf("Send CAN data failed!\n");
            return 0;
        }
    }
#endif
    /*getchar();
    ret = CANFD_StartSchedule(DevHandle[0],SendCANIndex,1,10,1);//发送第二个调度表
    if(ret == CANFD_SUCCESS){
        printf("Start CAN Schedule 2 Success\n");
    }else{
        printf("Start CAN Schedule 2 Error ret = %d\n", ret);
        return 0;
    }
    getchar();
    ret = CANFD_StartSchedule(DevHandle[0],SendCANIndex,2,10,0);//发送第三个调度表
    if(ret == CANFD_SUCCESS){
        printf("Start CAN Schedule 3 Success\n");
    }else{
        printf("Start CAN Schedule 3 Error ret = %d\n", ret);
        return 0;
    }*/
    getchar();
    ret = CANFD_StopSchedule(DevHandle[0], SendCANIndex);
    if(ret == CANFD_SUCCESS){
        printf("Stop CAN Schedule Success\n");
    }else{
        printf("Stop CAN Schedule Error ret = %d\n", ret);
        return 0;
    }
    return 0;
}

