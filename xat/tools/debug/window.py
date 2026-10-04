from PyQt5.Qt import *
from scapy.all import *
import sys
import psutil
import paramiko
import json
from query_bgm import query_bgm


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SOA测试")
        self.resize(790, 580)
        self.btn_start = QPushButton('开始', self)
        self.qcb_net_list = QComboBox(self)
        self.btn_conn = QPushButton('连接', self)
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.groupBox_getSalt = QGroupBox('GetSalt', self)

        self.func_list()

    def func_list(self):
        self.control_func()

    def control_func(self):

        self.btn_start.setGeometry(QRect(10, 20, 60, 30))
        self.btn_start.clicked.connect(query_bgm)

        self.qcb_net_list.setGeometry(QRect(90, 20, 170, 30))
        # self.qcb_net_list.currentIndexChanged.connect(self.get_net)

        self.btn_conn.setGeometry(QRect(280, 20, 60, 30))
        self.btn_conn.clicked.connect(self.net_conn)

        self.textEdit.setGeometry(QRect(360, 20, 230, 30))

        self.groupBox_getSalt.setGeometry(QRect(0, 0, 671, 70))

    def query_net_list(self):
        self.qcb_net_list.addItem("--请选择网卡--")
        for k, v in psutil.net_if_addrs().items():
            self.qcb_net_list.addItem(k)

    def Packcallback(self, pa):
        pass
        # pa.show()

    def net_conn(self):

        net_name = self.qcb_net_list.currentText()
        print(net_name)
        pack = sniff(iface=net_name, prn=self.Packcallback, count=1)
        wrpcap('file2.pcap', pack)
        # win32api.SetFileAttributes('file2.pcap',win32con.FILE_ATTRIBUTE_HIDDEN)
        pcaps = rdpcap("file2.pcap")
        packet = pcaps[0]
        print(packet['IP'].src)
        # os.remove('file2.pcap')
        ip = packet['IP'].src
        username = 'root'
        password = __import__("os").environ.get('XAT_CREDENTIAL____DEBUG_WINDOW_PY_PASSWORD', "")
        port = 22

        self.connect(ip, port, username, password)

    def connect(self, ip, port, username, password):
        connection = paramiko.SSHClient()
        connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        connection.connect(ip, port, username, password)

        cmd = "export JIDU_APP_LOG_PATH=/log/;\
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib;\
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib/soa;\
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib/proxy;\
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/service/em;\
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/service/prop;\
        export ENV_APP_PATH=/app/;\
        export ENV_APP_INFO=/app/etc/AppInfo.json;\
        export ENV_SOA_CONFIG_PATH=/app/etc/soaconfig/;\
        export ENV_CONFIG_PATH=/app/etc/;\
         cd /app/bin;   ./tprop get "

        stdin, stdout, stderr = connection.exec_command(cmd)
        str1 = stdout.read().decode('utf-8')
        connection.close()
        idx_asekey = str1.find('aeskey:')
        idx_aesiv = str1.find('aesiv:')
        idx_cmac = str1.find('cmac:')

        aes_str = str1[idx_asekey + 9:idx_aesiv]

        iv_str = str1[idx_aesiv + 8:idx_cmac]
        cmac_str = str1[idx_cmac + 7:idx_cmac + 56]

        aes_str_2 = aes_str.split()
        aes_key = self.getkey(aes_str_2)
        iv_str_2 = iv_str.split()
        iv_key = self.getkey(iv_str_2)
        cmac_str_2 = cmac_str.split()
        cmac_key = self.getkey(cmac_str_2)
        result = {
            "aes_key": aes_key,
            "aes_iv": iv_key,
            "cmac_key": cmac_key
        }
        with open("./slat.json", mode="w", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False, sort_keys=True))

        return result

    def getkey(self, str1):
        key1 = ''
        for item in str1:
            if len(item) == 2:
                key1 = key1 + item
            if len(item) == 1:
                key1 = key1 + "0"
                key1 = key1 + item
        return key1

    def get_net(self):
        net_name = self.qcb_net_list.currentText()
        print(net_name)


''' 
class query_window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.getNetlist.clicked.connect(self.query_netlist)
        # 给button 的 点击动作绑定一个事件处理函数

    def query_netlist(self):
        self.ui.comboBox_netlist.addItem("--请选择--")
        idx = 0
        str = []
        network = {}
        for k, v in psutil.net_if_addrs().items():
            self.ui.comboBox_netlist.addItem(k)

    def get_combBoxText(self):
        self.ui.comboBox_netlist.currentText()

        # 此处编写具体的业务逻辑
    def handelPacket(p):  # p捕获到的数据包
        p.show()

    pack = sniff(iface='eth0', prn=handelPacket, count=1)
    print('*****************')
    # print(pack[0])
    wrpcap('file2.pcap', pack)

    pcaps = rdpcap("file2.pcap")

    packet = pcaps[0]
    print(packet['IP'].src)
'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
