# -*- coding: utf-8 -*-
"""
@File        : relay_board.py
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/04/26 15:25
@Update Time :
@Description : 通过32路继电器模拟do 输出；8路采集信号，以及pwm发生器输出pwm 波 以及采集pwm 频率和占空比

"""
import os.path
import re
import subprocess

import serial.tools.list_ports
import serial
import time
from xat_ecu.legacy.common.logger import logger
import crcmod
from binascii import unhexlify


def get_tty_location_mapping():
    # 3-7.1 ---- ttyUSB0
    logger.info('获取ttyUSB与LOCATION的mapping')
    tty_location_dict = {}
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        logger.info(f"{port}: {desc} [{hwid}]")
        tty = port
        location = re.findall(r'LOCATION=(.*)', hwid)
        if location:
            location = location[0].split('/')[-1]
            tty_location_dict[location] = tty
    return tty_location_dict


def get_kernels_symlink_mapping():
    # /dev/USB_PWM --- 3-7.1
    logger.info('获取KERNELS与SYMLINK+的mapping')
    tty_symlink_dict = {}
    if os.path.exists('/etc/udev/rules.d/99-usb-serial.rules'):
        with open('/etc/udev/rules.d/99-usb-serial.rules') as f:
            for line in f:
                logger.info(line)
                location = re.findall(r"KERNELS==\"(.*?)\"", line)
                usb = re.findall(r"SYMLINK\+=\"(.*?)\"", line)
                if location and usb:
                    location = location[0]
                    usb = f"/dev/{usb[0]}"
                    tty_symlink_dict[usb] = location
    return tty_symlink_dict


def print_mapping():
    res = subprocess.check_output("ls -lrt /dev/USB* | awk '{print $9 $10 $11}'", shell=True)
    output = res.decode()
    logger.info(output)
    return output


def get_mapping_error():
    error_mapping = []
    output = print_mapping()
    for line in output.split('\n'):
        if '->' in line:
            usb, tty = line.split('->')
            if not tty.startswith('ttyUSB'):
                error_mapping.append(usb)
    return error_mapping


def recover_mapping(tty, usb):
    cmd = f"sudo ln -sf {tty} {usb}"
    logger.info(f'执行{cmd}')
    res = os.system(cmd)
    if res != 0:
        logger.error(f"sudo ln -sf {tty} {usb}执行失败")


class Serial(object):

    def __init__(self, comstr, baudrate=19200):
        '''
        继电器初始化
        :param comstr:   com 口
        :param baudrate: 波特率
        '''
        try:
            self.handler = serial.Serial(comstr, baudrate)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/jidutest_io/relay_io/relay_board.py")
            self.handler = None
            logger.error(f"串口打开失败：{str(e)}")
            try:
                self.recover_mapping_error()
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/jidutest_io/relay_io/relay_board.py")
                logger.error(f"串口打开失败：{str(e)}")
            try:
                self.handler = serial.Serial(comstr, baudrate)
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/jidutest_io/relay_io/relay_board.py")
                self.handler = None
                logger.error(f"串口打开失败：{str(e)}")

    def send_data(self, cmd):
        '''
        发送指令
        :param cmd:
        :return:
        '''
        try:
            self.handler.write(cmd)
            self.handler.flushInput()
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/jidutest_io/relay_io/relay_board.py")
            logger.error(str(e))

    def recv_data(self, buffer_size=None):
        '''
        接收数据
        :return:
        '''
        try:
            if buffer_size is None:
                buffer_size = self.get_buffer_size()
            return_data = self.handler.read(buffer_size)  # 读取缓冲数据
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/jidutest_io/relay_io/relay_board.py")
            logger.error(str(e))
            return_data = None
        return return_data

    def get_buffer_size(self):
        '''
        获取缓冲数据（接收数据）长度
        :return:
        '''
        time.sleep(0.1)  # 延时，否则len_return_data将返回0，此处易忽视！！！
        len_return_data = self.handler.inWaiting()  # 获取缓冲数据（接收数据）长度
        return len_return_data

    def close_com(self):
        '''
        关闭继电器通道
        :return:
        '''
        if self.handler:
            self.handler.close()

    def recover_mapping_error(self):
        tty_location_dict: dict = get_tty_location_mapping()
        kernels_symlink_dict: dict = get_kernels_symlink_mapping()
        error_mapping: list = get_mapping_error()
        if error_mapping:
            logger.info(f'找到mapping混乱的ttyUSB')
            for usb in error_mapping:
                location = kernels_symlink_dict[usb]
                tty = tty_location_dict[location]
                recover_mapping(tty, usb)
        else:
            logger.info('usb mapping配置正确')
        print_mapping()


