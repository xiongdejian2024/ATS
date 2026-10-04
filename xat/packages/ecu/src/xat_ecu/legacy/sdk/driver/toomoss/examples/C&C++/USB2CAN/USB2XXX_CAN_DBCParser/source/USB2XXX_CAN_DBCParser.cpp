  /*
  ******************************************************************************
  * @file     : USB2XXX_CAN_DBCParser.cpp
  * @Copyright: toomoss 
  * @Revision : ver 1.0
  * @Date     : 2022/03/31 9:33
  * @brief    : USB2XXX CAN DBC Parser test demo
  ******************************************************************************
  * @attention
  *
  * Copyright 2009-2022, toomoss.com
  * http://www.toomoss.com/
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
#include "dbc_parser.h"


int main(int argc, const char* argv[])
{
    DEVICE_INFO DevInfo;
    int DevHandle[10];
    int SendCANIndex = 0;//0-CAN1,1-CAN2
    int ReadCANIndex = 1;//0-CAN1,1-CAN2
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
    //解析DBC文件
    long long DBCHandle = DBC_ParserFile(DevHandle[0],"Common_DBC.dbc");
    if(DBCHandle==NULL){
        printf("Parser DBC File error!\n");
        return 0;
    }else{
        printf("Parser DBC File success!\n");
    }
    //打印DBC里面报文和信号相关信息
    int DBCMsgNum = DBC_GetMsgQuantity(DBCHandle);
    for(int i=0;i<DBCMsgNum;i++) {
        char MsgName[32]={0};
        DBC_GetMsgName(DBCHandle,i,MsgName);
        printf("Msg.Name = %s",MsgName);
        int DBCSigNum = DBC_GetMsgSignalQuantity(DBCHandle,MsgName);
        printf(" Signals:");
        for(int j=0;j<DBCSigNum;j++) {
            char SigName[32]={0};
            DBC_GetMsgSignalName(DBCHandle,MsgName,j,SigName);
            printf("%s ",SigName);
        }
        printf("\n");
    }
    //初始化配置CAN
    CAN_INIT_CONFIG CANConfig;
    ret = CAN_GetCANSpeedArg(DevHandle[0],&CANConfig,500000);
    if(ret != CAN_SUCCESS){
        printf("Get CAN Speed Arg Failed!\n");
        return 0;
    }else{
        printf("Get CAN Speed Arg Success!\n");
    }
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
    CAN_MSG CanMsg[3];
    //设置信号值
    DBC_SetSignalValue(DBCHandle,"msg_moto_speed","moto_speed",2412);
    DBC_SetSignalValue(DBCHandle,"msg_oil_pressure","oil_pressure",980);
    DBC_SetSignalValue(DBCHandle,"msg_speed_can","speed_can",120);
    //将信号值填入CAN消息里面
    DBC_SyncValueToCANMsg(DBCHandle,"msg_moto_speed",&CanMsg[0]);
    DBC_SyncValueToCANMsg(DBCHandle,"msg_oil_pressure",&CanMsg[1]);
    DBC_SyncValueToCANMsg(DBCHandle,"msg_speed_can",&CanMsg[2]);
    //发送CAN数据
    int SendedNum = CAN_SendMsg(DevHandle[0],SendCANIndex,CanMsg,3);
    if(SendedNum >= 0){
        printf("Success send frames:%d\n",SendedNum);
    }else{
        printf("Send CAN data failed! %d\n",SendedNum);
    }

    //另外一个CAN通道读取数据
    CAN_MSG CanMsgBuffer[10];
    int CanNum = CAN_GetMsg(DevHandle[0],ReadCANIndex,CanMsgBuffer);
    if(CanNum > 0){
        printf("CanNum = %d\n",CanNum);
        for(int i=0;i<CanNum;i++){
            printf("CanMsg[%d].ID = 0x%08X\n",i,CanMsgBuffer[i].ID);
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
    //将CAN消息数据填充到信号里面
    DBC_SyncCANMsgToValue(DBCHandle,CanMsgBuffer,CanNum);
    //获取信号值并打印出来
    char ValueStr[32];
    DBC_GetSignalValueStr(DBCHandle,"msg_moto_speed","moto_speed",ValueStr);
    printf("moto_speed = %s\n",ValueStr);
    DBC_GetSignalValueStr(DBCHandle,"msg_oil_pressure","oil_pressure",ValueStr);
    printf("oil_pressure = %s\n",ValueStr);
    DBC_GetSignalValueStr(DBCHandle,"msg_speed_can","speed_can",ValueStr);
    printf("speed_can = %s\n",ValueStr);

	return 0;
}

