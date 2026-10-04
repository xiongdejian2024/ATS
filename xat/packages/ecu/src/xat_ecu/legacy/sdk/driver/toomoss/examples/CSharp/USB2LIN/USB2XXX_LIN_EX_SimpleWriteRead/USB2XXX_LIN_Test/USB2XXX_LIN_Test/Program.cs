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
namespace USB2XXX_LIN_Test
{
    class Program
    {
        static void Main(string[] args)
        {
            usb_device.DEVICE_INFO DevInfo = new usb_device.DEVICE_INFO();
            Int32[] DevHandles = new Int32[20];
            Int32 DevHandle = 0;
            Byte LINIndex = 0;
            bool state;
            Int32 DevNum, ret=0;
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
            /************************************主机写数据************************************/
            ret = USB2LIN_EX.LIN_EX_MasterBreak(DevHandle, LINIndex);//发送Break信号，常用于唤醒设备
            if (ret != USB2LIN_EX.LIN_EX_SUCCESS)
            {
                Console.WriteLine("Write LIN failed!");
                return;
            }
            else
            {
                Console.WriteLine("Write LIN Success!");
            }
            //主机模式发送数据,ID和数据根据实际情况进行修改
            byte[] DataBuffer=new byte[8]{0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08};
            ret = USB2LIN_EX.LIN_EX_MasterWrite(DevHandle, LINIndex,(byte)0x02,DataBuffer,(byte)DataBuffer.Length,(byte)1);
            if (ret != USB2LIN_EX.LIN_EX_SUCCESS)
            {
                Console.WriteLine("Write LIN failed!");
                return;
            }
            else
            {
                Console.WriteLine("Write LIN Success!");
            }
            //主机模式读数据，ID根据实际情况修改
            ret = USB2LIN_EX.LIN_EX_MasterRead(DevHandle, LINIndex,(byte)0x03,DataBuffer);
            if(ret < 0){
                Console.WriteLine("Read LIN failed!");
            }else if(ret == 0){
                Console.WriteLine("The slave machine is not responding!");
            }else{
                Console.Write("Read Data:");
                for(int j=0;j<ret;j++){
                    Console.Write("{0:X2} ", DataBuffer[j]);
                }
                Console.WriteLine("");
            }
            return;
        }
    }
}