class ModbBusCollect(Serial):

    def __init__(self, comstr, baudrate=9600):
        super().__init__(comstr, baudrate)

    def get_channel_value(self, channel, **kwargs):
        '''
        获取通道状态, 1 表示有效信号，0 表示无效信号

        发送指令 [0x01, 0x02, 00, 0x20, 0x00, 0x08, 0x78, 0x06]
        01 表示地址，02 功能码，0020 离散量起始地址 0008 地址数量  7806 CRC16校验

        接收数据 01 02 01 00 A0 78
        01 地址，02 功能码，01 数据字节长度， 00 表示8路数字输入状态（00000000 表示8路全为无效信号），

        A078 表示CRC16 校验


        :param channel: 通道 ，范围为0到7 包含0和7
        :param kwargs:
        :return:成功的话，返回当前通道的状态，以及一个字典，包含所有通道对应状态
                0 {7: 0, 6: 0, 5: 0, 4: 0, 3: 0, 2: 0, 1: 0, 0: 0}
                失败的话， 返回 None 以及一个空字典

        '''
        # 读取 八个通道的指令
        cmd = [0x01, 0x02, 00, 0x20, 0x00, 0x08, 0x78, 0x06]
        try:
            send_data = bytes(cmd)
            self.send_data(send_data)
            return_data = self.recv_data()
            str_return_data = str(return_data.hex())
            print(f"读取的值为{str_return_data}")
            # 01020110a044
            if str_return_data and len(str_return_data) == 12:
                status = str_return_data[6:8]
                bin_str = bin(int(status, 16))[2:].zfill(8)
                key = list(range(0, 8))
                key.reverse()
                value = [True if int(i) else False for i in list(bin_str)]
                dic = dict(zip(key, value))
                ret = dic.get(channel)
                # 返回当前通道的值，以及一个字典，包含所有通道对应状态
                return ret, dic
            else:
                logger.error("接收的数据不对")
                return None, {}
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/jidutest_io/relay_io/relay_board.py")
            logger.error(str(e))
            return None, {}

    def close(self):
        '''
        关闭通道
        :return:
        '''
        self.close_com()


