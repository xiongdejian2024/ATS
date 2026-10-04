
import os
import sys
import pickle
import time

import pytest
from xat_cases.legacy.bgm.case_helper.test_base import TestBase

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path.split("sat")[0], "sat"))
from xat_ecu.legacy.interface.tcam.tcam_ssh import *
from xat_ecu.legacy.common.logger import *

result = []


@pytest.mark.guard
class TestEcuStress(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        if os.path.exists('result.pkl'):
            os.remove('result.pkl')
        with open("result.pkl", mode='w', encoding='utf-8'):
            logger.info("result.pkl 文件创建成功！")

    def before_each_func(self, ecu):
        super().before_each_func(ecu)

    def after_each_func(self, ecu):
        super().after_each_func(ecu)

    def after_class(self, ecu):
        super().after_class(self, ecu)
        fw = open('result.pkl', 'wb')
        global result
        pickle.dump(result, fw)
        fw.close()

    @pytest.mark.run(order=1)
    @pytest.mark.restart
    def test_tcam_restart_five_coredump(self):
        """
        验证TCAM连续重启5次，是否产生coredump文件
        """
        global result
        TCAM_SSH().type_commands('rm -rf /mnt/sdcard/coredump/*')  # 删除已有的coredump文件
        for i in range(5):
            self.ecu_restart("tcam")
            time.sleep(120)
            file_count = TCAM_SSH().type_commands('ls -lrt /mnt/sdcard/coredump | grep root |wc -l')

            file_count = file_count.split('\n')[2].strip()
            logger.info(f"==========={file_count}")
            if int(file_count) > 0:
                """
                获取到文件数
                """
                file_names = TCAM_SSH().type_commands('ls /mnt/sdcard/coredump')
                file_names = file_names.split('\n')[2]
                result.append(perf_result("BGM", "coredump", False, f"TCAM 第{i+1}次重启检测到coredump文件：{file_names}"))
                assert False, f"TCAM 第{i+1}次重启检测到coredump文件{file_names}"
        else:
            result.append(perf_result("BGM", "coredump", True, f"TCAM 5次重启均未检测到coredump文件。"))
            logger.info(f"TCAM 5次重启均未检测到coredump文件。")
            assert True, f"TCAM 5次重启均未检测到coredump文件。"

    @pytest.mark.run(order=2)
    @pytest.mark.restart
    def test_tcam_restart_five_minute_cpu(self):
        """
        验证TCAM重启5分钟后，静态CPU使用率是否超过了70%
        """
        global result
        self.ecu_restart("tcam")
        logger.info(f"重启tcam，需要等待 5分钟")
        time.sleep(300)
        cpu_free_list = []
        for _ in range(5):
            logger.info(f"获取tcam cpu 占用率，链接tcam 成功后，需要几分钟")
            cpu_cost = TCAM_SSH().type_commands("top -d 30 -n 5  | grep CPU: | awk '{print $8}'")
            logger.info(f"获取 cpu_cost:{cpu_cost}")
            cpu_cost_list=[i.replace("%\r","") for i in cpu_cost.split("\n") if i.strip()]
            logger.info(f"获取 cpu_cost_list:{cpu_cost_list}")
            cpu_free_list = [float(i) for i in cpu_cost_list[1:-1]]
            if len(cpu_free_list)!=5:
                continue
            break
        else:
            assert False,"获取cpu 占用率失败"
        cpu_free_average= sum(cpu_free_list)/len(cpu_free_list)
        cup= 100-cpu_free_average
        logger.info(f"台架静态CPU，五次的平均使用率为{cup}")
        if cpu_free_average > 70.0:
            result.append(perf_result("TCAM", "cpu", False, f"台架静态CPU使用超过了 70%,当前CPU使用率平均值为{cup}"))
            assert False, f"台架静态CPU使用超过了 70%,当前CPU使用率平均值为{cup}"
        else:
            result.append(perf_result("TCAM", "cpu", True, f"台架静态CPU使用未超过了 70%, 当前CPU使用率平均值为{cup}"))
            assert True

    @pytest.mark.run(order=3)
    @pytest.mark.restart
    def test_tcam_restart_five_minute_mem(self):
        """
        验证TCAM重启5分钟后，台架剩余内存是否少于300M
        """
        global result
        self.ecu_restart("tcam")
        logger.info(f"重启tcam，需要等待 5分钟")
        time.sleep(300)
        mem_free_list = []
        for i in range(5):
            cpu_cost = TCAM_SSH().type_commands("top -n 1 | grep Mem | awk '{print $4,$8,$10}'")
            cpu_cost = cpu_cost.split('\n')[2]
            mem_free = 0
            for m in cpu_cost.split(' '):
                mem_free = mem_free + int(m.replace('K', ''))
            mem_free = mem_free // 1024
            logger.info(f"TCAM重启2分钟后，可用内存为{mem_free}M")
            mem_free_list.append(int(mem_free))
            time.sleep(60)
        if max(mem_free_list) < 300:
            result.append(perf_result("TCAM", "mem", False, f'当前可用内存{mem_free_list}，小于300M'))
            assert False, f'当前可用内存{mem_free_list}，小于300M'
        else:
            result.append(perf_result("TCAM", "mem", True, f'当前可用内存{mem_free_list}'))
            assert True, f'当前可用内存{mem_free_list}'

    def ecu_restart(self, domain):
        """
        重启ECU：domain为域名，可选值：bgm、tcam、cdc、acu
        """
        if domain == 'bgm':
            self.nucapp.bgm_power_off()
            time.sleep(5)
            self.nucapp.bgm_power_on()
        elif domain == 'tcam':
            self.nucapp.tcam_power_off()
            time.sleep(5)
            self.nucapp.tcam_power_on()
        elif domain == 'acu':
            self.nucapp.acu_power_off()
            time.sleep(5)
            self.nucapp.acu_power_on()
        elif domain == 'cdc':
            self.nucapp.cdc_power_off()
            time.sleep(5)
            self.nucapp.cdc_power_on()
        else:
            logger.info("ecu_restart not support!!!")


class perf_result:
    """
    target: BGM、TCAM
    type_name：coredump、cpu、mem
    result: True、False
    details：执行结果说明
    """
    def __init__(self, target, type_name, result, details):
        self.target = target
        self.type_name = type_name
        self.result = result
        self.details = details


if __name__ == '__main__':
    pytest.main()

