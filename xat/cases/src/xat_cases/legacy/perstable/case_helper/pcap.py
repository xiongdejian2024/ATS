import shutil
from threading import Thread

from xat_ecu.legacy.sdk.sdk_tools import *
import os
import subprocess

from xat_cases.legacy.perstable.case_helper.constant import testParameter
from xat_cases.legacy.perstable.case_helper.Adb import ADB

class Pcap(object):
    def __init__(self, **kwargs):
        self.pcap_name = testParameter.get('pcap_name', 'bgm_static_unvlan_revise_mac_revise_ip.pcap')
        self.sf = SniffPacket()

        out, info = subprocess.getstatusoutput("sudo tcpreplay -V")
        output = subprocess.check_output(["sudo", "tcpreplay", "-V"])
        self.install_tcpreplay() if "tcpreplay version" not in info else ''

        self.logger = kwargs.get('logger', None)
        if logger:
            self.logger = logger
        else:
            logging.basicConfig(level=logging.INFO, stream=sys.stdout)
            self.logger = logging.getLogger(self.__class__.__name__)

    def install_tcpreplay(self):
        self.logger.info("install tcpreplay")
        os.system("sudo apt install libpcap-dev")
        os.system("sudo apt install tcpreplay")

    def start_pcap(self, pcap_file):
        """
        启动回放pcap
        """
        if os.path.exists(pcap_file):
            self.logger.error(f"{pcap_file} is not existed")
            exit(f"{pcap_file} is not existed")

        ifname = self.sf.get_network_card_name_by_ip()
        cmd_tcpreplay = f"sudo tcpreplay -i {ifname} -l 10000 {pcap_file}"
        self.logger.info(f"执行的指令为={cmd_tcpreplay}")
        out, info = subprocess.getstatusoutput(cmd_tcpreplay)

    def stop_pcap(self):
        process = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
        output, _ = process.communicate()

        # 查找包含指定命令的进程
        for line in output.decode().split('\n'):
            if 'tcpreplay -i' in line:
                pid = line.split()[1]  # 获取进程号
                # 杀死进程
                subprocess.call(['kill', pid])

    def pcap_thread(self):
        self.logger.info("get pcap thread")
        cmd = "ps -ef | grep tcpreplay"
        result = subprocess.check_output(cmd, shell=True)
        if self.pcap_name in result.decode('utf-8'):
            self.logger.info("Pcap Process is running")
            del result
            return True
        else:
            self.logger.info("Pcap Process is not running")
            del result
            return False


def pcap_thread_start(pcap_file):
    pcap_threading = Thread(
        target=Pcap().start_pcap,
        name="Pcap_Control",
        args=(pcap_file,),
        daemon=True,
    )
    pcap_threading.start()


if __name__ == '__main__':
    pcap_thread_start()
    for t in threading.enumerate():
        print(t)
    print("end")
