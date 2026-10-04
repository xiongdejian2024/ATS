  /*
  ******************************************************************************
  * @file     : USB2XXX_LINEX_RelayTest.cpp.cpp
  * @Copyright: usbxyz 
  * @Revision : ver 1.0
  * @Date     : 2014/12/19 9:33
  * @brief    : USB2XXX LIN Relay test demo
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
#include "usb_device.h"
#include "mlx_programer.h"
#if defined(WIN32)
#include <sys/timeb.h>
#include <process.h>
#else
#include <sys/time.h>
#include <pthread.h>
#include <sys/types.h>
#endif

#define GET_FIRMWARE_INFO       1//获取固件信息

int main(int argc, const char* argv[])
{
#if GET_FIRMWARE_INFO
    DEVICE_INFO DevInfo;
#endif
    int DevHandleArray[10];
    int LINMasterIndex = 0;
    int DevIndex = 0;
    bool state;
    int ret;
    for(int i=0;i<argc;i++){
        printf("argv[%d]=%s\n",i,argv[i]);
    }
    //扫描查找设备
    ret = USB_ScanDevice(DevHandleArray);
    if(ret <= 0){
        printf("No device connected!\r\n");
        return 0;
    }
    //打开设备
    state = USB_OpenDevice(DevHandleArray[DevIndex]);
    if(!state){
        printf("Open device error!\r\n");
        return 0;
    }
#if GET_FIRMWARE_INFO
    char FunctionStr[256]={0};
    //获取固件信息
    state = DEV_GetDeviceInfo(DevHandleArray[DevIndex],&DevInfo,FunctionStr);
    if(!state){
        printf("Get device infomation error!\r\n");
        return 0;
    }else{
        printf("Firmware Info:\r\n");
	    printf("Firmware Name:%s\r\n",DevInfo.FirmwareName);
        printf("Firmware Build Date:%s\r\n",DevInfo.BuildDate);
        printf("Firmware Version:v%d.%d.%d\r\n",(DevInfo.FirmwareVersion>>24)&0xFF,(DevInfo.FirmwareVersion>>16)&0xFF,DevInfo.FirmwareVersion&0xFFFF);
        printf("Hardware Version:v%d.%d.%d\r\n",(DevInfo.HardwareVersion>>24)&0xFF,(DevInfo.HardwareVersion>>16)&0xFF,DevInfo.HardwareVersion&0xFFFF);
	    printf("Firmware Functions:%s\r\n",FunctionStr);
        printf("Firmware SerialNumber:%08X%08X%08X\r\n",DevInfo.SerialNumber[0],DevInfo.SerialNumber[1],DevInfo.SerialNumber[2]);
    }
#endif
    //初始化配置LIN
    ret = MLX_ProgInit(DevHandleArray[DevIndex],LINMasterIndex,40,0);
    if(ret != MLX_SUCCESS){
        printf("Config LIN failed!\r\n");
        return 0;
    }else{
        printf("Config LIN success!\r\n");
    }
    printf("Start Program Flash...\r\n");
    ret = MLX_ProgFlash(DevHandleArray[DevIndex],LINMasterIndex,"loaderB-81108_9C-lin2x-19200-loader.hex","81108_9C_Example_LIN2_1_PWM06_27_30_36_42_48.hex",0x7F);
    if(ret != MLX_SUCCESS){
        printf("Program Flash failed! %d\r\n",ret);
        return 0;
    }else{
        printf("Program Flash success!\r\n");
    }
    USB_CloseDevice(DevHandleArray[DevIndex]);
	return 0;
}

