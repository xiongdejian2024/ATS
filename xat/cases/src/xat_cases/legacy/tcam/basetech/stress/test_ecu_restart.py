
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


@pytest.mark.guard
class TestEcuRestart(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)

    @pytest.mark.run(order=1)
    def test_tcam_restart(self):
        """
        验证TCAM静默五分钟内是否发生重启
        """
        hours_before, minutes_before = tcam_get_current_hours_minutes()
        time.sleep(5*60)
        try:
            hours_after, minutes_after = tcam_get_current_hours_minutes()
        except Exception:
            assert False, "BGM 动态IP发生变化"
        logger.info("######################")
        logger.info(f"hours_before:{hours_before}")
        logger.info(f"minutes_before:{minutes_before}")
        logger.info(f"{hours_before * 60 + minutes_before + 4}")
        logger.info("----------------------")
        logger.info(f"hours_after:{hours_after}")
        logger.info(f"minutes_after:{minutes_after}")
        logger.info(f"{hours_after * 60 + minutes_after}")
        logger.info("######################")
        if (hours_after*60 + minutes_after) >= (hours_before*60 + minutes_before + 4):
            assert True
        else:
            assert False


def tcam_get_current_hours_minutes():
    result = TCAM_SSH().type_commands('uptime -p')
    result = result.split('\n')[2].strip()
    if 'day' in result:
        result = result.split("load average")[0].split("day")[1].replace(",", "").strip()
    else:
        result = result.split("load average")[0].split("up")[1].replace(",", "").strip()
    logger.info("命令执行结果:{}".format(result))

    result_list = result.split(":")
    if len(result_list) == 2:
        hours = result_list[0]
        minutes = result_list[1]
    else:
        hours = 0
        minutes = result_list[0].split(" ")[0]
    logger.info(f"当前时间：{hours}小时，{minutes}分钟")
    return to_int(hours), to_int(minutes.strip())


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
