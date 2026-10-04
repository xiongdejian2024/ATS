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
    //读取LIN数据文件
    //输入文件名，该程序只支持ldat格式文件
    printf("Please input file name:");
    char FileName[512]={0};
    gets(FileName);
    //打开文件
    FILE *pReadFile=fopen(FileName,"rb"); //获取文件的指针
    if(pReadFile == NULL){
	    printf("Open file error!\n");
	    return -2;
    }
    fseek(pReadFile,256,0);//跳过256字节文件头
    //循环读取数据并将数据通过LIN总线发送出去
    while(!feof(pReadFile)){
        LIN_EX_MSG  LINMsg;
        ret = fread(&LINMsg,1,sizeof(LIN_EX_MSG),pReadFile);
        if(ret == sizeof(LIN_EX_MSG)){
            //需要转换下数据
            LINMsg.MsgType = (LINMsg.Reserve1>>2)&0x07;
            LINMsg.Timestamp = 10;
            LIN_EX_MSG LINOutMsg[10];
            ret = LIN_EX_MasterSync(DevHandle[DevIndex],LINMasterIndex,&LINMsg,LINOutMsg,1);
            if(ret < LIN_EX_SUCCESS){
                printf("MasterSync LIN failed!\n");
                return 0;
            }else{
                for(int i=0;i<ret;i++){
                    printf("%s SYNC[%02X] PID[%02X] ",MSGTypeStr[LINOutMsg[i].MsgType],LINOutMsg[i].Sync,LINOutMsg[i].PID);
                    for(int j=0;j<LINOutMsg[i].DataLen;j++){
                        printf("%02X ",LINOutMsg[i].Data[j]);
                    }
                    printf("[%s][%02X] [%02d:%02d:%02d.%03d]\n",CKTypeStr[LINOutMsg[i].CheckType],LINOutMsg[i].Check,(LINOutMsg[i].Timestamp/36000000)%60,(LINOutMsg[i].Timestamp/600000)%60,(LINOutMsg[i].Timestamp/10000)%60,(LINOutMsg[i].Timestamp/10)%1000);
                }
            }
        }else{
            break;
        }
    }
    fclose(pReadFile); // 关闭文件
	return 0;
}

