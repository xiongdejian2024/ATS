
import os
import sys
import pickle
import time

import pytest
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
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
    def test_bgm_restart_five_coredump(self):
        """
        验证BGM连续重启5次，是否产生coredump文件
        """
        self.bgmcli.type_commands("rm -rf /log/coredump/*")  # 执行用例前删除已存在的coredump文件
        global result
        for i in range(5):
            self.ecu_restart("bgm")
            time.sleep(120)
            # 重新获取obdip，解决重启后obdip变化的问题
            self.obdip = self.nucapp.get_announcement_ip()
            try:
                if self.obdip:
                    self.tc_config["gateway_ip"] = self.obdip
                    self.bgmcli = BGM_SSH(hostname=self.obdip)
                else:
                    self.bgmcli = BGM_SSH()
            except Exception as e:
                assert False, f"ssh 连接失败 {str(e)}"

            file_count = self.bgmcli.type_commands('ls -lrt /log/coredump/ | grep root |wc -l')
            logger.info(f"第{i}次重启，获取到的coredump文件数: {file_count}")
            if int(file_count) > 0:
                file_names = self.bgmcli.type_commands('ls /log/coredump/')
                logger.info(f"BGM 第{i+1}次重启检测到coredump文件{file_names}")
                result.append(perf_result("BGM", "coredump", False, f"BGM 第{i+1}次重启检测到coredump文件{file_names}"))
                assert False, f"BGM 第{i+1}次重启检测到coredump文件{file_names}"
            else:
                continue
        else:
            result.append(perf_result("BGM", "coredump", True, "BGM 5次重启均未检测到coredump文件。"))
            logger.info(f"BGM 5次重启均未检测到coredump文件。")
            assert True, f"BGM 5次重启均未检测到coredump文件。"

    @pytest.mark.run(order=2)
    @pytest.mark.restart
    def test_bgm_restart_five_minute_cpu(self):
        """
        验证BGM重启5分钟后，台架静态CPU是否超过了50%
        """
        global result
        self.ecu_restart("bgm")
        logger.info(f"重启 bgm 需要等待 5分钟")
        time.sleep(300)
        # 重新获取obdip，解决重启后obdip变化的问题
        self.obdip = self.nucapp.get_announcement_ip()
        try:
            if self.obdip:
                self.tc_config["gateway_ip"] = self.obdip
                self.bgmcli = BGM_SSH(hostname=self.obdip)
            else:
                self.bgmcli = BGM_SSH()
        except Exception as e:
            assert False, f"ssh 连接失败 {str(e)}"
        cpu_infos = []
        # 尝试五次 有一次成功就跳出
        for _ in range(5):
            logger.info(f"获取bgm cpu 占用率,需要几分钟")
            remote_log = self.bgmcli.type_commands("top -d 30 -n 5  | grep Cpu | awk '{print $8}'",timeout=300)
            logger.info(f"获取remote——{remote_log}")
            cpu_infos = [float(i) for i in remote_log.split("\n") if i.strip()]
            if len(cpu_infos)!=5:
                continue
            break
        else:
            assert False,"获取cpu 占用率失败"
        
        aver_cpu = sum(cpu_infos)/len(cpu_infos)
        temp = 100-aver_cpu
        logger.info(f"台架静态CPU空闲率={aver_cpu},使用率为={temp}")
        
        if temp>50:
             assert False, f"台架静态CPU使用率超过了50%, 当前CPU平均使用率{temp}"
        else:
            assert True, f"台架重启5分钟后静态CPU正常 当前CPU平均使用率{temp}"

    @pytest.mark.run(order=3)
    @pytest.mark.restart
    def test_bgm_restart_five_minute_mem(self):
        """
        验证BGM重启5分钟后，台架剩余内存是否少于500M
        """
        global result
        self.ecu_restart("bgm")
        logger.info(f"重启 bgm 需要等待 5分钟")
        time.sleep(300)
        # 重新获取obdip，解决重启后obdip变化的问题
        self.obdip = self.nucapp.get_announcement_ip()
        try:
            if self.obdip:
                self.tc_config["gateway_ip"] = self.obdip
                self.bgmcli = BGM_SSH(hostname=self.obdip)
            else:
                self.bgmcli = BGM_SSH()
        except Exception as e:
            assert False, f"ssh 连接失败 {str(e)}"
        mem_free_list = []
        for i in range(5):
            cpu_cost = self.bgmcli.type_commands('vmstat | tail -n 1 | awk \'END{print $4,$5,$6}\'')
            cpu_cost = cpu_cost.split(' ')
            mem_free = 0
            for m in cpu_cost:
                mem_free = mem_free + int(m)
            logger.info(f"{mem_free}")
            mem_free = mem_free // 1024
            mem_cost = 858 - mem_free
            logger.info(f"BGM重启1分钟后，MEM剩余{mem_free}M")
            logger.info(f"BGM重启1分钟后，MEM消耗信息{mem_cost}M")
            mem_free_list.append(mem_free)
            time.sleep(60)
        if max(mem_free_list) < 500:
            result.append(perf_result("BGM", "mem", False, f"台架剩余内存少于500M，当前剩余为{mem_free_list}M"))
            assert False, f"台架剩余内存少于500M，当前剩余为{mem_free_list}M"
        else:
            result.append(perf_result("BGM", "mem", True, f"BGM重启1分钟后，MEM剩余{mem_free_list}M"))
            assert True, f"BGM重启1分钟后，MEM剩余{mem_free_list}M"

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