class RelayModbus(Serial):

    def __init__(self, comstr, baudrate=115200):
        super().__init__(comstr, baudrate)
        '''
          继电器初始化
          :param comstr:   com 口
          :param baudrate: 波特率
        '''

    def send_32_way_relay_cmd(self, channel, linkup=True, **kwargs):
        '''
        发送 32 通道 继电器的指令 channel 取值范围为 1到32
        1-8 连同则为高电平 12v  9-32 连同则接地
        继电器打开指令：aa 01 01 xx yy zz ww 00 00 ab
             ww：1-8路  zz：9-16路 yy：17-24路 xx ：25-32路,
            比如之前第1路和第16路是闭合状态， 需要在不改变1和16路的状态下想让第2路和第15路闭合，就可发送
            aa 01 01 02 40 zz ww 00 00 ab ,02 代表第2路（00000010），40代表的15路（01000000）
        继电器断开的命令：aa 01 02 xx yy 00 00 00 00 ab
            (只选择需要断开的路赋值1即可)。比如想让第1,2,3,4路断开，就赋值xx = 0f，（00001111）即可。其他路的状态不发生改变。

        :param channel: 为整数，或者一个整数列表
        :param linkup: 为True 表示 通道连接，false 表示通道断开
        :param kwargs:
        :return:
        '''
        if linkup:
            # 关闭通道指令头部
            head = [0xaa, 0x01, 0x01]
            # 关闭通道指令尾部
            foot = [0, 0, 0xAB]
            ret_value = 1
        else:
            # 关闭通道指令头部
            head = [0xaa, 0x01, 0x02]
            # 关闭通道指令尾部
            foot = [0, 0, 0xAB]
            ret_value = 0

        if isinstance(channel, int):
            channel_list = [channel]
        elif isinstance(channel, (tuple, list)):
            channel_list = list(channel)
        else:
            assert 0, "通道类型不对"
        try:
            for chan in channel_list:
                if chan < 1 or chan > 32:
                    assert 0, f"当前继电器为32 通道，所传通道为{chan}超出范围"
                lis = ["0"] * 32
                lis[chan - 1] = '1'
                lis.reverse()
                string = ''.join(lis)
                value = [int(string[i:i + 8], 2) for i in range(0, len(string), 8)]
                cmd = head + value + foot
                # 发送指令
                self.send_data(bytes(cmd))
                current_status, all_status = self.get_32_way_relay_status(chan)
                if ret_value != current_status:
                    logger.warning(f"当前{chan}通道状态为:{'连通' if current_status else '悬空'}！！！！")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/jidutest_io/relay_io/relay_board.py")
            logger.warning(str(e))

    def get_32_way_relay_status(self, channel, **kwargs):
        '''
        发送 获取 32 通道状态 继电器的指令 channel 取值范围为 1到32
        1-8 连同则为高电平 12v
        9-32 连同则接地

        :param channel: 为整数
        :param kwargs:
        :return:
        '''
        head = [0xaa, 0x01, 0x1a]
        foot = [0, 0, 0xAB]

        if not isinstance(channel, int):
            assert 0, "通道类型不对"
        try:
            if channel < 1 or channel > 32:
                assert 0, f"当前继电器为32 通道，所传通道为{channel}超出范围"
            lis = ["0"] * 32
            lis[channel - 1] = '1'
            lis.reverse()
            string = ''.join(lis)
            value = [int(string[i:i + 8], 2) for i in range(0, len(string), 8)]
            cmd = head + value + foot
            # 发送指令
            self.send_data(bytes(cmd))
            # 读取下状态
            recv_data = self.recv_data()
            string_hex = recv_data.hex()[6:-6]
            string_bin = bin(int(string_hex, 16))[2:].zfill(32)
            string_lis = list(string_bin)
            string_lis.reverse()
            all_status = ''.join(string_lis)
            logger.info(f"获取的32路继电器1-32通道状态为：{all_status}; 1为连通状态0表示悬空")
            value = int(string_lis[channel - 1])
            logger.info(f"当前{channel}通道状态为:{'连通' if value else '悬空'}")
            channel_status_dic = dict(zip(list(range(1, 33)), [int(i) for i in string_lis]))
            return channel_status_dic.get(channel), channel_status_dic

        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/jidutest_io/relay_io/relay_board.py")
            logger.warning(str(e))
            return None, None

    def relay_linkup(self, channel, **kwargs):
        '''
        连接继电器，通路，channel 取值范围为 1到32
        :param channel: 需要连接的通道；为整数，或者一个整数列表
        :return:
        '''
        self.send_32_way_relay_cmd(channel, linkup=True, **kwargs)

    def relay_linkdown(self, channel, **kwargs):
        '''
        断开继电器，断路  channel 取值范围为 1到32
        :param channel: 需要断开的通道，为整数，或者一个整数列表
        :return:
        '''
        self.send_32_way_relay_cmd(channel, linkup=False, **kwargs)

    def close(self):
        '''
        关闭通道
        :return:
        '''
        self.close_com()


