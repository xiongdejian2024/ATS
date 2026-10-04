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
namespace USB2XXX_LIN_EX_MLXProgTest
{
    class Program
    {
        static void Main(string[] args)
        {
            USB_DEVICE.DEVICE_INFO DevInfo = new USB_DEVICE.DEVICE_INFO();
            Int32[] DevHandles = new Int32[20];
            Byte LINIndex = 0;
            int DevIndex = 0;
            bool state;
            Int32 DevNum, ret = 0;
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
            //打开设备
            state = USB_DEVICE.USB_OpenDevice(DevHandles[DevIndex]);
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
            state = USB_DEVICE.DEV_GetDeviceInfo(DevHandles[DevIndex], ref DevInfo, FuncStr);
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
            byte[] loaderFile = System.Text.Encoding.Default.GetBytes("loaderB-81108_9C-lin2x-19200-loader.hex");
            byte[] appFile = System.Text.Encoding.Default.GetBytes("81108_9C_Example_LIN2_1_PWM06_27_30_36_42_48.hex");
            //初始化,使用LIN模式编程,速度较慢
            ret = MLX_PROGRAMER.MLX_ProgInit(DevHandles[DevIndex], LINIndex,40,0);
            if (ret == MLX_PROGRAMER.MLX_SUCCESS)
            {
                Console.WriteLine("Init device success!");
            }
            //开始编程，该过程可能会比较耗时
            Console.WriteLine("Start LIN Mode Program ......");
            ret = MLX_PROGRAMER.MLX_ProgFlash(DevHandles[DevIndex], LINIndex, loaderFile,appFile, (Byte)0x7F);
            if (ret == MLX_PROGRAMER.MLX_SUCCESS)
            {
                Console.WriteLine("LIN Mode Program success!");
            }
            else
            {
                Console.WriteLine("Program faild! ret = {0}",ret);
            }

            //初始化,使用FastLIN模式编程，速度较快
            ret = MLX_PROGRAMER.MLX_ProgInit(DevHandles[DevIndex], LINIndex, 40, 1);
            if (ret == MLX_PROGRAMER.MLX_SUCCESS)
            {
                Console.WriteLine("Init device success!");
            }
            //开始编程，该过程可能会比较耗时
            Console.WriteLine("Start FastLIN Mode Program ......");
            ret = MLX_PROGRAMER.MLX_ProgFlash(DevHandles[DevIndex], LINIndex, loaderFile, appFile, (Byte)0x7F);
            if (ret == MLX_PROGRAMER.MLX_SUCCESS)
            {
                Console.WriteLine("Fast LIN Mode Program success!");
            }
            else
            {
                Console.WriteLine("Program faild! ret = {0}", ret);
            }
        }
    }
}
