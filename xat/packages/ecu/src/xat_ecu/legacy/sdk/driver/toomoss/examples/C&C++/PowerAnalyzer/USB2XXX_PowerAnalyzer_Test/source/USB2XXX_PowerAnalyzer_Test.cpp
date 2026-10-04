  /*
  ******************************************************************************
  * @file     : USB2XXX_PowerAnalyzer_Test.cpp
  * @Copyright: toomoss 
  * @Revision : ver 1.0
  * @Date     : 2021/3/31 9:33
  * @brief    : PowerAnalyzer test demo
  ******************************************************************************
  * @attention
  *
  * Copyright 2009-2014, toomoss.com
  * http://www.toomoss.com/
  * All Rights Reserved
  * 
  ******************************************************************************
  */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include "usb_device.h"
#include "power_analyzer.h"
//若提示找不到USB2XXX.dll文件，请将libs目录下的dll复制到exe文件输出目录
int main(int argc, const char* argv[])
{
    DEVICE_INFO DevInfo;
    int DevHandleArray[10];
    int DevHandle=0;
    bool state;
    int ret;
    //扫描查找设备
    ret = USB_ScanDevice(DevHandleArray);
    if(ret <= 0){
        printf("No device connected!\n");
        return 0;
    }
    for(int i=0;i<ret;i++){
        if((DevHandleArray[i]&0xFF000000)==0x61000000){
            DevHandle = DevHandleArray[i];
            break;
        }
    }
    if(DevHandle==0){
        printf("No power analyzer device connected!\n");
    }
    //打开设备
    state = USB_OpenDevice(DevHandle);
    if(!state){
        printf("Open device error!\n");
        return 0;
    }
    //获取固件信息
    char FuncStr[256]={0};
    state = DEV_GetDeviceInfo(DevHandle,&DevInfo,FuncStr);
    if(!state){
        printf("Get device infomation error!\n");
        return 0;
    }else{
        printf("Firmware Info:\n");
        printf("    Name:%s\n",DevInfo.FirmwareName);
        printf("    Build Date:%s\n",DevInfo.BuildDate);
        printf("    Firmware Version:v%d.%d.%d\n",(DevInfo.FirmwareVersion>>24)&0xFF,(DevInfo.FirmwareVersion>>16)&0xFF,DevInfo.FirmwareVersion&0xFFFF);
        printf("    Hardware Version:v%d.%d.%d\n",(DevInfo.HardwareVersion>>24)&0xFF,(DevInfo.HardwareVersion>>16)&0xFF,DevInfo.HardwareVersion&0xFFFF);
        printf("    Functions:%08X\n",DevInfo.Functions);
        printf("    Functions:%s\n",FuncStr);
    }
    //初始化功耗分析仪
    ret = PA_Init(DevHandle,0,10000,1,1,500);
    if(ret != PA_SUCCESS){
        printf("Power analyzer initialize error!\n");
        return 0;
    }
    //启动分析仪，开始接收数据
    ret = PA_StartGetData(DevHandle,0);
    if(ret != PA_SUCCESS){
        printf("Power analyzer start error!\n");
        return 0;
    }
    //循环获取数据并打印输出
    for(int i=0;i<1000;i++){
        double Voltage[10000];
        double Current[10000];
        double Power[10000];
        int VoltageDataNum = PA_GetVoltageData(DevHandle,0,Voltage,10000);
        int CurrentDataNum = PA_GetCurrentData(DevHandle,0,Current,10000);
        int PowerDataNum = PA_GetPowerData(DevHandle,0,Power,10000);
        int DataNum = min(min(VoltageDataNum,CurrentDataNum),PowerDataNum);
        if(DataNum > 0){
            printf("Voltage = %.3fmV\tCurrent = %.3fmA\tPower=%.3fmW\n",Voltage[0],Current[0],Power[0]);
        }
        //延时
#ifndef OS_UNIX
        Sleep(10);
#else
        usleep(10*1000);
#endif
    }
    //停止接收数据
    ret = PA_StopGetData(DevHandle,0);
    if(ret != PA_SUCCESS){
        printf("Power analyzer stop error!\n");
        return 0;
    }
}