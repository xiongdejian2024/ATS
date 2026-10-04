using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Linq;
using System.Diagnostics;
using System.Text;
using USB2XXX;

namespace USB2XXX_LIN_UserDefine
{
    class Program
    {
        static void Main(string[] args)
        {
            USB_DEVICE.DEVICE_INFO DevInfo = new USB_DEVICE.DEVICE_INFO();
            Int32[] DevHandles = new Int32[20];
            Int32 DevHandle = 0;
            Byte LINIndex = 0;
            bool state;
            Int32 DevNum, ret = 0;
            String[] MSGTypeStr = new String[10] { "UN", "MW", "MR", "SW", "SR", "BK", "SY", "ID", "DT", "CK" };
            String[] CKTypeStr = new String[5] { "STD", "EXT", "USER", "NONE", "ERROR" };
            //扫描查找设备
            DevNum = USB_DEVICE.USB_ScanDevice(DevHandles);
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
            state = USB_DEVICE.USB_OpenDevice(DevHandle);
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
            state = USB_DEVICE.DEV_GetDeviceInfo(DevHandle, ref DevInfo, FuncStr);
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
            //初始化自定义LIN
            ret = USB2BMM_LIN.BMM_LIN_Init(DevHandle, LINIndex,19200);
            ret = USB2BMM_LIN.BMM_LIN_SetPara(DevHandle, LINIndex,16,500,500);
            byte[] SendData = new byte[]{0x55,0xC1,0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x60};
            ret = USB2BMM_LIN.BMM_LIN_WriteData(DevHandle, LINIndex, SendData, SendData.Length);
            USB_DEVICE.USB_CloseDevice(DevHandle);
        }
    }
}
