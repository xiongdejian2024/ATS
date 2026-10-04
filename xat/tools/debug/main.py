#!/usr/bin/env python
import paramiko
from PyQt5.Qt import *
import sys
import os
import gui
from PyQt5 import QtWidgets
import json
from doipclient import DoIPClient

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)
from xat_ecu.legacy.driver.ssh_client import SSHClient, SSHFailException
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH


class WindowClass(QMainWindow, gui.Ui_MainWindow):

    def __init__(self):
        super(WindowClass, self).__init__()
        self.setupUi(self)
        self.set_myUi()
        self.ip = self.bgm_ip()

    def set_myUi(self):
        self.getNetlist.clicked.connect(self.bgm_ip)
        self.getNetlist.clicked.connect(self.showdialog_ip)
        self.pushButton.clicked.connect(self.s_buttonState)
        self.pushButton.clicked.connect(self.showdialog_slat)
        self.getNetlist1.clicked.connect(self.b_buttonState)
        self.getNetlist1.clicked.connect(self.showdialog_bgm)
        self.getNetlist2.clicked.connect(self.t_buttonState)
        self.getNetlist2.clicked.connect(self.showdialog_tcam)
        self.pushButton11.clicked.connect(self.b_clear_digital)
        self.pushButton22.clicked.connect(self.t_clear_digital)
        self.pushButton31.clicked.connect(self.AESkey)
        self.pushButton32.clicked.connect(self.AESkey_recovery)

    def b_buttonState(self):
        try:
            conn = SSHClient(hostname=self.ip, port=22, username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____DEBUG_MAIN_PY_PASSWORD', ""))
        except SSHFailException as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/debug/main.py")
            logger.error(f'The server connect failed with error {e}')
            QtWidgets.QMessageBox.about(self, '连接BGM', "BGM连接超时")
            raise SSHFailException
        else:
            print('开始连接BGM')
            if conn.is_connected():
                data, error = conn.exec_cmd("ifconfig")
                print("BGM vlan展示:\n{}".format(data))
                QtWidgets.QMessageBox.about(self, '连接BGM', "BGM连接成功")
            else:
                QtWidgets.QMessageBox.about(self, '连接BGM', "BGM连接失败")

    def s_buttonState(self):
        try:
            data = Slat(self.ip, timeout=10)
            if data:
                QtWidgets.QMessageBox.about(self, '查看slat', 'slat获取成功')
        except SSHFailException as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/debug/main.py")
            logger.error(f'The server connect failed with error {e}')
            QtWidgets.QMessageBox.about(self, '获取slat', "BGM连接超时")
            raise SSHFailException

    def t_buttonState(self):
        try:
            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(hostname=self.ip, username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____DEBUG_MAIN_PY_PASSWORD', ""))
            transport = conn.get_transport()
            dest_addr = ("172.16.5.31", 22)  # edited#
            local_addr = (self.ip, 22)  # edited#
            channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

            conn1 = paramiko.SSHClient()
            conn1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn1.connect(hostname="172.16.5.31", username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____DEBUG_MAIN_PY_PASSWORD', ""), sock=channel)
            stdin, data, error = conn1.exec_command("ifconfig")
            print("TCAM vlan展示:\n{}".format(data.read().decode('utf-8')))
            QtWidgets.QMessageBox.about(self, '连接TCAM', f"TCAM连接成功")
        except SSHFailException as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/debug/main.py")
            logger.error(f'The server connect failed with error {e}')
            QtWidgets.QMessageBox.about(self, '连接TCAM', "TCAM连接超时")
            raise SSHFailException

    def t_clear_digital(self):
        try:
            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(hostname=self.ip, port=22, username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____DEBUG_MAIN_PY_PASSWORD', ""))
            transport = conn.get_transport()
            dest_addr = ("172.16.5.31", 22)
            local_addr = (self.ip, 22)
            channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

            conn1 = paramiko.SSHClient()
            conn1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn1.connect(hostname="172.16.5.31", username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____DEBUG_MAIN_PY_PASSWORD', ""), sock=channel)

            conn1.exec_command(f"rm -rf /oemdata_crit/etc/certificate/*")
            stdin, data, error = conn1.exec_command("ls -l /oemdata_crit/etc/certificate/")

            if not data:
                QtWidgets.QMessageBox.about(self, '清除TCAM证书', "清除失败")
            else:
                QtWidgets.QMessageBox.about(self, '清除TCAM证书', "清除成功")

        except SSHFailException as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/debug/main.py")
            QtWidgets.QMessageBox.about(self, '清除TCAM证书', "TCAM连接已断开")
            logger.error(f'The server connect failed with error {e}')
            raise SSHFailException

    def b_clear_digital(self):
        success = []
        try:
            conn = SSHClient(hostname=self.ip, port=22, username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____DEBUG_MAIN_PY_PASSWORD', ""))
            for i in ['/data/certificate', '/data/storage']:
                conn.exec_cmd(f"rm -rf {i}/*")
                data = conn.exec_cmd(f"ls {i}")
                if not data:
                    success.append(data)
            if len(success) == 0:
                QtWidgets.QMessageBox.about(self, '清除BGM证书', "清除成功")
            else:
                QtWidgets.QMessageBox.about(self, '清除BGM证书', "清除失败")

        except SSHFailException as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/debug/main.py")
            QtWidgets.QMessageBox.about(self, '清除BGM证书', "BGM连接已断开")
            logger.error(f'The server connect failed with error {e}')
            raise SSHFailException

    def bgm_ip(self):
        try:
            address, announcement = DoIPClient.await_vehicle_announcement(timeout=10)
            ip, port = address
            if ip:
                QtWidgets.QMessageBox.about(self, '获取BGM IP地址', "获取ip成功")
            else:
                QtWidgets.QMessageBox.about(self, '获取BGM IP地址', "获取ip失败")

        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/debug/main.py")
            logger.error(e)
            QtWidgets.QMessageBox.about(self, '获取BGM IP地址', "获取ip超时")
        else:
            return ip

    def showdialog_ip(self):
        ip = self.ip
        self.comboBox_netlist.setText(ip)

    def showdialog_slat(self):
        slat = f"json文件保存在{os.path.dirname(__file__)}/slat.json文件中"
        self.textEdit.setText(slat)

    def showdialog_bgm(self):
        self.comboBox_netlist1.setText("BGM已连接成功")

    def showdialog_tcam(self):
        self.comboBox_netlist2.setText("TCAM已连接成功")

    def AESkey(self):
        try:
            conn = SSHClient(hostname=self.ip, port=22, username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____DEBUG_MAIN_PY_PASSWORD', ""))
        except SSHFailException as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/debug/main.py")
            logger.error(f'The server connect failed with error {e}')
            QtWidgets.QMessageBox.about(self, '连接BGM', "BGM连接超时")
            raise SSHFailException
        else:
            print('开始绕行AESKey')
            if conn.is_connected():
                data1, error = conn.exec_cmd("ls /data/storage/")
                if "L7Aes.key" in data1 and "L7Aes_back.key" not in data1:
                    conn.exec_cmd("mv /data/storage/L7Aes.key /data/storage/L7Aes_back.key")
                    data, error = conn.exec_cmd("ls /data/storage/L7Aes_back.key")
                    if data == "/data/storage/L7Aes_back.key":
                        QtWidgets.QMessageBox.about(self, '绕行AESKey', "绕行AESKey成功")
                    else:
                        QtWidgets.QMessageBox.about(self, '绕行AESKey', "绕行AESKey失败")
                elif "L7Aes.key" not in data1 and "L7Aes_back.key" in data1:
                    QtWidgets.QMessageBox.about(self, '恢复AESKey', "请先恢复AESKey")
                else:
                    QtWidgets.QMessageBox.about(self, '恢复AESKey', "AESKey文件有误，请先检查BGM")

    def AESkey_recovery(self):
        try:
            conn = SSHClient(hostname=self.ip, port=22, username="root", password=__import__("os").environ.get('XAT_CREDENTIAL____DEBUG_MAIN_PY_PASSWORD', ""))
        except SSHFailException as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/debug/main.py")
            logger.error(f'The server connect failed with error {e}')
            QtWidgets.QMessageBox.about(self, '连接BGM', "BGM连接超时")
            raise SSHFailException
        else:
            print('开始恢复AESKey')
            if conn.is_connected():
                data1, error = conn.exec_cmd("ls /data/storage/")
                if "L7Aes.key" in data1 and "L7Aes_back.key" not in data1:
                    QtWidgets.QMessageBox.about(self, '恢复AESKey', "请先绕行AESKey")
                elif "L7Aes.key" not in data1 and "L7Aes_back.key" in data1:
                    conn.exec_cmd("mv /data/storage/L7Aes_back.key /data/storage/L7Aes.key")
                    data, error = conn.exec_cmd("ls /data/storage/L7Aes.key")
                    if data == "/data/storage/L7Aes.key":
                        QtWidgets.QMessageBox.about(self, '恢复AESKey', "恢复AESKey成功")
                    else:
                        QtWidgets.QMessageBox.about(self, '恢复AESKey', "恢复AESKey失败")
                else:
                    QtWidgets.QMessageBox.about(self, '恢复AESKey', "AESKey文件有误，请先检查BGM")


def Slat(hostname, timeout=None):
    # try:
    #     connection = paramiko.SSHClient()
    #     connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #     connection.connect(hostname=hostname, port=22, username="root", password="mars1bgm", timeout=timeout)
    # except SSHFailException as e:
    #     logger.error(f'The server connect failed with error {e}')
    #     raise SSHFailException

    # else:
    #     cmd = "export JIDU_APP_LOG_PATH=/log/;\
    #     export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib;\
    #     export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib/soa;\
    #     export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib/proxy;\
    #     export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/service/em;\
    #     export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/service/prop;\
    #     export ENV_APP_PATH=/app/;\
    #     export ENV_APP_INFO=/app/etc/AppInfo.json;\
    #     export ENV_SOA_CONFIG_PATH=/app/etc/soaconfig/;\
    #     export ENV_CONFIG_PATH=/app/etc/;\
    #      cd /app/bin;   ./tprop get "

    #     stdin, stdout, stderr = connection.exec_command(cmd)
    #     str1 = stdout.read().decode('utf-8')
    #     print(str1)
    #     connection.close()
    #     idx_asekey = str1.find('aeskey:')
    #     idx_aesiv = str1.find('aesiv:')
    #     idx_cmac = str1.find('cmac:')
    #     idx_init = str1.find("Init")

    #     aes_str = str1[idx_asekey + 9:idx_aesiv]
    #     iv_str = str1[idx_aesiv + 8:idx_cmac]
    #     cmac_str = str1[idx_cmac + 7:idx_init]
        # print(type(aes_str))
        # print(iv_str)
        # print(cmac_str)
        # aes_str_2 = aes_str.split()
        # aes_key = getkey(aes_str_2)
        # iv_str_2 = iv_str.split()
        # iv_key = getkey(iv_str_2)
        # cmac_str_2 = cmac_str.split()
        # cmac_key = getkey(cmac_str_2)
        str1,aes_key,iv_key,cmac_key = BGM_SSH().get_tprop()
        result = {
            "aes_key": aes_key,
            "aes_iv": iv_key,
            "cmac_key": cmac_key
        }
        with open("./slat.json", mode="w", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False, sort_keys=True))

        return result


def getkey(str1):
    key1 = ''
    for item in str1:
        if len(item) == 2:
            key1 = key1 + item
        if len(item) == 1:
            key1 = key1 + "0"
            key1 = key1 + item
    return key1


if __name__ == '__main__':
    print("开始测试")
    # 1、创建QApplication类的实例对象
    app = QApplication(sys.argv)
    # 2、创建一个WindowClass实例对象
    myMainWindow = WindowClass()
    # 3、显示主窗口
    myMainWindow.show()
    # 4、进入程序的主循环、并通过exit函数确保主循环安全结束
    sys.exit(app.exec_())
