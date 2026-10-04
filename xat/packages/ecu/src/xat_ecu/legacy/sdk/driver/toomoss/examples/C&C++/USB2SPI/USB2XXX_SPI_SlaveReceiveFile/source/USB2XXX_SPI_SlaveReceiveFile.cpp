  /*
  ******************************************************************************
  * @file     : USB2XXXSPISlaveReceiveFile.cpp
  * @Copyright: usbxyz 
  * @Revision : ver 1.0
  * @Date     : 2014/12/19 9:33
  * @brief    : USB2XXX SPI slave receive file test demo
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
#include "usb_device.h"
#include "usb2spi.h"
#include <vector>
#define USE_CALLBACK_RECEIVE_DATA   1
using namespace std;
FILE *pFile;
int FileSize = 0;
vector<uint8_t> SPI_DataBuffer;
int WINAPI SPI_SlaveStartContinueRead(int DevHandle,int SPIIndex);
int WINAPI SPI_SlaveStopContinueRead(int DevHandle,int SPIIndex);

#if USE_CALLBACK_RECEIVE_DATA
int __stdcall SlaveGetData(int DevHandle,int SPIIndex,unsigned char *pData,int DataNum)
{
    fwrite(pData,1,DataNum,pFile);
	FileSize += DataNum;
    return 0;
}
#endif

int main(int argc, const char* argv[])
{
    DEVICE_INFO DevInfo;
    SPI_CONFIG SPIConfig;
    int DevHandle[10];
    int SPIIndex = SPI1_CS0;
    bool state;
    int ret;
    unsigned char ReadBuffer[20480];
    //扫描查找设备
    ret = USB_ScanDevice(DevHandle);
    if(ret <= 0){
        printf("No device connected!\n");
        getchar();
        return 0;
    }
    //打开设备
    state = USB_OpenDevice(DevHandle[0]);
    if(!state){
        printf("Open device error!\n");
        getchar();
        return 0;
    }
    //获取固件信息
    char FunctionStr[512]={0};
    state = DEV_GetDeviceInfo(DevHandle[0],&DevInfo,FunctionStr);
    if(!state){
        printf("Get device infomation error!\n");
        getchar();
        return 0;
    }else{
	    printf("Firmware Name:%s\n",DevInfo.FirmwareName);
        printf("Firmware Build Date:%s\n",DevInfo.BuildDate);
        printf("Firmware Version:v%d.%d.%d\n",(DevInfo.FirmwareVersion>>24)&0xFF,(DevInfo.FirmwareVersion>>16)&0xFF,DevInfo.FirmwareVersion&0xFFFF);
        printf("Hardware Version:v%d.%d.%d\n",(DevInfo.HardwareVersion>>24)&0xFF,(DevInfo.HardwareVersion>>16)&0xFF,DevInfo.HardwareVersion&0xFFFF);
	    printf("Firmware Functions:%s\n",FunctionStr);
        printf("Firmware Serial Number:%08X%08X%08X\n",DevInfo.SerialNumber[0],DevInfo.SerialNumber[1],DevInfo.SerialNumber[2]);
    }
    //输入SPI相关参数，必须和主机匹配
    int DataTemp;
    printf("Please input CPHA(0 or 1):");
    scanf("%d",&DataTemp);
    SPIConfig.CPHA = DataTemp;
    printf("Please input CPOL(0 or 1):");
    scanf("%d",&DataTemp);
    SPIConfig.CPOL = DataTemp;
    printf("SPIConfig.CPHA = %d\n",SPIConfig.CPHA);
    printf("SPIConfig.CPOL = %d\n",SPIConfig.CPOL);
    //配置SPI总线相关参数(配置为从机模式)
    SPIConfig.Mode = SPI_MODE_HARD_HDX;
    SPIConfig.ClockSpeedHz = 50000000;
    //SPIConfig.CPHA = 0;
    //SPIConfig.CPOL = 0;
    SPIConfig.LSBFirst = SPI_MSB;
    SPIConfig.Master = SPI_SLAVE;
    SPIConfig.SelPolarity = SPI_SEL_LOW;
    ret = SPI_Init(DevHandle[0],SPIIndex,&SPIConfig);
    if(ret != SPI_SUCCESS){
        printf("Initialize device error!\n");
        getchar();
        return 0;
    }
    //输入文件名
    printf("Please input file name:");
    char FileName[512]={0};
    scanf("%s",FileName);
    printf("Start receive data to file,the file name is %s\n",FileName);
    printf("Press any key to exit the data reception!\n");
    pFile=fopen(FileName,"wb"); //获取文件的指针
    if(pFile == NULL){
        printf("Open file faild\n");
        getchar();
        return 0;
    }
#if USE_CALLBACK_RECEIVE_DATA
    SPI_SlaveContinueRead(DevHandle[0],SPIIndex,SlaveGetData);
    getchar();
    getchar();
#else
    SPI_SlaveContinueRead(DevHandle[0],SPIIndex,NULL);
    while(FileSize<(94862114))
    {
        unsigned char DataBuffer[40960+20480];
        int DataNum = SPI_SlaveGetBytes(DevHandle[0],SPIIndex,DataBuffer,sizeof(DataBuffer));
        if(DataNum > 0){
            fwrite(DataBuffer,1,DataNum,pFile);
            FileSize += DataNum;
            //printf("Get data num = %d\n",DataNum);
            //printf("FileSize = %d Byte\n",FileSize);
        }else if(DataNum < 0){
            break;
        }
        //延时
#ifndef OS_UNIX
        Sleep(10);
#else
        usleep(10*1000);
#endif
    }
#endif
    SPI_SlaveContinueWriteReadStop(DevHandle[0],SPIIndex);
    fclose(pFile);
    printf("FileSize = %d Byte\n",FileSize);
    printf("Stop receive!\n");
    getchar();
    return 0;
}
