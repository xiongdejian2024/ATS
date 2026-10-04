using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Linq;
using System.Diagnostics;
using System.Text;
using USB2XXX;
/**
 * 注意：若运行程序提示找不到USB2XXX.dll文件，可以将工程目录下的USB2XXX.dll和libusb-1.0.dll文件拷贝到exe程序输出目录下即可（一般是./bin/Release或者./bin/Debug目录）
 */
namespace USB2XXX_CAN_SchTest
{
    class Program
    {
        static void Main(string[] args)
        {
            usb_device.DEVICE_INFO DevInfo = new usb_device.DEVICE_INFO();
            Int32[] DevHandles = new Int32[20];
            Int32 DevHandle = 0;
            Byte CANIndex = 1;
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
            CANConfig.CAN_Mode = 0x80;//正常模式
            CANConfig.CAN_ABOM = 0;//禁止自动离线
            CANConfig.CAN_NART = 1;//禁止报文重传
            CANConfig.CAN_RFLM = 0;//FIFO满之后覆盖旧报文
            CANConfig.CAN_TXFP = 1;//发送请求决定发送顺序
            //配置波特率,波特率 = 500K
            CANConfig.CAN_BRP = 4;
            CANConfig.CAN_BS1 = 15;
            CANConfig.CAN_BS2 = 5;
            CANConfig.CAN_SJW = 2;
            ret = USB2CAN.CAN_Init(DevHandle, CANIndex, ref CANConfig);
            if (ret != USB2CAN.CAN_SUCCESS)
            {
                Console.WriteLine("Config CAN failed!");
                return;
            }
            else
            {
                Console.WriteLine("Config CAN Success!");
            }
            //配置CAN调度表
            int CANSchTabNum = 10;
            USB2CAN.CAN_MSG[] CanMsg = new USB2CAN.CAN_MSG[CANSchTabNum];
            for (int i = 0; i < CANSchTabNum; i++)
            {
                CanMsg[i] = new USB2CAN.CAN_MSG();
                CanMsg[i].ExternFlag = 0;
                CanMsg[i].RemoteFlag = 0;
                CanMsg[i].ID = (UInt32)i;
                CanMsg[i].DataLen = 8;
                CanMsg[i].Data = new Byte[CanMsg[i].DataLen];
                for (int j = 0; j < CanMsg[i].DataLen; j++)
                {
                    CanMsg[i].Data[j] = (Byte)j;
                }
            }
            //总共3个调度表，第一个表里面包含3帧数据，第二个调度表包含6帧数据，第三个调度表包含11帧数据
            Byte[] MsgTabNum = new Byte[3]{3,6,11};
            //第一个调度表循环发送数据，第二个调度表循环发送数据，第三个调度表只发送3次
            UInt16[] SendTimes = new UInt16[3]{ 0xFFFF, 0xFFFF, 3 };
            ret = USB2CAN.CAN_SetSchedule(DevHandle, CANIndex, CanMsg, MsgTabNum, SendTimes, 3);//配置调度表，该函数耗时可能会比较长，但是只需要执行一次即可
            if (ret == USB2CAN.CAN_SUCCESS)
            {
                Console.WriteLine("Set CAN Schedule Success");
            }else{
                Console.WriteLine("Set CAN Schedule Error ret = {0}", ret);
                return;
            }
            ret = USB2CAN.CAN_StartSchedule(DevHandle, CANIndex, 0, 10,0);//启动第一个调度表,表里面的CAN帧并行发送
            if (ret == USB2CAN.CAN_SUCCESS)
            {
                Console.WriteLine("Start CAN Schedule 1 Success");
            }else{
                Console.WriteLine("Start CAN Schedule 1 Error ret = {0}", ret);
                return;
            }
            Console.ReadLine();
            ret = USB2CAN.CAN_StartSchedule(DevHandle, CANIndex, 1, 10, 1);//启动第二个调度表,表里面的CAN帧顺序发送
            if (ret == USB2CAN.CAN_SUCCESS)
            {
                Console.WriteLine("Start CAN Schedule 2 Success");
            }else{
                Console.WriteLine("Start CAN Schedule 2 Error ret = {0}", ret);
                return;
            }
            Console.ReadLine();
            ret = USB2CAN.CAN_StartSchedule(DevHandle, CANIndex, 2, 10, 0);//启动第三个调度表，表里面的CAN帧并行发送，每帧只发送3次
            if (ret == USB2CAN.CAN_SUCCESS)
            {
                Console.WriteLine("Start CAN Schedule 3 Success");
            }else{
                Console.WriteLine("Start CAN Schedule 3 Error ret = {0}", ret);
                return;
            }
            Console.ReadLine();
            ret = USB2CAN.CAN_StopSchedule(DevHandle, CANIndex);//停止调度表
            if (ret == USB2CAN.CAN_SUCCESS)
            {
                Console.WriteLine("Stop CAN Schedule Success");
            }else{
                Console.WriteLine("Stop CAN Schedule Error ret = {0}", ret);
                return;
            }

        }
    }
}
