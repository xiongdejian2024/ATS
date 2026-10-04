using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Linq;
using System.Diagnostics;
using System.Text;
using USB2XXX;

namespace USB2XXX_CAN_UDSTest
{
    class Program
    {
        static void Main(string[] args)
        {
            USB_DEVICE.DEVICE_INFO DevInfo = new USB_DEVICE.DEVICE_INFO();
            Int32[] DevHandles = new Int32[20];
            Int32 DevHandle = 0;
            Byte CANIndex = 0;
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
            //初始化配置CAN
            USB2CAN.CAN_INIT_CONFIG CANConfig = new USB2CAN.CAN_INIT_CONFIG();
            CANConfig.CAN_Mode = 0|0x80;//正常模式,按位或上0x80表示接入内部终端电阻到总线
            CANConfig.CAN_ABOM = 0;//禁止自动离线
            CANConfig.CAN_NART = 0;//禁止报文重传
            CANConfig.CAN_RFLM = 0;//FIFO满之后覆盖旧报文
            CANConfig.CAN_TXFP = 1;//发送请求决定发送顺序
            //配置波特率,请参考函数说明文档里面的波特率表
            CANConfig.CAN_BRP = 2;
            CANConfig.CAN_BS1 = 15;
            CANConfig.CAN_BS2 = 5;
            CANConfig.CAN_SJW = 1;
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
            //获取发动机转速
            byte[] req_data=new byte[2]{0x01,0x0C};
            byte[] res_data=new byte[4096];
            CAN_UDS.CAN_UDS_ADDR UDSAddr=new CAN_UDS.CAN_UDS_ADDR();
            UDSAddr.ExternFlag = 0;//使用标准帧
            UDSAddr.AddrFormats = 0;
            UDSAddr.ReqID = 0x7DF;
            UDSAddr.ResID = 0x7E8;
            ret = CAN_UDS.CAN_UDS_Request(DevHandle, CANIndex, ref UDSAddr, req_data, req_data.Length);
            if (ret != CAN_UDS.CAN_UDS_OK)
            {
                Console.WriteLine("CAN UDS request failed! {0}", ret);
            }else{
                Console.Write("Request:");
                for (int i = 0; i < req_data.Length; i++)
                {
                    Console.Write(" {0:X2}", req_data[i]);
                }
                Console.WriteLine("");
            }
            ret = CAN_UDS.CAN_UDS_Response(DevHandle, CANIndex, ref UDSAddr, res_data, 1000);
            if (ret <= CAN_UDS.CAN_UDS_OK)
            {
                Console.WriteLine("CAN UDS response failed! {0}", ret);
            }else{
                Console.Write("Response:");
                for(int i=0;i<ret;i++){
                    Console.Write(" {0:X2}", res_data[i]);
                }
                Console.WriteLine("");
                if((res_data[0]==(0x40+req_data[0]))&&(req_data[1]==res_data[1])){
                    Console.WriteLine("转速 = {0} Rpm", ((res_data[2] << 8) | res_data[3]) / 4);
                }
            }
            //获取车速
            req_data[1] = 0x0D;
            ret = CAN_UDS.CAN_UDS_Request(DevHandle, CANIndex, ref UDSAddr, req_data, req_data.Length);
            if (ret != CAN_UDS.CAN_UDS_OK)
            {
                Console.WriteLine("CAN UDS request failed! {0}", ret);
            }else{
                Console.Write("Request:");
                for (int i = 0; i < req_data.Length; i++)
                {
                    Console.Write(" {0:X2}", req_data[i]);
                }
                Console.WriteLine("");
            }
            ret = CAN_UDS.CAN_UDS_Response(DevHandle, CANIndex, ref UDSAddr, res_data, 1000);
            if (ret <= CAN_UDS.CAN_UDS_OK)
            {
                Console.WriteLine("CAN UDS response failed! {0}", ret);
            }else{
                Console.Write("Response:");
                for(int i=0;i<ret;i++){
                    Console.Write(" {0:X2}", res_data[i]);
                }
                Console.WriteLine("");
                if((res_data[0]==(0x40+req_data[0]))&&(req_data[1]==res_data[1])){
                    Console.WriteLine("车速 = {0} Km/h\r\n", res_data[2]);
                }
            }
        }
    }
}
