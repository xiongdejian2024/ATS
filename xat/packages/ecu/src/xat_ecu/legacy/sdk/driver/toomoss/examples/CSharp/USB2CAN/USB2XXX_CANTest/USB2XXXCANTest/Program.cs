
#define GET_FIRMWARE_INFO
#define CAN_MODE_LOOPBACK
#define CAN_SEND_MSG
#define CAN_GET_STATUS
#define CAN_GET_MSG

using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;  
using System.Linq;
using System.Diagnostics;
using System.Text;
using USB2XXX;

/**
 * 注意：若运行程序提示找不到USB2XXX.dll文件，可以将工程目录下的USB2XXX.dll和libusb-1.0.dll文件拷贝到exe程序输出目录下即可（一般是./bin/Release或者./bin/Debug目录）
 * 运行程序之前，先将CAN1_H接CAN2_H，CAN1_L接CAN2_L
 */
namespace USB2XXXCANTest
{
    class Program
    {
        static void Main(string[] args)
        {
            usb_device.DEVICE_INFO DevInfo = new usb_device.DEVICE_INFO();
            Int32[] DevHandles = new Int32[20];
            Int32 DevHandle = 0;
            Byte WriteCANIndex = 0;
            Byte ReadCANIndex = 0;
            bool state;
            Int32 DevNum, ret;
            //扫描查找设备
            DevNum = usb_device.USB_ScanDevice(DevHandles);
            if (DevNum <= 0)
            {
                Console.WriteLine("No device connected!");
                return;
            }
            else
            {
                Console.WriteLine("Have {0} device connected!", DevNum);
            }
            DevHandle = DevHandles[0];
            //打开设备
            state = usb_device.USB_OpenDevice(DevHandle);
            if (!state)
            {
                Console.WriteLine("Open device error!");
                return;
            }
            else
            {
                Console.WriteLine("Open device success!");
            }
            //获取固件信息
            StringBuilder FuncStr = new StringBuilder(256);
            state = usb_device.DEV_GetDeviceInfo(DevHandle, ref DevInfo, FuncStr);
            if (!state)
            {
                Console.WriteLine("Get device infomation error!");
                return;
            }
            else
            {
                Console.WriteLine("Firmware Info:");
                Console.WriteLine("    Name:" + Encoding.Default.GetString(DevInfo.FirmwareName));
                Console.WriteLine("    Build Date:" + Encoding.Default.GetString(DevInfo.BuildDate));
                Console.WriteLine("    Firmware Version:v{0}.{1}.{2}", (DevInfo.FirmwareVersion >> 24) & 0xFF, (DevInfo.FirmwareVersion >> 16) & 0xFF, DevInfo.FirmwareVersion & 0xFFFF);
                Console.WriteLine("    Hardware Version:v{0}.{1}.{2}", (DevInfo.HardwareVersion >> 24) & 0xFF, (DevInfo.HardwareVersion >> 16) & 0xFF, DevInfo.HardwareVersion & 0xFFFF);
                Console.WriteLine("    Functions:" + DevInfo.Functions.ToString("X8"));
                Console.WriteLine("    Functions String:" + FuncStr);
            }
            //初始化配置CAN
            USB2CAN.CAN_INIT_CONFIG CANConfig = new USB2CAN.CAN_INIT_CONFIG();
            ret = USB2CAN.CAN_GetCANSpeedArg(DevHandle, ref CANConfig,500000);
            if (ret != USB2CAN.CAN_SUCCESS)
            {
                Console.WriteLine("Get CAN Speed failed!");
                return;
            }
            else
            {
                Console.WriteLine("Get CAN Speed Success!");
            }
#if CAN_MODE_LOOPBACK
            CANConfig.CAN_Mode = 1;//环回模式
#else
            CANConfig.CAN_Mode = 0x80;//正常模式并接入终端电阻
#endif
            ret = USB2CAN.CAN_Init(DevHandle, WriteCANIndex, ref CANConfig);
            if(ret != USB2CAN.CAN_SUCCESS){
                Console.WriteLine("Config CAN failed!");
                return;
            }else{
                Console.WriteLine("Config CAN Success!");
            }
            ret = USB2CAN.CAN_Init(DevHandle, ReadCANIndex, ref CANConfig);
            if (ret != USB2CAN.CAN_SUCCESS)
            {
                Console.WriteLine("Config CAN failed!");
                return;
            }
            else
            {
                Console.WriteLine("Config CAN Success!");
            }
            //配置过滤器，接收所有数据
            /*USB2CAN.CAN_FILTER_CONFIG CANFilter = new USB2CAN.CAN_FILTER_CONFIG();
            CANFilter.Enable = 1;
            CANFilter.ExtFrame = 0;
            CANFilter.FilterIndex = 0;
            CANFilter.FilterMode = 0;
            CANFilter.MASK_IDE = 0;
            CANFilter.MASK_RTR = 0;
            CANFilter.MASK_Std_Ext = 0;
            CANFilter.ID_Std_Ext = 0x475;
            ret = USB2CAN.CAN_Filter_Init(DevHandle, ReadCANIndex, ref CANFilter);
            if (ret != USB2CAN.CAN_SUCCESS)
            {
                Console.WriteLine("Config CAN Filter failed!");
                return;
            }
            else
            {
                Console.WriteLine("Config CAN Filter Success!");
            }*/
            //启动CAN接收数据
            ret = USB2CAN.CAN_StartGetMsg(DevHandle, ReadCANIndex);
            if (ret != USB2CAN.CAN_SUCCESS)
            {
                Console.WriteLine("Start CAN failed!");
                return;
            }
            else
            {
                Console.WriteLine("Start CAN Success!");
            }
#if CAN_SEND_MSG//发送CAN帧
            USB2CAN.CAN_MSG[] CanMsg = new USB2CAN.CAN_MSG[5];
            for(int i=0;i<5;i++){
                CanMsg[i] = new USB2CAN.CAN_MSG();
                CanMsg[i].ExternFlag = 0;
                CanMsg[i].RemoteFlag = 0;
                CanMsg[i].ID = (UInt32)i;
                CanMsg[i].DataLen = 8;
                CanMsg[i].Data = new Byte[CanMsg[i].DataLen];
                for(int j=0;j<CanMsg[i].DataLen;j++){
                    CanMsg[i].Data[j] = (Byte)j;
                }
            }

            int SendedNum = USB2CAN.CAN_SendMsg(DevHandle, WriteCANIndex, CanMsg, (UInt32)CanMsg.Length);
            if(SendedNum >= 0){
                Console.WriteLine("Success send frames:{0}",SendedNum);
            }else{
                Console.WriteLine("Send CAN data failed!");
            }
#endif
#if CAN_GET_STATUS
            USB2CAN.CAN_STATUS CANStatus = new USB2CAN.CAN_STATUS();
            ret = USB2CAN.CAN_GetStatus(DevHandle, WriteCANIndex, ref CANStatus);
            if(ret == USB2CAN.CAN_SUCCESS){
                Console.WriteLine("TSR = {0:X8}",CANStatus.TSR);
                Console.WriteLine("ESR = {0:X8}",CANStatus.ESR);
            }else{
                Console.WriteLine("Get CAN status error!\n");
            }
#endif
            //延时
            System.Threading.Thread.Sleep(500);
            
#if CAN_GET_MSG
            for (int t = 0; t < 10; t++)
            {
                USB2CAN.CAN_MSG[] CanMsgBuffer = new USB2CAN.CAN_MSG[1024];
                //申请存储数据缓冲区
                IntPtr pt = Marshal.AllocHGlobal(Marshal.SizeOf(typeof(USB2CAN.CAN_MSG)) * CanMsgBuffer.Length);
                int CanNum = USB2CAN.CAN_GetMsgWithSize(DevHandle, ReadCANIndex, pt, CanMsgBuffer.Length);
                if (CanNum > 0)
                {
                    for (int i = 0; i < CanNum; i++)
                    {
                        //从缓冲区中获取数据
                        CanMsgBuffer[i] = (USB2CAN.CAN_MSG)Marshal.PtrToStructure((IntPtr)((UInt32)pt + i * Marshal.SizeOf(typeof(USB2CAN.CAN_MSG))), typeof(USB2CAN.CAN_MSG));
                        Console.WriteLine("CanMsg[{0}].ID = {1}", i, CanMsgBuffer[i].ID);
                        Console.WriteLine("CanMsg[{0}].TimeStamp = {1}", i, CanMsgBuffer[i].TimeStamp);
                        Console.Write("CanMsg[{0}].Data = ", i);
                        for (int j = 0; j < CanMsgBuffer[i].DataLen; j++)
                        {
                            Console.Write("{0:X2} ", CanMsgBuffer[i].Data[j]);
                        }
                        Console.WriteLine("\n");
                    }
                }
                else if (CanNum < 0)
                {
                    Console.WriteLine("Get CAN data error!");
                }
                //延时
                System.Threading.Thread.Sleep(100);
                //释放申请的数据缓冲区
                Marshal.FreeHGlobal(pt);
            }
            //停止CAN
            USB2CAN.CAN_StopGetMsg(DevHandle, ReadCANIndex);
#endif
        }
    }
}
