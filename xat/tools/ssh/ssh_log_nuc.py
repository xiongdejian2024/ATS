import os, sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))
sys.path.append(os.path.join(current_path, "../.."))
sys.path.append(os.path.join(current_path, "../../.."))

from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.interface.tcam.tcam_ssh import *


class SSH(object):
    def get_bgm_log(self):
        bgm_ssh = BGM_SSH()
        print("正在取BGM log...")
        bgm_ssh.get_log('/root/logs')
        print(bgm_ssh.pack_location)

    def get_tcam_log(self):
        print("正在取TCAM log...")
        tcam_ssh = TCAM_SSH()
        tcam_ssh.get_log('/root/logs', '/mnt/sdcard/log')

    def BGMorTCAM(self):
        if (sys.argv[1] == "BGM"):
            self.get_bgm_log()
        elif (sys.argv[1] == "TCAM"):
            self.get_tcam_log()
        elif (sys.argv[1] == "ALL"):
            self.get_bgm_log()
            self.get_tcam_log()
        else:
            print("输入的参数不正确，目前仅支持BGM or TCAM")


if __name__ == '__main__':
    SSH().get_tcam_log()