class PwmModbus(Serial):
    def __init__(self, comstr, baudrate=9600):
        super().__init__(comstr, baudrate)
        '''
          继电器初始化
          :param comstr:   com 口
          :param baudrate: 波特率
        '''

    def __send_pwm_data(self, data):
        '''
        发送 pwm 波的数据，返回1 为发送成功，返回0 发送失败
        :param data:
        :return:
        '''
        try:
            self.send_data(data.encode('utf-8'))
            time.sleep(0.5)
            res = self.recv_data()  # b'DOWN\r\n'   b'FALL\r\n'
            if "DOWN" in str(res):
                return 1
            return 0
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/jidutest_io/relay_io/relay_board.py")
            logger.error(str(e))
            return 0

    def set_pwm_freq(self, freq, **kwargs):
        '''
        设置pwm 波的频率
        F101 ：设置频率为 101 HZ   (001~999)
        F1.05 ：设置频率为 1.05 KHZ   (1.00~9.99)
        F10.5 ：设置频率为 10.5 KHZ   (10.0~99.9)
        F1.0.5 ：设置频率为 105 KHZ   (1.0.0~1.5.0)

        0-999
        1000-9990
        10 000 -99 900
        100 000 -150 000

        :param freq:
        :param kwargs:
        :return:
        '''
        if isinstance(freq, int):
            if freq < 0:
                logger.info("频率最小为0")
                freq = 0
            elif freq > 150 * 1000:
                logger.info("频率最大为150KHZ")
                freq = 150 * 1000
            # 除1000
            freq_khz = freq / 1000

            if freq_khz < 1:
                # 对原数据处理
                freq_str = str(freq).zfill(3)
            elif 1 <= freq_khz < 10:
                freq_str = str(freq_khz).ljust(4, "0")
            elif 10 <= freq_khz < 100:
                freq_str = str(freq_khz)
            else:
                # 100 <= freq_khz <= 150:
                freq_str = '.'.join(list(str(int(freq_khz))))
        else:
            assert 0, "频率只能为整数"

        data = "F" + freq_str

        return self.__send_pwm_data(data)

    def set_pwm_duty(self, duty, **kwargs):
        '''
        设置pwm 的占空比

        “DXXX”:设置PWM的占空比为XXX；(001~100)
        例如D050，设置PWM占空比是50%

        :param duty: 最小值0，最大值为100，整数
        :param kwargs:
        :return:
        '''

        if isinstance(duty, int):
            if duty > 100:
                duty = 100
            elif duty < 0:
                duty = 0
            duty = str(duty).zfill(3)
        else:
            assert 0, "占空比只能为整数"

        data = 'D' + duty
        return self.__send_pwm_data(data)

    def set_pwm_freq_and_duty(self, freq, duty, **kwargs):
        '''
        设置 pwm 的占空比和频率
        :param freq:
        :param duty:
        :param kwargs:
        :return:
        '''

        res = self.set_pwm_freq(freq)
        if not res:
            return 0
        time.sleep(1)
        res = self.set_pwm_duty(duty)
        if not res:
            return 0
        logger.info(f"设置pwm 波的 频率为={freq}，占空比={duty}")
        return 1

    def get_pwm_freq_and_duty(self):
        '''
        读取 pwm 波的 频率和占空比
            发送“read”字符串，读取设置的参数。
            设置成功返回：DOWN；
            设置失败返回：FALL。
        :return:
        '''
        data = 'read'
        self.send_data(data.encode('utf-8'))
        time.sleep(0.5)
        res = self.recv_data()  # b'F=10 Hz     D= 90%\r\n'
        if res:
            logger.info(f'获取的pwm 数据为{str(res)}')
            res = res.decode().replace("\r\n", '')
            regular = re.findall(f"F=(.+?)Hz     D=(.+?)%", res)
            if regular:
                try:
                    value = regular[0]
                    if value and len(value) == 2:
                        f_str = value[0].strip()
                        if "K" in f_str:
                            f = int(float(f_str[:-1])) * 1000
                        else:
                            f = int(float(f_str))
                        d = int(float(value[1].strip()))
                        return f, d
                except Exception as e:
                    __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/sdk/driver/jidutest_io/relay_io/relay_board.py")
                    logger.error(str(e))
                    return None, None

        return None, None

    def close(self):
        self.close_com()


def crc16Add(read):
    '''
    pwm 的 crc 校验
    :param read:
    :return:
    '''
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    if isinstance(read, list):
        read = bytes(read).hex()
    data = read.replace(" ", "")
    readcrcout = hex(crc16(unhexlify(data))).upper()
    str_list = list(readcrcout)
    if len(str_list) == 5:
        str_list.insert(2, '0')
    crc_data = "".join(str_list)
    read = data + crc_data[4:] + crc_data[2:4]
    lis = [int(read[i:i + 2], 16) for i in range(0, len(read), 2)]
    # print('增加Modbus_CRC16校验:>>> %s' % read)
    return lis


