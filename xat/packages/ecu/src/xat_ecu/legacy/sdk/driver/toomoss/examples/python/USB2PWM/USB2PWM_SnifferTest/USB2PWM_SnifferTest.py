"""
文件说明：USB2XXX PWM相关函数测试程序
更多帮助：www.usbxyz.com
"""
from ctypes import *
import platform
from time import sleep
from usb_device import *
from usb2pwm import *

if __name__ == '__main__': 
    DevIndex = 0
    DevHandles = (c_int * 20)()
    # Scan device
    ret = USB_ScanDevice(byref(DevHandles))
    if(ret == 0):
        print("No device connected!")
        exit()
    else:
        print("Have %d device connected!"%ret)
    # Open device
    ret = USB_OpenDevice(DevHandles[DevIndex])
    if(bool(ret)):
        print("Open device success!")
    else:
        print("Open device faild!")
        exit()
    # Get device infomation
    USB2XXXInfo = DEVICE_INFO()
    USB2XXXFunctionString = (c_char * 256)()
    ret = DEV_GetDeviceInfo(DevHandles[DevIndex],byref(USB2XXXInfo),byref(USB2XXXFunctionString))
    if(bool(ret)):
        print("USB2XXX device infomation:")
        print("--Firmware Name: %s"%bytes(USB2XXXInfo.FirmwareName).decode('ascii'))
        print("--Firmware Version: v%d.%d.%d"%((USB2XXXInfo.FirmwareVersion>>24)&0xFF,(USB2XXXInfo.FirmwareVersion>>16)&0xFF,USB2XXXInfo.FirmwareVersion&0xFFFF))
        print("--Hardware Version: v%d.%d.%d"%((USB2XXXInfo.HardwareVersion>>24)&0xFF,(USB2XXXInfo.HardwareVersion>>16)&0xFF,USB2XXXInfo.HardwareVersion&0xFFFF))
        print("--Build Date: %s"%bytes(USB2XXXInfo.BuildDate).decode('ascii'))
        print("--Serial Number: ",end='')
        for i in range(0, len(USB2XXXInfo.SerialNumber)):
            print("%08X"%USB2XXXInfo.SerialNumber[i],end='')
        print("")
        print("--Function String: %s"%bytes(USB2XXXFunctionString.value).decode('ascii'))
    else:
        print("Get device infomation faild!")
        exit()
    # Initialize adc
    PWMConfig = PWM_CONFIG()
    PWMConfig.ChannelMask = 0x40 #CH6
    for i in range(0,8):
        PWMConfig.Polarity[i] = 0 # 将所有PWM通道都设置为正极性
        PWMConfig.Precision[i] = 1000 # 将所有通道的占空比调节精度都设置为1%
        PWMConfig.Prescaler[i] = 84 # 将所有通道的预分频器都设置为10，则PWM输出频率为84MHz/(PWMConfig.Precision*PWMConfig.Prescaler)
        PWMConfig.Pulse[i] = PWMConfig.Precision[i]*25//100 # 将所有通道的占空比都设置为25%
        PWMConfig.Phase[i] = 0
    # 初始化PWM
    ret = PWM_Init(DevHandles[DevIndex],byref(PWMConfig));
    if ret != PWM_SUCCESS:
        print("Initialize pwm faild!")
        exit()
    else:
        print("Initialize pwm sunccess!")
    # 启动PWM,RunTimeOfUs之后自动停止，利用该特性可以控制输出脉冲个数，脉冲个数=RunTimeOfUs*200/(PWMConfig.Precision*PWMConfig.Prescaler)
    RunTimeOfUs = 0 #一直输出
    ret = PWM_Start(DevHandles[DevIndex],PWMConfig.ChannelMask,RunTimeOfUs)
    if(ret != PWM_SUCCESS):
        print("Start pwm faild!")
        exit()
    else:
        print("Start pwm sunccess!")
    # 初始化PWM监控
    TimePrecUs = 10 #PWM监控时间精度，单位为微秒
    ret = PWM_CAP_Init(DevHandles[DevIndex],1,TimePrecUs)
    if(ret != PWM_SUCCESS):
        print("Start pwm sniffer faild!")
        exit()
    else:
        print("Start pwm sniffer sunccess!")
    # 循环获取数据
    for t in range(0,10):
        PWMData = PWM_CAP_DATA()
        ret = PWM_CAP_GetData(DevHandles[DevIndex],1,byref(PWMData))
        if (ret != PWM_SUCCESS):
            print("pwm cap data faild!")
        else:
            print("cap data sunccess!")
            print(f"HighValue={PWMData.HighValue}")
            print(f"LowValue={PWMData.LowValue}")
            if (((PWMData.HighValue + PWMData.LowValue) > 0)and (PWMData.HighValue < 0xFFFF)and (PWMData.LowValue < 0xFFFF)):
                pwm_cap_freq = 1000000 / ((PWMData.HighValue + PWMData.LowValue)*TimePrecUs)
                pwm_cap_duty = (100 * PWMData.HighValue) / (PWMData.HighValue + PWMData.LowValue)
                print(f"cap freq:{pwm_cap_freq} cap duty:{pwm_cap_duty}")
            else:
                print("未检测到PWM信号")
        sleep(0.01)
    #停止监控
    PWM_CAP_Stop(DevHandles[DevIndex],1)
    exit()

