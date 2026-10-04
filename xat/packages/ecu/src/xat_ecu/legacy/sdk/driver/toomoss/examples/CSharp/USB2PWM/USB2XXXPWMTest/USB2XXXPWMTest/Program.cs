using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using USB2XXX;
/**
 * 注意：若运行程序提示找不到USB2XXX.dll文件，可以将工程目录下的所有dll文件拷贝到exe程序输出目录下即可（一般是./bin/Release或者./bin/Debug目录）
 */
namespace USB2XXXPWMTest
{
    class Program
    {
        static void Main(string[] args)
        {
            usb_device.DEVICE_INFO DevInfo = new usb_device.DEVICE_INFO();
            USB2PWM.PWM_CONFIG PWMConfig = new USB2PWM.PWM_CONFIG();
            Int32[] DevHandles = new Int32[20];
            Int32 DevHandle = 0;
            bool state;
            Int32 DevNum, ret;
            Byte[] WriteBuffer = new Byte[64];
            Byte[] ReadBuffer = new Byte[20480];
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
                Console.WriteLine("    Serial Number:" + DevInfo.SerialNumber[0].ToString("X8") + DevInfo.SerialNumber[1].ToString("X8") + DevInfo.SerialNumber[2].ToString("X8"));
            }
            //UTA0101 UTA0201 UTA0301 UTA0302引脚定义参考引脚定义说明文档，主频为200M
            //UTA0403 UTA0402 UTA0401  LIN1对应的PWM通道为0x40,LIN2对应的PWM通道为0x80，主频84M
            //UTA0503  LIN1对应的PWM通道为0x02,LIN2对应的PWM通道为0x04，主频220M
            //UTA0504  LIN1->0x01 LIN2->0x02 LIN3->0x04 LIN4->0x08 DO0->0x10 DO1->0x20,主频240M
            PWMConfig.ChannelMask = 0x01;//初始化PWM
            PWMConfig.Polarity = new byte[8];
            for(int i=0;i<8;i++){
                PWMConfig.Polarity[i] = 1;//将所有PWM通道都设置为正极性
            }
            PWMConfig.Precision = new ushort[8];
            for(int i=0;i<8;i++){
                PWMConfig.Precision[i] = 1000;//将所有通道的占空比调节精度都设置为1/1000
            }
            PWMConfig.Prescaler = new ushort[8];
            for(int i=0;i<8;i++){
                PWMConfig.Prescaler[i] = 10;//将所有通道的预分频器都设置为10，PWM输出频率=PWM主频/(PWMConfig.Precision*PWMConfig.Prescaler)
            }
            PWMConfig.Pulse = new ushort[8];
            for(int i=0;i<8;i++){
                PWMConfig.Pulse[i] = (UInt16)(PWMConfig.Precision[i]*30/100);//将所有通道的占空比都设置为30%
            }
            //初始化PWM
            ret = USB2PWM.PWM_Init(DevHandle,ref PWMConfig);
            if(ret != USB2PWM.PWM_SUCCESS){
                Console.WriteLine("Initialize pwm faild!\n");
                Console.ReadLine();
                return;
            }else{
                Console.WriteLine("Initialize pwm sunccess!\n");
            }
            //启动PWM,RunTimeOfUs之后自动停止，利用该特性可以控制输出脉冲个数，脉冲个数=RunTimeOfUs*200/(PWMConfig.Precision*PWMConfig.Prescaler)
            //若需要一直输出PWM波形，则可以把RunTimeOfUs设置为0
            Int32 RunTimeOfUs = 10000;
            ret = USB2PWM.PWM_Start(DevHandle,PWMConfig.ChannelMask,RunTimeOfUs);
            if(ret != USB2PWM.PWM_SUCCESS){
                Console.WriteLine("Start pwm faild!\n");
                Console.ReadLine();
                return;
            }else{
                Console.WriteLine("Start pwm sunccess!\n");
            }
            Thread.Sleep(1000);
            //改变占空比
            for (int i = 0; i < 8; i++)
            {
                PWMConfig.Pulse[i] = (UInt16)(PWMConfig.Precision[i] * 50 / 100);//将所有通道的占空比都设置为50%
            }
            ret = USB2PWM.PWM_SetPulse(DevHandle, PWMConfig.ChannelMask, PWMConfig.Pulse);
            if(ret != USB2PWM.PWM_SUCCESS){
                Console.WriteLine("Set PWM Pulse Faild!\n");
                Console.ReadLine();
                return;
            }else{
                Console.WriteLine("Set PWM Pulse Sunccess!\n");
            }
            //按下回车后结束发送接收线程
            Console.ReadLine();
            //停止PWM
            ret = USB2PWM.PWM_Stop(DevHandle,PWMConfig.ChannelMask);
            if (ret != USB2PWM.PWM_SUCCESS)
            {
                Console.WriteLine("Stop pwm faild!\n");
                Console.ReadLine();
                return;
            }else{
                Console.WriteLine("Stop pwm sunccess!\n");
            }
            
            //关闭设备
            usb_device.USB_CloseDevice(DevHandle);
        }
    }
}
