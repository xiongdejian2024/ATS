import os

from jas import CommonLib
from jal_terminal import *
from xat_cases.legacy.perstable.case_helper.constant import testParameter, WORK_PATH


class ADB:
    def __init__(self, adb_sn):
        self.adb = Adb(serialno=adb_sn)