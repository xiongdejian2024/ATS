using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using USB2XXX;

namespace USB2XXX_CNT_Test
{
    class Program
    {
        static void Main(string[] args)
        {
            USB_DEVICE.DEVICE_INFO DevInfo = new USB_DEVICE.DEVICE_INFO();
            Int32[] DevHandles = new Int32[20];
            Int32 DevHandle = 0;
            bool state;
            Int32 DevNum, ret;
            Byte[] WriteBuffer = new Byte[64];
            Byte[] ReadBuffer = new Byte[20480];
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
                Console.WriteLine("    Serial Number:" + DevInfo.SerialNumber[0].ToString("X8") + DevInfo.SerialNumber[1].ToString("X8") + DevInfo.SerialNumber[2].ToString("X8"));
            }
            //初始化计数器
            USB2CNT.CNT_CONFIG CNTConfig = new USB2CNT.CNT_CONFIG();
            CNTConfig.CounterMode = USB2CNT.COUNTER_MODE_UP;
            CNTConfig.CounterBitWide = USB2CNT.COUNTER_BITS32;
            CNTConfig.CounterPinMode = USB2CNT.COUNTER_PIN_DOWN;
            CNTConfig.CounterPolarity = USB2CNT.COUNTER_POL_RISING;
            ret = USB2CNT.CNT_Init(DevHandle, USB2CNT.COUNTER_CH2 | USB2CNT.COUNTER_CH3, ref CNTConfig);
            if (ret != USB2CNT.CNT_SUCCESS)
            {
                Console.WriteLine("Init Conter Error!");
                return;
            }
            else
            {
                Console.WriteLine("Init Conter Success!");
            }
            //启动脉冲计数器
            ret = USB2CNT.CNT_Start(DevHandle, USB2CNT.COUNTER_CH2 | USB2CNT.COUNTER_CH3);
            if (ret != USB2CNT.CNT_SUCCESS)
            {
                Console.WriteLine("Start Conter Error!");
                return;
            }
            else
            {
                Console.WriteLine("Start Conter Success!");
            }
            //循环获取脉冲计数器值
            for (int i = 0; i < 1000; i++)
            {
                Int32[] ConterVaue = new Int32[4];
                ret = USB2CNT.CNT_GetValue(DevHandle, USB2CNT.COUNTER_CH2 | USB2CNT.COUNTER_CH3, ConterVaue);
                if (ret == USB2CNT.CNT_SUCCESS)
                {
                    Console.WriteLine("CH2.Value = {0} CH3.Value = {1}", ConterVaue[2], ConterVaue[3]);
                }
                Thread.Sleep(100);
            }
            //停止计数
            ret = USB2CNT.CNT_Stop(DevHandle, USB2CNT.COUNTER_CH2 | USB2CNT.COUNTER_CH3);      
            //关闭设备
            USB_DEVICE.USB_CloseDevice(DevHandle);
        }
    }
}