class ModbPwmBusCollect(Serial):

    def __init__(self, comstr, baudrate=9600, **kwargs):
        super().__init__(comstr, baudrate)
        # 采集通道
        self.pwm_in_pin = kwargs.get('pwm_in_pin', [0, 1, 2, 3])
        # 输出通道
        self.pwm_out_pin = kwargs.get('pwm_out_pin', [4, 5, 6, 7])

    def set_pwm_freq(self, channel, freq, address=0x04, **kwargs):
        '''
        设置 pwm 的 频率
        :param freq:
        :param kwargs:
        :return:
        '''

        if channel not in self.pwm_out_pin:
            assert 0, f" 采集通道不对，本应为{self.pwm_out_pin}，实际为{channel}"
        cmd_list = []
        cmd_list.append(address)
        cmd_list.append(0x06)
        cmd_list.append(0x08)
        if channel == 4:
            channel_cmd = 0x40
        elif channel == 5:
            channel_cmd = 0x42
        elif channel == 6:
            channel_cmd = 0x44
        else:
            channel_cmd = 0x46

        cmd_list.append(channel_cmd)
        freq = int(float("%.1f" % freq) * 10)
        freq_hex = hex(freq)[2:].zfill(4)
        freq_lis = [int(freq_hex[i:i + 2], 16) for i in range(0, len(freq_hex), 2)]
        cmd_list.extend(freq_lis)

        cmd = crc16Add(cmd_list)
        send_data = bytes(cmd)
        self.send_data(send_data)

    def set_pwm_duty(self, channel, duty, address=0x04, **kwargs):
        '''
        设置pwm 的占空比
        :param duty: 小数
        :param kwargs:
        :return:
        '''
        if channel not in self.pwm_out_pin:
            assert 0, f" 采集通道不对，本应为{self.pwm_out_pin}，实际为{channel}"
        cmd_list = []
        cmd_list.append(address)
        cmd_list.append(0x06)
        cmd_list.append(0x08)
        if channel == 4:
            channel_cmd = 0x41
        elif channel == 5:
            channel_cmd = 0x43
        elif channel == 6:
            channel_cmd = 0x45
        else:
            channel_cmd = 0x47
        cmd_list.append(channel_cmd)
        duty = int(duty * 100)
        duty_hex = hex(duty)[2:].zfill(4)
        duty_lis = [int(duty_hex[i:i + 2], 16) for i in range(0, len(duty_hex), 2)]
        cmd_list.extend(duty_lis)
        cmd = crc16Add(cmd_list)
        send_data = bytes(cmd)
        self.send_data(send_data)

    def set_pwm_freq_and_duty(self, channel, freq, duty, address=4, **kwargs):
        '''
        设置 pwm 的占空比和频率
        :param freq:
        :param duty:
        :param kwargs:
        :return:
        '''
        if channel not in self.pwm_out_pin:
            assert 0, f" 采集通道不对，本应为{self.pwm_out_pin}，实际为{channel}"

        self.set_pwm_freq(channel, freq, address)
        time.sleep(0.5)
        self.set_pwm_duty(channel, duty, address)

    def get_pwm_freq_and_duty(self, channel, address=0x04, **kwargs):
        '''
        获取 通道的 频率和占空比
        :param channel:
        :param address:
        :param kwargs:
        :return:
        '''
        # if channel not in self.pwm_in_pin:
        #     assert 0, f" 采集通道不对，本应为{self.pwm_in_pin}，实际为{channel}"
        cmd_list = [address, 0x03]
        if channel in self.pwm_in_pin:
            cmd_list.append(0x00)
            if channel == 0:
                channel_cmd = 0x80
            elif channel == 1:
                channel_cmd = 0x82
            elif channel == 2:
                channel_cmd = 0x84
            else:
                channel_cmd = 0x86
        elif channel in self.pwm_out_pin:
            cmd_list.append(0x08)
            if channel == 4:
                channel_cmd = 0x40
            elif channel == 5:
                channel_cmd = 0x42
            elif channel == 6:
                channel_cmd = 0x44
            else:
                channel_cmd = 0x46
        else:
            assert 0, f" 采集通道不对，本应为{self.pwm_in_pin + self.pwm_out_pin}，实际为{channel}"

        cmd_list.append(channel_cmd)
        cmd_list.append(0x00)
        cmd_list.append(0x02)

        cmd = crc16Add(cmd_list)
        send_data = bytes(cmd)
        self.send_data(send_data)
        return_data = self.recv_data()
        str_return_data = str(return_data.hex())
        print(f"读取的值为{str_return_data}")
        freq = str_return_data[6:10]
        duty = str_return_data[10:14]

        print(f"channel={channel} freq={int(freq, 16) / 10} duty={int(duty, 16) / 100}")
        return int(freq, 16) / 10, int(duty, 16) / 100

    def read_pwm(self, channel, address=0x04, **kwargs):
        '''
        获取
        [0x04, 0x03, 0x08, 0x40, 0x00, 0x02]
        :param channel:
        :param address:
        :param kwargs:
        :return:
        '''
        if channel not in self.pwm_out_pin:
            assert 0, f" 采集通道不对，本应为{self.pwm_out_pin}，实际为{channel}"
        cmd_list = [address, 0x03]
        cmd_list.append(0x08)
        if channel == 4:
            channel_cmd = 0x40
        elif channel == 5:
            channel_cmd = 0x42
        elif channel == 6:
            channel_cmd = 0x44
        else:
            channel_cmd = 0x46

        cmd_list.append(channel_cmd)
        cmd_list.append(0x00)
        cmd_list.append(0x02)

        cmd = crc16Add(cmd_list)
        send_data = bytes(cmd)
        self.send_data(send_data)
        return_data = self.recv_data()
        str_return_data = str(return_data.hex())
        print(f"读取的值为{str_return_data}")
        freq = str_return_data[6:10]
        duty = str_return_data[10:14]
        print('freq', freq, int(freq, 16))
        print('duty', duty, int(duty, 16))

        print(f"channel={channel} freq={int(freq, 16)} duty={int(duty, 16) / 100}")
        return int(freq, 16), int(duty, 16) / 100

    def close(self):
        '''
        关闭通道
        :return:
        '''
        self.close_com()


