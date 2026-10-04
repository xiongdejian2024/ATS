using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using USB2XXX;
using System.Threading;
/**
 * 注意：若运行程序提示找不到USB2XXX.dll文件，可以将工程目录下的所有dll文件拷贝到exe程序输出目录下即可（一般是./bin/Release或者./bin/Debug目录）
 */
namespace USB2XXX_PWM_SnifferTest
{
    class Program
    {
        public static byte TimePrecUs = 10;
        public static bool RunFlag = true;
        public static void GetPWMDataThread(int DevHandle, byte Channel)
        {
            while (RunFlag)
            {
                USB2PWM.PWM_CAP_DATA PWMCapData = new USB2PWM.PWM_CAP_DATA();
                int ret = USB2PWM.PWM_CAP_GetData(DevHandle, Channel, ref PWMCapData);
                if (ret == USB2PWM.PWM_SUCCESS)
                {
                    if (((PWMCapData.HighValue + PWMCapData.LowValue) > 0)&&(PWMCapData.HighValue<0xFFFF)&&(PWMCapData.LowValue<0xFFFF))
                    {
                        Console.WriteLine("频率 = {0}Hz", 1000000 / ((PWMCapData.HighValue + PWMCapData.LowValue)*TimePrecUs));
                        Console.WriteLine("占空比 = {0}%", (100 * PWMCapData.HighValue) / (PWMCapData.HighValue + PWMCapData.LowValue));
                    }
                    else
                    {
                        Console.WriteLine("未检测到PWM信号");
                    }
                }
                else
                {
                    Console.WriteLine("PWM get data error!exit thread!");
                    break;
                }
                Thread.Sleep(1000);
            }
            USB2PWM.PWM_CAP_Stop(DevHandle, Channel);
        }
        //主函数
        static void Main(string[] args)
        {
            USB_DEVICE.DEVICE_INFO DevInfo = new USB_DEVICE.DEVICE_INFO();
            Int32[] DevHandles = new Int32[20];
            Int32 DevIndex = 0;
            Byte ChannelIndex=0;//0-对应LIN1，1-对应LIN2
            bool state;
            Int32 DevNum, ret;
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
                Console.WriteLine("    Serial Number:" + DevInfo.SerialNumber[0].ToString("X8") + DevInfo.SerialNumber[1].ToString("X8") + DevInfo.SerialNumber[2].ToString("X8"));
            }
            //初始化PWM监控器
            ret = USB2PWM.PWM_CAP_Init(DevHandles[DevIndex], ChannelIndex, TimePrecUs);
            if (ret != USB2PWM.PWM_SUCCESS)
            {
                Console.WriteLine("Init pwm sniffer error!");
                return;
            }
            else
            {
                Console.WriteLine("Init pwm sniffer success!");
            }
            //创建一个获取PWM数据线程
            Thread pGetPWMDataThread = new Thread(() => GetPWMDataThread(DevHandles[DevIndex], ChannelIndex));
            RunFlag = true;
            pGetPWMDataThread.Start();
            //按下回车后结束发送接收线程
            Console.ReadLine();
            RunFlag = false;
            pGetPWMDataThread.Join();
            Console.WriteLine("Test End!");
        }
    }
}
