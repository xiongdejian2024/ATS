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
            USB2CANFD.CANFD_INIT_CONFIG CANFDConfig = new USB2CANFD.CANFD_INIT_CONFIG();
            CANFDConfig.Mode = 0;        //0-正常模式，1-自发自收模式
            CANFDConfig.RetrySend = 1;   //使能自动重传
            CANFDConfig.ISOCRCEnable = 1;//使能ISOCRC
            CANFDConfig.ResEnable = 1;   //使能内部终端电阻（若总线上没有终端电阻，则必须使能终端电阻才能正常传输数据）
            //波特率参数可以用TCANLINPro软件里面的波特率计算工具计算
            //仲裁段波特率参数,波特率=40M/NBT_BRP*(1+NBT_SEG1+NBT_SEG2)
            CANFDConfig.NBT_BRP = 1;
            CANFDConfig.NBT_SEG1 = 59;
            CANFDConfig.NBT_SEG2 = 20;
            CANFDConfig.NBT_SJW = 2;
            //数据域波特率参数,波特率=40M/DBT_BRP*(1+DBT_SEG1+DBT_SEG2)
            CANFDConfig.DBT_BRP = 1;
            CANFDConfig.DBT_SEG1 = 14;
            CANFDConfig.DBT_SEG2 = 5;
            CANFDConfig.DBT_SJW = 2;
            ret = USB2CANFD.CANFD_Init(DevHandle, 0, ref CANFDConfig);
            if (ret != USB2CANFD.CANFD_SUCCESS)
            {
                Console.WriteLine("Config CANFD failed!");
                return;
            }
            else
            {
                Console.WriteLine("Config CANFD Success!");
            }
            ret = USB2CANFD.CANFD_Init(DevHandle, 1, ref CANFDConfig);
            if (ret != USB2CANFD.CANFD_SUCCESS)
            {
                Console.WriteLine("Config CANFD failed!");
                return;
            }
            else
            {
                Console.WriteLine("Config CANFD Success!");
            }
            //准备CAN调度表数据
            const int AllMsgNum = 5;
            USB2CANFD.CANFD_MSG[] CanMsg = new USB2CANFD.CANFD_MSG[AllMsgNum];
            for (int i = 0; i < AllMsgNum; i++){
                CanMsg[i].Data = new Byte[64];
                CanMsg[i].Flags = 0;//bit[0]-BRS,bit[1]-ESI,bit[2]-FDF,bit[6..5]-Channel,bit[7]-RXD
                CanMsg[i].DLC = 8;
                CanMsg[i].ID = 0x121+(UInt32)i;
                for (int j = 0; j < CanMsg[i].DLC; j++){
                    CanMsg[i].Data[j] = (Byte)j;
                }
                CanMsg[i].Data[0] = (Byte)i;
                CanMsg[i].TimeStamp = 100;//每帧间隔100ms
            }
            //USB2CANFD.CANFD_SendMsg(DevHandle, CANIndex, ref CanMsg[0],1);
            //总共1个调度表，表里面包含20帧数据
            byte[] MsgTabNum=new byte[]{AllMsgNum};
            //调度表循环发送数据
            UInt16[] SendTimes = new UInt16[] { 5 };
            ret = USB2CANFD.CANFD_SetSchedule(DevHandle, CANIndex, CanMsg, MsgTabNum, SendTimes, 1);//配置调度表，该函数耗时可能会比较长，但是只需要执行一次即可
            if (ret == USB2CANFD.CANFD_SUCCESS)
            {
                Console.WriteLine("Set CAN Schedule Success");
            }
            else
            {
                Console.WriteLine("Set CAN Schedule Error ret = {0}", ret);
                return;
            }
            ret = USB2CANFD.CANFD_StartSchedule(DevHandle, CANIndex, 0, 10,0);//启动第一个调度表,表里面的CAN帧并行发送
            if (ret == USB2CANFD.CANFD_SUCCESS)
            {
                Console.WriteLine("Start CAN Schedule 1 Success");
            }else{
                Console.WriteLine("Start CAN Schedule 1 Error ret = {0}", ret);
                return;
            }
            Console.ReadLine();
            USB2CANFD.CANFD_StopSchedule(DevHandle, CANIndex);
            usb_device.USB_CloseDevice(DevHandle);
        }
    }
}