class RelayIOSystem(object):
    def __init__(self, io_config: dict):
        self.io_signal_dict = io_config.get('signal')
        self.io_task = {}
        self.decv_dict = {}
        self.decv_map_sig = {}
        self.init_device()

    def init_device(self):
        '''
        根据接线初始化设备
        @return:
        '''

        for io_signal, signal_config in self.io_signal_dict.items():
            io_signal = io_signal.lower()
            com_channel = signal_config.get('channel')
            com_line = com_channel.split("line")
            com = com_line[0][:-1]
            line = int(com_line[-1])
            baudrate = signal_config.get('baudrate')
            if signal_config.get('type') == 'DO':
                if com not in self.decv_dict:
                    # 设备初始化
                    if baudrate is None:
                        relay_obj = RelayModbus(com)
                    else:
                        relay_obj = RelayModbus(com, baudrate=baudrate)
                    self.decv_dict[com] = relay_obj
                    # 信号名称和设备 映射,以及和设备的 通道
                    self.decv_map_sig[io_signal] = (com, line)
                else:
                    self.decv_map_sig[io_signal] = (com, line)
            elif signal_config.get('type') == 'DI':
                if com not in self.decv_dict:
                    # 设备初始化
                    if baudrate is None:
                        relay_obj = ModbBusCollect(com)
                    else:
                        relay_obj = ModbBusCollect(com, baudrate=baudrate)
                    self.decv_dict[com] = relay_obj
                    # 信号名称和设备 映射,以及和设备的 通道
                    self.decv_map_sig[io_signal] = (com, line)
                else:
                    self.decv_map_sig[io_signal] = (com, line)
            elif signal_config.get('type') == 'AO':
                pass
            elif signal_config.get('type') == 'AI':
                pass
            elif signal_config.get('type') == 'PWMI':
                if com not in self.decv_dict:
                    # 设备初始化
                    if baudrate is None:
                        pwm_obj = ModbPwmBusCollect(com)
                    else:
                        pwm_obj = ModbPwmBusCollect(com, baudrate=baudrate)
                    self.decv_dict[com] = pwm_obj
                    # 信号名称和设备 映射,以及和设备的 通道
                    self.decv_map_sig[io_signal] = (com, line)
                else:
                    self.decv_map_sig[io_signal] = (com, line)
            elif signal_config.get('type') == 'PWMO':
                if com not in self.decv_dict:
                    # 设备初始化
                    if baudrate is None:
                        pwm_obj = ModbPwmBusCollect(com)
                    else:
                        pwm_obj = ModbPwmBusCollect(com, baudrate=baudrate)
                    self.decv_dict[com] = pwm_obj
                    # 信号名称和设备 映射,以及和设备的 通道
                    self.decv_map_sig[io_signal] = (com, line)
                else:
                    self.decv_map_sig[io_signal] = (com, line)
            else:
                logger.warning("SignalType is not supported.")

    def set_do_level(self, io_signal: str, value):
        '''
        设置输出电平
        @param io_signal:
        @param value:
        @return:
        '''
        io_signal = io_signal.lower()
        # 根据信号获取设备 以及通道
        dev_com, channel = self.decv_map_sig.get(io_signal, (None, None))
        # 获取 设备句柄
        obj = self.decv_dict.get(dev_com)
        if obj is None:
            logger.error(f"未找到{io_signal}对应的设备")
            return 0
        if value:
            obj.relay_linkup(channel)
        else:
            obj.relay_linkdown(channel)

        return 1

    def get_di_level(self, io_signal: str):
        '''
        获取 电平信号
        @param io_signal:
        @return:
        '''
        io_signal = io_signal.lower()
        # 根据信号获取设备 以及通道
        dev_com, channel = self.decv_map_sig.get(io_signal, (None, None))
        # 获取 设备句柄
        obj = self.decv_dict.get(dev_com)
        if obj is None:
            logger.error(f"未找到{io_signal}对应的设备")
            return None
        value, dic = obj.get_channel_value(channel)
        logger.info(f"{io_signal}对应的设备 所有通道的状态为{dic}")
        return value

    def set_pwm(self, io_signal: str, freq: int, duty: int):
        '''
        设置 pwm
        @param io_signal: 信号名称
        @param freq: 频率
        @param duty: 占空比
        @return: 0 表示失败，1表示成功
        '''
        io_signal = io_signal.lower()
        # 根据信号获取设备 以及通道
        dev_com, channel = self.decv_map_sig.get(io_signal, (None, None))
        # 获取 设备句柄
        obj = self.decv_dict.get(dev_com)
        if obj is None:
            logger.error(f"未找到{io_signal}对应的设备")
            return None
        res = obj.set_pwm_freq_and_duty(channel, freq, duty)
        return res

    def get_pwm(self, io_signal: str):
        '''
        获取 pwm ，返回频率和占空比
        @param io_signal:
        @return:
        '''
        io_signal = io_signal.lower()
        # 根据信号获取设备 以及通道
        dev_com, channel = self.decv_map_sig.get(io_signal, (None, None))
        # 获取 设备句柄
        obj = self.decv_dict.get(dev_com)
        if obj is None:
            logger.error(f"未找到{io_signal}对应的设备")
            return None, None
        f, d = obj.get_pwm_freq_and_duty(channel)
        return f, d

    def close(self):
        '''
        关闭 设备
        @return:
        '''
        all_dev = list(self.decv_dict.values())
        for dev in all_dev:
            dev.close()

    # # 32 路继电器使用

# relay_obj = RelayModbus("/dev/ttyUSB0")
# relay_obj = RelayModbus('com3')
# # 连同 通道1
# relay_obj.relay_linkup(1)
# # 断开通道1
# relay_obj.relay_linkup(1)
# # 关闭
# relay_obj.close()


# # MODBUS 采集器使用
# mobd = ModbBusCollect("/dev/ttyUSB1")
# mobd = ModbBusCollect("com4")
# # 获取通道0的 状态
# value, dic = mobd.get_channel_value(0)
# print(value, dic)
# # 返回 0通道对应的状态，以及所有通道对应的状态
# # 0 {7: 0, 6: 0, 5: 0, 4: 0, 3: 0, 2: 0, 1: 0, 0: 0}
# # 关闭通道
# mobd.close()


# # pwm 使用说明
# pwm = PwmModbus('com5', 9600)
# pwm = PwmModbus("/dev/ttyUSB2", 9600)
# # 设置 pwm 频率为250 HZ 占空比为50%
# pwm.set_pwm_freq_and_duty(250, 80)
# # 获取 pwm 波的频率和占空比
# freq, retduty = pwm.get_pwm_freq_and_duty()
# print(f"freq={freq},duty={retduty}")
# # freq=250,duty=80
# pwm.close()
