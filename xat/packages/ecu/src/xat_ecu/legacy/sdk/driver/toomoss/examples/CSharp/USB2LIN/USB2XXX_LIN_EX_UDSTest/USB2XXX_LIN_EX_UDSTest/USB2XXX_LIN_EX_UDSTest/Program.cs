using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Linq;
using System.Diagnostics;
using System.Text;
using USB2XXX;

namespace USB2XXX_LIN_EX_UDSTest
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
            //初始化配置LIN
            ret = USB2LIN_EX.LIN_EX_Init(DevHandle, LINIndex, 19200, 1);//初始化为主机
            if (ret != USB2LIN_EX.LIN_EX_SUCCESS)
            {
                Console.WriteLine("Config LIN failed!");
                return;
            }
            else
            {
                Console.WriteLine("Config LIN Success!");
            }
            //执行一次UDS请求
            LIN_UDS.LIN_UDS_ADDR UDSAddr = new LIN_UDS.LIN_UDS_ADDR();
            UDSAddr.CheckType = 0;
            UDSAddr.NAD = 0x7F;
            UDSAddr.ReqID = 0x3C;
            UDSAddr.ResID = 0x3D;
            UDSAddr.STmin = 5;
            Byte[] udsCmd = new Byte[] { 0x22, 0x68, 0x4E };
            Byte[] resData = new Byte[1024];
            ret = LIN_UDS.LIN_UDS_Request(DevHandle, LINIndex, ref UDSAddr, udsCmd, udsCmd.Length);
            if (ret == LIN_UDS.LIN_UDS_OK)
            {
                Console.Write("Request:");
                for (int j = 0; j < udsCmd.Length; j++)
                {
                    Console.Write("{0:X2} ", udsCmd[j]);
                }
                Console.WriteLine("");
                ret = LIN_UDS.LIN_UDS_Response(DevHandle, LINIndex, ref UDSAddr, resData, 100);
                if ((ret > 0))
                {
                    Console.Write("Response:");
                    for (int j = 0; j < ret; j++)
                    {
                        Console.Write("{0:X2} ", resData[j]);
                    }
                    Console.WriteLine("");
                }
                else
                {
                    Console.WriteLine("LIN_UDS_Request Faild {0}", ret);
                }
            }
            else
            {
                Console.WriteLine("LIN_UDS_Request Error {0}", ret);
            }
            Console.WriteLine("Close Device!");
            //关闭设备
            USB_DEVICE.USB_CloseDevice(DevHandle);
        }
    }
}
