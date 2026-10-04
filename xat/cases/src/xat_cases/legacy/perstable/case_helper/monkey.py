import pdb
import re
import threading
from threading import Thread

from xat_cases.legacy.perstable.case_helper.Adb import ADB
from xat_cases.legacy.perstable.case_helper.constant import testParameter, JOB_PATH


class Monkey(object):
    def __init__(self):
        self.cdc_device_id = testParameter.get("cdc_device_id")
        self.cdc_adb = ADB(self.cdc_device_id)

    def start_monkey(self):
        monkey_cmd = ("-s {} shell monkey -p com.jidu.settings -p com.jidu.map -p com.jidu.media.hall "
                      "-p com.jidu.media.iqy -p com.jidu.media.ktv -s 200 --throttle 500  --ignore-crashes "
                      "--ignore-timeouts --ignore-security-exceptions --monitor-native-crashes -v -v -v 1000000 "
                      ">/sdcard/monkey.log").format(self.cdc_device_id)
        self.cdc_adb.adb.cmd(monkey_cmd)

    def stop_monkey(self):
        out = self.cdc_adb.adb.shell(f"ps -ef |grep monkey").strip()
        if out:
            pid = re.findall(r'\d+', out)[0]
            self.cdc_adb.adb.shell(f"kill -9 {pid}")

    def monkey_states(self):
        out = self.cdc_adb.adb.shell("ps -ef |grep monkey").strip()
        if "com.android.commands.monkey" in out:
            return True
        else:
            return False


def monkey_thread_start():
    monkey_threading = Thread(
        target=Monkey().start_monkey,
        name="Monkey_Control",
        args=(),
        daemon=True,
    )
    monkey_threading.start()


if __name__ == '__main__':
    monkey_thread_start()
    for t in threading.enumerate():
        print(t)
    print("end")
