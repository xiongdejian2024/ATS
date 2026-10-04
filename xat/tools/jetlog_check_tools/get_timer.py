#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@Time: 2022/12/12 14:39  
@Author: lei.tao
@File: get_time.py
@Software: PyCharm
@Description: 
@Example: 
"""
import datetime
import time
import subprocess
import paramiko


def timer_func():
    """
    实现TCAM 上电后到网络可用时间记时功能
    """
    
    print("tcam开始上电")
    first_time = datetime.datetime.now()
    
    # while True:
    #     try:
    #         con_tcam(cmd="reboot")
    #     except:
    #         print(f'The server connect failed with error')
    #         time.sleep(1)
    #     finally:
    #         cmd = "ping 172.16.5.31 -c 4"
    #         if os.system(cmd) == 0:
    #             break
    #         else:
    #             time.sleep(0.1)
    # time.sleep(10)
    # while True:
    #     part = pexpect.spawn("adb wait-for-device", timeout=500)
    #     if part.expect(pexpect.EOF) == 0:
    #         print("TCAM上电后再次连接成功")
    #         break
    #     else:
    #         time.sleep(0.1)
    # first = pexpect.spawn("adb shell root")
    # try:
    #     if first.expect('Passwd:'):
    #         first.sendline("oelinux123")
    # except:
    #     print("adb has running as root")
    print("检查tcam网络")
    while True:
  
        conn = subprocess.Popen(f"ping baidu.com -c 4",
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE).communicate()
        print(conn[0].decode())

        if "4 packets transmitted, 4 received, 0% packet loss" in conn[0].decode()\
            or "已发送 4 个包， 已接收 4 个包, 0% 包丢失" in conn[0].decode():
            second_time = datetime.datetime.now()
            timer = second_time - first_time
            break
        else:
            print("网络暂不可用，等待1S")
            time.sleep(1)

    return timer

with open('./Network_time.txt', 'w', encoding="utf-8") as f:
    f.write(f"TCAM上电后到网络可用时间记时:\n{str(timer_func())}")

print(f"TCAM上电后到网络可用时间记时{timer_func()}")
