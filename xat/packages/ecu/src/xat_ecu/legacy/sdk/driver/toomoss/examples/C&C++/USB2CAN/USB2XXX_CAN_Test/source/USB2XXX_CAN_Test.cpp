  /*
  ******************************************************************************
  * @file     : USB2XXXCANTest.cpp
  * @Copyright: usbxyz 
  * @Revision : ver 1.0
  * @Date     : 2014/12/19 9:33
  * @brief    : USB2XXX IIC test demo
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
#include <windows.h>
#include "usb_device.h"
#include "usb2can.h"
#pragma comment(lib,"Winmm.lib")

#define GET_FIRMWARE_INFO   1
#define CAN_MODE_LOOPBACK   0
#define CAN_SEND_MSG        1
#define CAN_GET_MSG         1
#define CAN_GET_STATUS      0
#define CAN_SCH             0

void PASCAL OneMilliSecondProc(UINT wTimerID, UINT msg,DWORD dwUser,DWORD dwl,DWORD dw2)
{
    static CAN_MSG CanMsg;
    CanMsg.ID++;
    memset(&CanMsg,0,sizeof(CAN_MSG));
    CAN_SendMsg(dwUser,0,&CanMsg,1);
}

int main(int argc, const char* argv[])
{
#if GET_FIRMWARE_INFO
    DEVICE_INFO DevInfo;
#endif
    int DevHandle[10];
    int SendCANIndex = 0;//0-CAN1,1-CAN2
    int ReadCANIndex = 1;//0-CAN1,1-CAN2
    bool state;
    int ret;
    //打开dll文件编译日期
    char dllBuildDateTime[64]={0};
    DEV_GetDllBuildTime(dllBuildDateTime);
    printf("DLL Build Date Time = %s\n",dllBuildDateTime);
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
#if GET_FIRMWARE_INFO
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
#endif
    //初始化配置CAN,波特率为500000
    CAN_INIT_CONFIG CANConfig;
    ret = CAN_GetCANSpeedArg(DevHandle[0],&CANConfig,500000);
    if(ret != CAN_SUCCESS){
        printf("Get CAN Speed Arg Failed!\n");
        return 0;
    }else{
        printf("Get CAN Speed Arg Success!\n");
    }
#if CAN_MODE_LOOPBACK
    CANConfig.CAN_Mode = 1;//环回模式
#else
    CANConfig.CAN_Mode = 0x80;//正常模式
#endif
    ret = CAN_Init(DevHandle[0],SendCANIndex,&CANConfig);
    if(ret != CAN_SUCCESS){
        printf("Config CAN failed!\n");
        return 0;
    }else{
        printf("Config CAN Success!\n");
    }
    ret = CAN_Init(DevHandle[0],ReadCANIndex,&CANConfig);
    if(ret != CAN_SUCCESS){
        printf("Config CAN failed!\n");
        return 0;
    }else{
        printf("Config CAN Success!\n");
    }
    //配置过滤器，必须配置，否则可能无法收到数据
    CAN_FILTER_CONFIG CANFilter;
    CANFilter.Enable = 1;
    CANFilter.ExtFrame = 0;
    CANFilter.FilterIndex = 0;
    CANFilter.FilterMode = 0;
    CANFilter.MASK_IDE = 0;
    CANFilter.MASK_RTR = 0;
    CANFilter.MASK_Std_Ext = 0;
    ret = CAN_Filter_Init(DevHandle[0],ReadCANIndex,&CANFilter);
    if(ret != CAN_SUCCESS){
        printf("Config CAN Filter failed!\n");
        return 0;
    }else{
        printf("Config CAN Filter Success!\n");
    }
    //UINT TimerID = timeSetEvent(5, 1,(LPTIMECALLBACK)OneMilliSecondProc,DevHandle[0],TIME_PERIODIC);
    //Sleep(10000);
    //timeKillEvent(TimerID);
    //return 0;
#if CAN_SEND_MSG//发送CAN帧
    CAN_MSG CanMsg[5];
    for(int i=0;i<5;i++){
        CanMsg[i].ExternFlag = 0;
        CanMsg[i].RemoteFlag = 0;
        CanMsg[i].ID = i+1;
        CanMsg[i].DataLen = 8;
        for(int j=0;j<CanMsg[i].DataLen;j++){
            CanMsg[i].Data[j] = j;
        }
    }
    for(int t=0;t<10;t++){
        int SendedNum = CAN_SendMsg(DevHandle[0],SendCANIndex,CanMsg,5);
        if(SendedNum >= 0){
            printf("Success send frames:%d\n",SendedNum);
        }else{
            printf("Send CAN data failed! %d\n",SendedNum);
        }
    }
#endif
#if CAN_GET_STATUS
    CAN_STATUS CANStatus;
    ret = CAN_GetStatus(DevHandle[0],SendCANIndex,&CANStatus);
    if(ret == CAN_SUCCESS){
        printf("TSR = %08X\n",CANStatus.TSR);
        printf("ESR = %08X\n",CANStatus.ESR);
    }else{
        printf("Get CAN status error!\n");
    }
#endif
    //延时
#ifndef OS_UNIX
    Sleep(100);
#else
    usleep(100*1000);
#endif
#if CAN_GET_MSG
    CAN_MSG CanMsgBuffer[10240];
    int CanNum = CAN_GetMsg(DevHandle[0],ReadCANIndex,CanMsgBuffer);
    if(CanNum > 0){
        printf("CanNum = %d\n",CanNum);
        for(int i=0;i<CanNum;i++){
            printf("CanMsg[%d].ID = %d\n",i,CanMsgBuffer[i].ID);
            printf("CanMsg[%d].TimeStamp = %d\n",i,CanMsgBuffer[i].TimeStamp);
            printf("CanMsg[%d].Data = ",i);
            for(int j=0;j<CanMsgBuffer[i].DataLen;j++){
                printf("%02X ",CanMsgBuffer[i].Data[j]);
            }
            printf("\n");
        }
    }else if(CanNum == 0){
        printf("No CAN data!\n");
    }else{
        printf("Get CAN data error!\n");
    }
#endif
#if CAN_SCH
    CAN_MSG CanSchMsg[5];
    for(int i=0;i<5;i++){
        CanSchMsg[i].ExternFlag = 0;
        CanSchMsg[i].RemoteFlag = 0;
        CanSchMsg[i].ID = (i<<4)|(i+1);
        CanSchMsg[i].DataLen = 8;
        for(int j=0;j<CanMsg[i].DataLen;j++){
            CanSchMsg[i].Data[j] = j;
        }
        CanSchMsg[i].TimeStamp =10;//帧间隔时间为10ms,必须设置，若其中的某一帧数据该项为0，则这帧发送完毕后不会继续进行后续的数据发送了
    }
    ret = CAN_StartSchedule(DevHandle[0],SendCANIndex,CanSchMsg,5);
    if(ret == CAN_SUCCESS){
        printf("Start CAN Schedule Success!\n");
    }else{
        printf("Start CAN Schedule Failed!\n");
    }
    Sleep(10000);
    CAN_StopSchedule(DevHandle[0],SendCANIndex);
#endif

    //关闭设备
    USB_CloseDevice(DevHandle[0]);
	return 0;
}

