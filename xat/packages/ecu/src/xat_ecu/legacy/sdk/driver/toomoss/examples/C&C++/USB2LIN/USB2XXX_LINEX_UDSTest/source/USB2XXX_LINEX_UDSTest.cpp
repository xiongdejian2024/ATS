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
  * http://www.toomoss.com/
  * All Rights Reserved
  * 
  ******************************************************************************
  */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "usb_device.h"
#include "usb2lin_ex.h"
#include "lin_uds.h"

#define GET_FIRMWARE_INFO       1//获取固件信息

int main(int argc, const char* argv[])
{
#if GET_FIRMWARE_INFO
    DEVICE_INFO DevInfo;
#endif
    int DevHandle[10];
    int LINMasterIndex = 0;
    int LINSlaveIndex = 0;
    int DevIndex = 0;
    bool state;
    int ret;
    char *MSGTypeStr[]={"UN","MW","MR","SW","SR","BK","SY","ID","DT","CK"};
    char *CKTypeStr[]={"STD","EXT","USER","NONE","ERROR"};
    //扫描查找设备
    ret = USB_ScanDevice(DevHandle);
    if(ret <= 0){
        printf("No device connected!\n");
        return 0;
    }
    //打开设备
    state = USB_OpenDevice(DevHandle[DevIndex]);
    if(!state){
        printf("Open device error!\n");
        return 0;
    }
#if GET_FIRMWARE_INFO
    char FunctionStr[256]={0};
    //获取固件信息
    state = DEV_GetDeviceInfo(DevHandle[DevIndex],&DevInfo,FunctionStr);
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
        printf("Firmware SerialNumber:%08X%08X%08X\n",DevInfo.SerialNumber[0],DevInfo.SerialNumber[1],DevInfo.SerialNumber[2]);
    }
#endif
    //初始化配置LIN
    ret = LIN_EX_Init(DevHandle[DevIndex],LINMasterIndex,19200,1);
    if(ret != LIN_EX_SUCCESS){
        printf("Config LIN failed!\n");
        return 0;
    }else{
        printf("Config LIN Success!\n");
    }
    LIN_UDS_ADDR UDSAddr;
    UDSAddr.CheckType = 0;
    UDSAddr.NAD = 0x01;
    UDSAddr.ReqID = 0x3C;
    UDSAddr.ResID = 0x3D;
    UDSAddr.STmin = 5;
    uint8_t reqData[]={0x01,0x02,0x03};
    ret = LIN_UDS_Request(DevHandle[DevIndex],LINMasterIndex,&UDSAddr,reqData,sizeof(reqData));
    uint8_t resData[256];
    ret = LIN_UDS_Response(DevHandle[DevIndex],LINMasterIndex,&UDSAddr,resData,100);
    LIN_EX_MSG LINMsg[1000];
    ret = LIN_UDS_GetMsgFromUDSBuffer(DevHandle[DevIndex],LINMasterIndex,LINMsg,1000);
    printf("ret = %d\n",ret);
    for(int i=0;i<ret;i++){
        printf("[%d]%s SYNC[%02X] PID[%02X] ",i,MSGTypeStr[LINMsg[i].MsgType],LINMsg[i].Sync,LINMsg[i].PID);
        for(int j=0;j<LINMsg[i].DataLen;j++){
            printf("%02X ",LINMsg[i].Data[j]);
        }
        printf("[%s][%02X] [%02d:%02d:%02d.%03d]\n",CKTypeStr[LINMsg[i].CheckType],LINMsg[i].Check,(LINMsg[i].Timestamp/3600000)%60,(LINMsg[i].Timestamp/60000)%60,(LINMsg[i].Timestamp/1000)%60,(LINMsg[i].Timestamp)%1000);
    }
	return 0;
}

