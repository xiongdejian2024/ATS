#!/usr/bin/env python 3.8
# _*_ coding: utf-8 _*_

"""
@File: adb_client.py
@Time: 2022/07/06 10:03
@Author: lei.tao
@Software: PyCharm
@Description: adb驱动类的封装
@Examples:
"""

import pexpect
from airtest.core.api import *
from airtest.core.android.adb import *
from distutils import spawn

# project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
# sys.path.append(project_root)

from xat_ecu.legacy.common.logger import logger


class Adb(ADB):

    def __init__(self, serialno=None, adb_path=None, server_addr=None, display_id=None, input_event=None):
        if not adb_path:
            adb_path = spawn.find_executable("adb")
            self.adb_path = adb_path

        if not serialno:
            serial_no = self.get_devices_id()
            if len(serial_no) >= 2:
                print("请选择需要操作的设备号：" + str(serial_no))
                exit(1)
            elif len(serial_no) == 1:
                self.serialno = serial_no[0]
            else:
                print("没有设备连接，请检查是否连接正常")
                exit(1)
        else:
            self.serialno = serialno

        super().__init__(serialno=serialno, adb_path=adb_path, server_addr=server_addr, display_id=display_id,
                         input_event=input_event)

    def shell(self, args=None, timeout=None):
        try:

            if len(self.get_devices_id()) == 1:
                cmd = "%s shell %s" % (self.adb_path, str(args))
            else:
                cmd = "%s -s %s shell %s" % (self.adb_path, self.serialno, str(args))
            
            root = pexpect.spawn("adb shell root")
            try:
                if root.expect('Passwd:') == 0:
                    #print("输入root密码")
                    root.sendline('oelinux123')
                    time.sleep(1)
                part = pexpect.spawn("adb wait-for-device")
                while True:
                    if part.expect(pexpect.EOF) == 0:
                        break
                    else:
                        time.sleep(1)
            except: 
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/adb_client.py")
                logger.debug("adb has running as root")

            child = pexpect.spawn(cmd)
            print(cmd)
            #print("再次输入root密码")
            child.sendline('oelinux123')
            if timeout:
                time.sleep(timeout)
                child.sendcontrol('c')
                
            out = child.readlines()[4:]
            data = []
            for i in out:
                data.append(i.decode())

            logger.debug('执行命令为：' + str(cmd))
            # out = os.popen(cmd).read()
        except AdbError as err:
            raise AdbShellError(err.stdout, err.stderr)
        else:
            return ''.join(data)

    def get_devices_id(self):
        device_list = []
        cmd = "%s devices" % self.adb_path
        out = os.popen(cmd).readlines()
        for i in out:
            if 'devices' not in i and len(i) > 5:
                device_list.append(i.split("\t")[0])
        return device_list

    def install(self, filepath, replace=False, install_options=None):
        """
        Args:
            filepath: full path to file to be installed on the device
            replace: force to replace existing application, default is False
            install_options:
                e.g.["-t",  # allow test packages
                    "-l",  # forward lock application,
                    "-s",  # install application on sdcard,
                    "-d",  # allow version code downgrade (debuggable packages only)
                    "-g",  # grant all runtime permissions
                ]
        Returns:
            command output

        """
        try:
            res = super().install_app(filepath, replace=replace, install_options=install_options)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/adb_client.py")
            logger.error(e)
            return ""
        else:
            return res

    def uninstall(self, package):
        """
        package: package name to be uninstalled from the device
        Returns: command output
        """
        try:
            res = super().uninstall_app(package)
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/driver/adb_client.py")
            logger.error(e)
            return ""
        else:
            return res

    def exists_file(self, filepath):
        """
        判断文件在目标路径是否存在
        :return:
        """
        out = self.shell("ls %s " % filepath)
        if "No such file or directory" in out:
            return False
        return True

    def root(self):
        self.cmd("root")
        self.cmd("remount")

    def enter_fastboot(self):
        logger.info("enter fastboot")
        self.install_busybox()
        self.shell('{ sleep 1; echo root ; sleep 10 ; echo reset -f; sleep 5 ; } | busybox telnet 198.18.32.11')
        time.sleep(5)

    def install_busybox(self):
        busybox_exist = self.shell('which busybox').rstrip()
        if 'busybox' not in busybox_exist:
            logger.info('busybox not exist, will push busybox to /system/bin/')
            busybox_path = os.path.join(os.path.dirname(__file__), 'busybox')
            logger.info(busybox_path)
            self.root()
            self.push(busybox_path, '/system/bin/busybox')
            self.shell('chmod a+x /system/bin/busybox')
        else:
            logger.info(f'busybox already exists in {busybox_exist}')

    def device_info(self):
        """
        Returns:
            Device Info
        """
        logger.info('return device info')
        return self.get_device_info()

    def file_size(self, filepath):
        if not os.path.isfile(filepath):
            logger.error("文件路径不存在，请检查")
        else:
            out = self.shell('ls -l %s' % filepath)
            try:
                file_size = int(out.split()[4])
            except ValueError:
                # 安卓6.0.1系统得到的结果是[3]为文件大小
                file_size = int(out.split()[3])
            return file_size


class ADBFailException(Exception):
    """
    An ADB fail even having retried to adb to the server
    """

    def __init__(self, value='ADB Fail'):
        self.value = value

    def __str__(self):
        return repr(self.value)


if __name__ == '__main__':
    a = Adb()
    print(a.shell("ps -A | grep power_manager_daemon | grep -v grep "))
    print(a.file_size('/tmp/data/hostname.txt'))
    print(a.shell("ps -A | grep phc2sys | grep -v grep", timeout=3))
