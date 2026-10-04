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
#include "usb2lin_ex.h"
#if defined(WIN32)
#include <sys/timeb.h>
#include <process.h>
#else
#include <sys/time.h>
#include <pthread.h>
#include <sys/types.h>
#endif

#define GET_FIRMWARE_INFO       1//获取固件信息

/**
程序功能：实现LIN1和LIN2的中继功能，LIN1配置为从机，接到主机端；LIN2配置为主机，接到从机端
中继规则：
1，LIN1收到数据后，将数据通过LIN2转发出去
2，LIN2通过ID(0x01)向外部从机定时读取数据，并将读到的数据配置到LIN1的ID(0x01)中
*/
#ifdef OS_UNIX
static pthread_t LIN_RelayThreadHandle=(pthread_t)0xFFFFFFFF;  /* 记录线程ID号 */
#else
unsigned int LIN_RelayThreadID=0;  /* 记录线程ID号 */
HANDLE LIN_RelayThreadHandle=NULL;  /* 记录线程句柄 */
#endif
unsigned int WINAPI LIN_RelayThread( void* threadArg );
bool ThreadRunFlag = false;
char *MSGTypeStr[]={"UN","MW","MR","SW","SR","BK","SY","ID","DT","CK"};
char *CKTypeStr[]={"STD","EXT","USER","NONE","ERROR"};
int main(int argc, const char* argv[])
{
#if GET_FIRMWARE_INFO
    DEVICE_INFO DevInfo;
#endif
    int DevHandle[10];
    int LINMasterIndex = 1;
    int LINSlaveIndex = 0;
    int DevIndex = 0;
    bool state;
    int ret;
    //扫描查找设备
    ret = USB_ScanDevice(DevHandle);
    if(ret <= 0){
        printf("No device connected!\r\n");
        return 0;
    }
    //打开设备
    state = USB_OpenDevice(DevHandle[DevIndex]);
    if(!state){
        printf("Open device error!\r\n");
        return 0;
    }
#if GET_FIRMWARE_INFO
    char FunctionStr[256]={0};
    //获取固件信息
    state = DEV_GetDeviceInfo(DevHandle[DevIndex],&DevInfo,FunctionStr);
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
    //初始化配置LIN从机端
    ret = LIN_EX_Init(DevHandle[DevIndex],LINSlaveIndex,19200,0);
    if(ret != LIN_EX_SUCCESS){
        printf("Config LIN slave failed!\r\n");
        return 0;
    }else{
        printf("Config LIN slave success!\r\n");
    }
    //将ID(0x01)配置为从机写数据模式，以便向主机返回数据
    LIN_EX_MSG SlaveRespMsg;
    SlaveRespMsg.BreakBits = 13;
    SlaveRespMsg.CheckType = 1; //增强校验
    SlaveRespMsg.DataLen = 8;   //返回数据字节数
    SlaveRespMsg.PID = 0x01;
    SlaveRespMsg.MsgType = LIN_EX_MSG_TYPE_SW;//配置为从机写数据模式
    //填充数据
    for(int i=0;i<SlaveRespMsg.DataLen;i++){
        SlaveRespMsg.Data[i] = i;
    }
    ret = LIN_EX_SlaveSetIDMode(DevHandle[DevIndex],LINSlaveIndex,&SlaveRespMsg,1);
    if(ret != LIN_EX_SUCCESS){
        printf("Config LIN slave mode failed!\r\n");
        return 0;
    }else{
        printf("Config LIN slave mode success!\r\n");
    }
    //初始化配置LIN1
    ret = LIN_EX_Init(DevHandle[DevIndex],LINMasterIndex,19200,1);
    if(ret != LIN_EX_SUCCESS){
        printf("Config LIN master failed!\r\n");
        return 0;
    }else{
        printf("Config LIN master success!\r\n");
    }
    //启动数据中继线程，控制台输入回车结束程序
    ThreadRunFlag = true;
#ifdef OS_UNIX
        int ret = pthread_create(&LIN_RelayThreadHandle,NULL,(void*(*)(void*))LIN_RelayThread,(void*)&DeviceHandle[DevIndex]);
        if(ret){
            printf("Create thread error!\r\n");
            return 0;
        }
#else
        LIN_RelayThreadHandle = (HANDLE)_beginthreadex(NULL,0,&LIN_RelayThread,&DevHandle[DevIndex],0,&LIN_RelayThreadID);
        if(LIN_RelayThreadHandle == NULL ){
            printf("Create thread error!\r\n");
            return 0;
        }
#endif
        //控制器输入小写字母q并按下回车后退出程序
        printf("Enter 'q' exit...\r\n");
        while(1){
            char DataTemp;
            scanf("%c",&DataTemp);
            if(DataTemp=='q'){
                break;
            }
        }
        ThreadRunFlag = false;
#ifdef OS_UNIX
        if(LIN_RelayThreadHandle == (pthread_t)0xFFFFFFFF){
            return 0;
        }
        pthread_join(LIN_RelayThreadHandle, NULL);
#else
        if(LIN_RelayThreadHandle == NULL){
            return 0;
        }
        WaitForSingleObject(LIN_RelayThreadHandle, 1000);
#endif
#if LIN_MASTER_TEST
    LIN_EX_MSG LINMsg[5];
    LIN_EX_MSG LINOutMsg[10];
    unsigned int MsgLen = 5;
    LINMsg[0].MsgType = LIN_EX_MSG_TYPE_BK;
    LINMsg[0].Timestamp = 10;//发送该帧数据之后的延时时间，最小建议设置为1
    //后面4个ID全部为主机发送数据模式
    for(int f=1;f<MsgLen;f++){
        LINMsg[f].MsgType = LIN_EX_MSG_TYPE_MW;//主机写数据模式
        LINMsg[f].DataLen = 8;
        for(int i=0;i<LINMsg[1].DataLen;i++){
            LINMsg[f].Data[i] = (f<<4)|i;
        }
        LINMsg[f].Timestamp = 10;//发送该帧数据之后的延时时间，最小建议设置为1
        LINMsg[f].CheckType = LIN_EX_CHECK_EXT;//设置好校验类型后，适配器会根据校验类型自动计算校验数据
        LINMsg[f].PID = f+1;
    }
    ret = LIN_EX_MasterSync(DevHandle[DevIndex],LINMasterIndex,LINMsg,LINOutMsg,MsgLen);
    if(ret < LIN_EX_SUCCESS){
        printf("MasterSync LIN failed!\n");
        return 0;
    }else{
        printf("MsgLen = %d\n",ret);
        for(int i=0;i<ret;i++){
            printf("%s SYNC[%02X] PID[%02X] ",MSGTypeStr[LINOutMsg[i].MsgType],LINOutMsg[i].Sync,LINOutMsg[i].PID);
            for(int j=0;j<LINOutMsg[i].DataLen;j++){
                printf("%02X ",LINOutMsg[i].Data[j]);
            }
            printf("[%s][%02X] [%02d:%02d:%02d.%03d]\n",CKTypeStr[LINOutMsg[i].CheckType],LINOutMsg[i].Check,(LINOutMsg[i].Timestamp/36000000)%60,(LINOutMsg[i].Timestamp/600000)%60,(LINOutMsg[i].Timestamp/10000)%60,(LINOutMsg[i].Timestamp/10)%1000);
        }
    }
    //后面4个ID全部为主机读数据模式
    for(int f=1;f<MsgLen;f++){
        LINMsg[f].MsgType = LIN_EX_MSG_TYPE_MR;//主机读数据模式
        LINMsg[f].Timestamp = 10;//主机读取完数据之后的延时时间，最小建议设置为1
        LINMsg[f].PID = f+1;
    }
    ret = LIN_EX_MasterSync(DevHandle[DevIndex],LINMasterIndex,LINMsg,LINOutMsg,MsgLen);
    if(ret < LIN_EX_SUCCESS){
        printf("MasterSync LIN failed!\n");
        return 0;
    }else{
        printf("MsgLen = %d\n",ret);
        for(int i=0;i<ret;i++){
            printf("%s SYNC[%02X] PID[%02X] ",MSGTypeStr[LINOutMsg[i].MsgType],LINOutMsg[i].Sync,LINOutMsg[i].PID);
            for(int j=0;j<LINOutMsg[i].DataLen;j++){
                printf("%02X ",LINOutMsg[i].Data[j]);
            }
            printf("[%s][%02X] [%02d:%02d:%02d.%03d]\n",CKTypeStr[LINOutMsg[i].CheckType],LINOutMsg[i].Check,(LINOutMsg[i].Timestamp/36000000)%60,(LINOutMsg[i].Timestamp/600000)%60,(LINOutMsg[i].Timestamp/10000)%60,(LINOutMsg[i].Timestamp/10)%1000);
        }
    }
#endif

#if LIN_SLAVE_TEST
    //初始化配置LIN
    ret = LIN_EX_Init(DevHandle[DevIndex],LINSlaveIndex,9600,0);
    if(ret != LIN_EX_SUCCESS){
        printf("Config LIN failed!\n");
        return 0;
    }else{
        printf("Config LIN Success!\n");
    }
    printf("Start Get LIN Data...\n");
    //设置ID为LIN_EX_MSG_TYPE_SW模式，这样主机就可以读取到数据
    LIN_EX_MSG LINSlaveMsg[10];
    for(int i=0;i<10;i++){
        LINSlaveMsg[i].PID = i;
        LINSlaveMsg[i].CheckType = LIN_EX_CHECK_EXT;
        LINSlaveMsg[i].DataLen = 7;
        for(int j=0;j<LINSlaveMsg[i].DataLen;j++){
            LINSlaveMsg[i].Data[j]=(i<<4)|j;
        }
        LINSlaveMsg[i].MsgType = LIN_EX_MSG_TYPE_SW;//从机发送数据模式
    }
    ret = LIN_EX_SlaveSetIDMode(DevHandle[DevIndex],LINSlaveIndex,LINSlaveMsg,10);
    if(ret != LIN_EX_SUCCESS){
        printf("Config LIN ID Mode failed!\n");
        return 0;
    }else{
        printf("Config LIN ID Mode Success!\n");
    }
    //循环获取接收到的数据，该操作可以用作LIN总线数据监控
    while(1)
    {
        LIN_EX_MSG LINMsg[1024];//缓冲区尽量大一点，防止益处
        int ret = LIN_EX_SlaveGetData(DevHandle[DevIndex],LINSlaveIndex,LINMsg);
        for(int i=0;i<ret;i++){
            printf("%s SYNC[%02X] PID[%02X] ",MSGTypeStr[LINMsg[i].MsgType],LINMsg[i].Sync,LINMsg[i].PID);
            for(int j=0;j<LINMsg[i].DataLen;j++){
                printf("%02X ",LINMsg[i].Data[j]);
            }
            printf("[%s][%02X] [%02d:%02d:%02d.%03d]\n",CKTypeStr[LINMsg[i].CheckType],LINMsg[i].Check,(LINMsg[i].Timestamp/36000000)%60,(LINMsg[i].Timestamp/600000)%60,(LINMsg[i].Timestamp/10000)%60,(LINMsg[i].Timestamp/10)%1000);
        }
        Sleep(1000);
    }
#endif
#if LIN_MASTER_SCH_TEST
    LIN_EX_MSG LINMsg[6];
    LIN_EX_MSG LINOutMsg[10];
    unsigned int MsgLen = 6;
    LINMsg[0].MsgType = LIN_EX_MSG_TYPE_BK;
    LINMsg[0].Timestamp = 20;//当前帧发送时，下一帧数据发送的时间间隔，单位为毫秒
    for(int f=1;f<MsgLen;f++){
        LINMsg[f].MsgType = LIN_EX_MSG_TYPE_MW;
        LINMsg[f].DataLen = 8;
        for(int i=0;i<LINMsg[1].DataLen;i++){
            LINMsg[f].Data[i] = (f<<4)|i;
        }
        LINMsg[f].Timestamp = 20;//20+f*10;//当前帧发送时，下一帧数据发送的时间间隔，单位为毫秒
        LINMsg[f].CheckType = LIN_EX_CHECK_EXT;
        LINMsg[f].PID = f+1;
    }
    //ID=6，该帧为主机读数据模式，也就是主机发送帧头，从机返回数据
    LINMsg[5].MsgType = LIN_EX_MSG_TYPE_MR;
    LINMsg[5].PID = 6;
    LINMsg[5].Timestamp = 20;
    //启动调度表
    ret = LIN_EX_MasterStartSch(DevHandle[DevIndex],LINMasterIndex,LINMsg,MsgLen);
    if(ret < LIN_EX_SUCCESS){
        printf("Master schedule start failed!\n");
        return 0;
    }else{
        printf("Master schedule start success!\n");
    }
    //循环获取调度表数据
    for(int i=0;i<200;i++){
        Sleep(100);
        ret = LIN_EX_MasterGetSch(DevHandle[DevIndex],LINMasterIndex,LINOutMsg);
        if(ret < LIN_EX_SUCCESS){
            printf("Master get schedule failed!\n");
            return 0;
        }else{
            printf("[0]MsgLen = %d\r\n",ret);
            for(int i=0;i<ret;i++){
                printf("[0]%s SYNC[%02X] PID[%02X] ",MSGTypeStr[LINOutMsg[i].MsgType],LINOutMsg[i].Sync,LINOutMsg[i].PID);
                for(int j=0;j<LINOutMsg[i].DataLen;j++){
                    printf("%02X ",LINOutMsg[i].Data[j]);
                }
                printf("CK = %d ",LINOutMsg[i].CheckType);
                printf("Timestamp = %d",LINOutMsg[i].Timestamp);
                printf("\r\n");
            }
        }
    }
    //停止调度表
    LIN_EX_MasterStopSch(DevHandle[DevIndex],LINMasterIndex);
#endif
    //关闭设备
    USB_CloseDevice(DevHandle[DevIndex]);
	return 0;
}
//LIN中继处理线程
unsigned int WINAPI LIN_RelayThread( void* threadArg )
{
    int DevHandle = *((int *)threadArg);
    int LINMasterIndex = 1;
    int LINSlaveIndex = 0;
    printf("Start lin relay thread!\r\n");
    while(ThreadRunFlag){
#ifdef OS_UNIX
        usleep(10000);
#else
	    Sleep(10);
#endif
        //读取从机接收到的数据
        LIN_EX_MSG LINMsg[1024];//缓冲区尽量大一点，防止益处
        LIN_EX_MSG LINOutMsg[1024];//缓冲区尽量大一点，防止益处
        int ret = LIN_EX_SlaveGetData(DevHandle,LINSlaveIndex,LINMsg);
        for(int i=0;i<ret;i++){
            printf("%s SYNC[%02X] PID[%02X] ",MSGTypeStr[LINMsg[i].MsgType],LINMsg[i].Sync,LINMsg[i].PID);
            for(int j=0;j<LINMsg[i].DataLen;j++){
                printf("%02X ",LINMsg[i].Data[j]);
            }
            printf("[%s][%02X] [%02d:%02d:%02d.%03d]\r\n",CKTypeStr[LINMsg[i].CheckType],LINMsg[i].Check,(LINMsg[i].Timestamp/36000000)%60,(LINMsg[i].Timestamp/600000)%60,(LINMsg[i].Timestamp/10000)%60,(LINMsg[i].Timestamp/10)%1000);
            //转发ID不为0x01帧数据
            if((LINMsg[i].PID&0x3F)!=0x01){
                LINMsg[i].MsgType = LIN_EX_MSG_TYPE_MW;
                //修改接收到的数据
                for(int j=0;j<LINMsg[i].DataLen;j++){
                    LINMsg[i].Data[j]++;
                }
                LINMsg[i].Timestamp = 0;//发送帧之后不延时
                ret = LIN_EX_MasterSync(DevHandle,LINMasterIndex,&LINMsg[i],LINOutMsg,1);
                if(ret != 1){
                    printf("LIN_EX_MasterSync error %d\r\n",ret);
                }
            }
        }
        //主机向从机读取数据
        LINMsg[0].PID = 0x01;
        LINMsg[0].MsgType = LIN_EX_MSG_TYPE_MR;
        LINMsg[0].Timestamp = 0;
        ret = LIN_EX_MasterSync(DevHandle,LINMasterIndex,&LINMsg[0],LINOutMsg,1);
        if(ret != 1){
            printf("LIN_EX_MasterSync error %d\r\n",ret);
        }else{
            //将读到的数据设置到从机响应表里面
            LINOutMsg[0].MsgType = LIN_EX_MSG_TYPE_SW;
            LINOutMsg[0].Timestamp = 0;
            //修改接收到的数据
            for(int j=0;j<LINOutMsg[0].DataLen;j++){
                LINOutMsg[0].Data[j]++;
            }
            ret = LIN_EX_SlaveSetIDMode(DevHandle,LINSlaveIndex,&LINOutMsg[0],1);
            if(ret != LIN_EX_SUCCESS){
                printf("LIN_EX_SlaveSetIDMode error %d\r\n",ret);
            }
        }
	}
    printf("lin relay thread exit!\r\n");
#ifdef OS_UNIX
    pthread_exit(0);
#else
	return 0;
#endif
}

