
import os
import sys
import pickle
import time

import pytest

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path.split("sat")[0], "sat"))
from xat_cases.legacy.bgm.case_helper.test_base import TestBase
from xat_ecu.legacy.interface.tcam.tcam_ssh import *
from xat_ecu.legacy.common.logger import *


# @pytest.mark.guard
class TestEcuRestart(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)

    # @pytest.mark.smoke
    @pytest.mark.run(order=1)
    def test_bgm_restart(self):
        """
        验证BGM静默五分钟内是否发生重启
        """

        hours_before, minutes_before = bgm_get_current_hours_minutes(self.bgmcli)
        time.sleep(5*60)
        try:
            hours_after, minutes_after = bgm_get_current_hours_minutes(self.bgmcli)
        except Exception:
            assert False, "BGM 动态IP发生变化"
        if (hours_after*60 + minutes_after) >= (hours_before*60 + minutes_before + 4):
            assert True
        else:
            assert False


def bgm_get_current_hours_minutes(bgm_client):
    result = bgm_client.type_commands("uptime -p")
    logger.info("命令执行结果：{}".format(result))
    result_list = result.split(" ")
    if "hours" in result:
        hours_before = result_list[result_list.index("hours,") - 1]
    elif "hour" in result:
        hours_before = result_list[result_list.index("hour,") - 1]
    else:
        hours_before = 0
    if "minutes" in result:
        minutes_before = result_list[result_list.index("minutes") - 1]
    else:
        minutes_before = 0
    logger.info(f"当前时间：{hours_before}小时，{minutes_before}分钟")
    return to_int(hours_before), to_int(minutes_before.strip())


def to_int(m_str):
    try:
        int(m_str)
        return int(m_str)
    except ValueError:
        try:
            float(m_str)
            return int(float(m_str))
        except ValueError:
            return False


if __name__ == '__main__':
    pytest.main()

