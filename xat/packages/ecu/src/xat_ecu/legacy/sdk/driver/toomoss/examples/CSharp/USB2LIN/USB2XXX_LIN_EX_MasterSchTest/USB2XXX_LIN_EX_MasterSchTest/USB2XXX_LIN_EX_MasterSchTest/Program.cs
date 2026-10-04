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
namespace USB2XXX_LIN_EX_MasterSchTest
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
            Int32 DevNum, ret=0;
            String[] MSGTypeStr = new String[10]{"UN","MW","MR","SW","SR","BK","SY","ID","DT","CK"};
            String[] CKTypeStr = new String[5]{"STD","EXT","USER","NONE","ERROR"};
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
            //从设备数组里面获取当前设备的设备号
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
            /************************************主机写数据************************************/
            int MsgIndex = 0;
            USB2LIN_EX.LIN_EX_MSG[] LINMsg = new USB2LIN_EX.LIN_EX_MSG[5];
            USB2LIN_EX.LIN_EX_MSG[] LINOutMsg = new USB2LIN_EX.LIN_EX_MSG[100];
            //添加第一帧数据，只发送BREAK信号，一般用于唤醒休眠中的从设备
            LINMsg[MsgIndex] = new USB2LIN_EX.LIN_EX_MSG();
            LINMsg[MsgIndex].MsgType = USB2LIN_EX.LIN_EX_MSG_TYPE_BK;//BREAK信号
            LINMsg[MsgIndex].Timestamp = 10;//发送该帧数据之后的延时时间，最小建议设置为1
            MsgIndex++;
            //添加第二帧数据
            LINMsg[MsgIndex] = new USB2LIN_EX.LIN_EX_MSG();
            LINMsg[MsgIndex].MsgType = USB2LIN_EX.LIN_EX_MSG_TYPE_MW;//主机发送数据
            LINMsg[MsgIndex].DataLen = 8;//实际要发送的数据字节数
            LINMsg[MsgIndex].Timestamp = 10;//发送该帧数据之后的延时时间
            LINMsg[MsgIndex].CheckType = USB2LIN_EX.LIN_EX_CHECK_EXT;//增强校验
            LINMsg[MsgIndex].PID = 0x01;//可以只传入ID，校验位底层会自动计算
            LINMsg[MsgIndex].Data = new Byte[8] { 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08 };//必须分配8字节空间，根据自己实际情况修改数据
            MsgIndex++;
            //添加第三帧数据
            LINMsg[MsgIndex] = new USB2LIN_EX.LIN_EX_MSG();
            LINMsg[MsgIndex].MsgType = USB2LIN_EX.LIN_EX_MSG_TYPE_MW;//主机发送数据
            LINMsg[MsgIndex].DataLen = 8;//实际要发送的数据字节数
            LINMsg[MsgIndex].Timestamp = 10;//发送该帧数据之后的延时时间
            LINMsg[MsgIndex].CheckType = USB2LIN_EX.LIN_EX_CHECK_EXT;//增强校验
            LINMsg[MsgIndex].PID = 0x02;//可以只传入ID，校验位底层会自动计算
            LINMsg[MsgIndex].Data = new Byte[8] { 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08 };//必须分配8字节空间，根据自己实际情况修改数据
            MsgIndex++;
            /********************需要发送更多帧数据，请按照前面的方式继续添加********************/
            //发送调度表数据
            ret = USB2LIN_EX.LIN_EX_MasterStartSch(DevHandle, LINIndex, LINMsg, MsgIndex);
            if (ret < USB2LIN_EX.LIN_EX_SUCCESS)
            {
                Console.WriteLine("Master Start Sch failed!");
                return;
            }
            else
            {
                Console.WriteLine("Master Start Sch success!");
            }
            //读取调度表发送出去的数据
            //分配存储返回LIN数据空间，尽量分配大一点，防止缓冲区溢出出错
            IntPtr pt = Marshal.AllocHGlobal(Marshal.SizeOf(typeof(USB2LIN_EX.LIN_EX_MSG)) * LINOutMsg.Length);
            for (int t = 0; t < 20; t++)
            {
                ret = USB2LIN_EX.LIN_EX_SlaveGetData(DevHandle, LINIndex, pt);
                if (ret < USB2LIN_EX.LIN_EX_SUCCESS)
                {
                    Console.WriteLine("Get LIN Data failed!");
                    //释放内存
                    Marshal.FreeHGlobal(pt);
                    return;
                }
                else
                {
                    //显示主机调度表模式发送出去的数据
                    Console.WriteLine("MsgLen = {0}", ret);
                    for (int i = 0; i < ret; i++)
                    {
                        LINOutMsg[i] = (USB2LIN_EX.LIN_EX_MSG)Marshal.PtrToStructure((IntPtr)((UInt32)pt + i * Marshal.SizeOf(typeof(USB2LIN_EX.LIN_EX_MSG))), typeof(USB2LIN_EX.LIN_EX_MSG));
                        Console.Write("{0} SYNC[{1:X2}] PID[{2:X2}] ", MSGTypeStr[LINOutMsg[i].MsgType], LINOutMsg[i].Sync, LINOutMsg[i].PID);
                        for (int j = 0; j < LINOutMsg[i].DataLen; j++)
                        {
                            Console.Write("{0:X2} ", LINOutMsg[i].Data[j]);
                        }
                        Console.WriteLine("[{0}][{1:X2}] [{2}:{3}:{4}.{5}]", CKTypeStr[LINOutMsg[i].CheckType], LINOutMsg[i].Check, (LINOutMsg[i].Timestamp / 36000000) % 60, (LINOutMsg[i].Timestamp / 600000) % 60, (LINOutMsg[i].Timestamp / 10000) % 60, (LINOutMsg[i].Timestamp / 10) % 1000);
                    }
                }
                System.Threading.Thread.Sleep(100);
            }
            //停止调度表发送数据
            USB2LIN_EX.LIN_EX_MasterStopSch(DevHandle, LINIndex);
            //释放内存
            Marshal.FreeHGlobal(pt);
            USB_DEVICE.USB_CloseDevice(DevHandle);
        }
    }
}
