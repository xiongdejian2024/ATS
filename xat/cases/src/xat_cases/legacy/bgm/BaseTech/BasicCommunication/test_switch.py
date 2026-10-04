import subprocess
import pytest
import allure
import pytest
import allure
import re
from xat_cases.legacy.bgm.mcu.case_helper.test_abc_base import TestABCBase 
from xat_ecu.api.common.common import *


@pytest.mark.mcu_test
@allure.feature("通讯功能/以太网通讯")
@allure.story("以太网通讯")
class Test_Switch(TestABCBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        current_path = os.path.join(os.getcwd(),"mcu/config_data/vlan/switch_vlan5.sh")
        with open(current_path,"r") as f:
            lines = f.readlines()
            li = []
            for index,data in enumerate(lines):
                vlan_name = re.findall("add link (.*?) name",data)
                if vlan_name:
                    new_vlan_name = lines[index].replace(vlan_name[0],ecu.tc_config['eth_vlan'])
                    li.append(new_vlan_name)
                else:
                    li.append(data)

        with open(current_path,"w") as f:
            for i in li:
                f.write(i)


    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        # Code Location

    def after_each_func(self, ecu):
        # Code Location
        super().after_each_func(ecu)

    def after_class(self, ecu):
        # Code Location
        res1 = os.popen("ifconfig").read()
        if "eth0.32" in res1:
            os.popen(f"ip link delete eth0.32")
            for i in ["eth0.5","eth0.9","eth0.21","eth0.22"]:
                os.popen(f"ip link delete {i}")
        else:
            for i in ["eth0.5","eth0.9","eth0.21","eth0.22"]:
                os.popen(f"ip link delete {i}")
        subprocess.run("/root/usb_vlan5.sh",shell=True)
        res2 = os.popen("ifconfig").read()
        logger.info(f"after class ifconfig 执行结果 {res2}")
        super().after_class(self, ecu)


    @pytest.mark.smoke
    def test_BGMSOC_VLAN5_31_caseid_113054(self):
        """
        设置PC端VLAN5网络IP172.16.5.31,ether02:00:00:00:10:31
        ping BGM及172.16.5.1
        """
        self.mix.change_ip_and_id("172.16.5.31","02:00:00:00:10:31","eth0.5")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.5.1")
        
    @pytest.mark.smoke
    def test_BGMSOC_VLAN5_11_caseid_113053(self):
        """
        设置PC端VLAN5网络IP172.16.5.11,ether02:00:00:00:10:11
        ping BGM及172.16.5.1
        """
        self.mix.change_ip_and_id("172.16.5.11","02:00:00:00:10:11","eth0.5")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.5.1")

    @pytest.mark.smoke
    def test_BGMSOC_VLAN5_13_caseid_113052(self):
        """
        设置PC端VLAN5网络IP172.16.5.13,ether02:00:00:00:10:13
        ping BGM及172.16.5.1
        """
        self.mix.change_ip_and_id("172.16.5.13","02:00:00:00:10:13","eth0.5")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.5.1")

    @pytest.mark.smoke
    def test_BGMSOC_VLAN5_21_caseid_113051(self):
        """
        设置PC端VLAN5网络IP172.16.5.21,ether02:00:00:00:10:21
        ping BGM及172.16.5.1
        """
        self.mix.change_ip_and_id("172.16.5.21","02:00:00:00:10:21","eth0.5")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.5.1")

    @pytest.mark.smoke
    def test_BGMSOC_VLAN5_23_caseid_113050(self):
        """
        设置PC端VLAN5网络IP172.16.5.23,ether02:00:00:00:10:23
        ping BGM及172.16.5.1
        """
        self.mix.change_ip_and_id("172.16.5.23","02:00:00:00:10:23","eth0.5")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.5.1")

    @pytest.mark.smoke
    def test_BGMSOC_VLAN32_31_caseid_113049(self):
        """
        设置PC端VLAN32网络172.16.32.31,ether02:00:00:00:10:31
        ping BGM及ping172.16.32.1
        """
        self.mix.change_ip_and_id("172.16.32.31","02:00:00:00:10:31","eth0.32")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.32.1")

    @pytest.mark.smoke
    def test_BGMSOC_VLAN32_11_caseid_113048(self):
        """
        设置PC端VLAN32网络172.16.32.11,ether02:00:00:00:10:11
        ping BGM及ping172.16.32.1
        """
        self.mix.change_ip_and_id("172.16.32.11","02:00:00:00:10:11","eth0.32")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.32.1")

    @pytest.mark.smoke
    def test_BGMSOC_VLAN32_13_caseid_113047(self):
        """
        设置PC端VLAN32网络172.16.32.13,ether02:00:00:00:10:13
        ping BGM及ping172.16.32.1
        """
        self.mix.change_ip_and_id("172.16.32.13","02:00:00:00:10:13","eth0.32")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.32.1")
    
    @pytest.mark.smoke
    def test_BGMSOC_VLAN32_21_caseid_113046(self):
        """
        设置PC端VLAN32网络172.16.32.21,ether02:00:00:00:10:21
        ping BGM及ping172.16.32.1
        """
        self.mix.change_ip_and_id("172.16.32.21","02:00:00:00:10:21","eth0.32")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.32.1")

    @pytest.mark.smoke
    def test_BGMSOC_VLAN32_23_caseid_113045(self):
        """
        设置PC端VLAN32网络172.16.32.23,ether02:00:00:00:10:23
        ping BGM及ping172.16.32.1
        """
        self.mix.change_ip_and_id("172.16.32.23","02:00:00:00:10:23","eth0.32")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.32.1")

    @pytest.mark.smoke
    def test_BGMSOC_VLAN9_31_caseid_113044(self):
        """
        设置PC端VLAN9网络172.16.9.31,ether02:00:00:00:10:31
        ping BGM及172.16.9.1
        """
        self.mix.change_ip_and_id("172.16.9.31","02:00:00:00:10:31","eth0.9")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.9.1")

    @pytest.mark.smoke
    def test_BGMSOC_VLAN9_11_caseid_113043(self):
        """
        设置PC端VLAN9网络172.16.9.11,ether02:00:00:00:10:11
        ping BGM及172.16.9.1
        """
        self.mix.change_ip_and_id("172.16.9.11","02:00:00:00:10:11","eth0.9")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.9.1")

    @pytest.mark.smoke
    def test_BGMSOC_VLAN9_12_caseid_113042(self):
        """
        设置PC端VLAN9网络172.16.9.12,ether02:00:00:00:10:12
        ping BGM及172.16.9.1
        """
        self.mix.change_ip_and_id("172.16.9.12","02:00:00:00:10:12","eth0.9")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.9.1")

    @pytest.mark.smoke
    def test_BGMSOC_VLAN9_13_caseid_113041(self):
        """
        设置PC端VLAN9网络172.16.9.13,ether02:00:00:00:10:13
        ping BGM及172.16.9.1
        """
        self.mix.change_ip_and_id("172.16.9.13","02:00:00:00:10:13","eth0.9")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.9.1")

    @pytest.mark.smoke
    def test_BGMSOC_VLAN9_21_caseid_113040(self):
        """
        设置PC端VLAN9网络172.16.9.21,ether02:00:00:00:10:21
        ping BGM及172.16.9.1
        """
        self.mix.change_ip_and_id("172.16.9.21","02:00:00:00:10:21","eth0.9")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.9.1")

    @pytest.mark.smoke
    def test_BGMSOC_VLAN9_23_caseid_113039(self):
        """
        设置PC端VLAN9网络172.16.9.23,ether02:00:00:00:10:23
        ping BGM及172.16.9.1
        """
        self.mix.change_ip_and_id("172.16.9.23","02:00:00:00:10:23","eth0.9")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.9.1")

    @pytest.mark.smoke
    def test_BGMSOC_VLAN9_25_caseid_113038(self):
        """
        设置PC端VLAN9网络172.16.9.25,ether02:00:00:00:10:25
        ping BGM及172.16.9.1
        """
        self.mix.change_ip_and_id("172.16.9.25","02:00:00:00:10:25","eth0.9")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.9.1")
    
    @pytest.mark.smoke
    def test_BGMMCU_VLAN9_31_caseid_113035(self):
        """
        设置PC端VLAN9网络172.16.9.31,ether02:00:00:00:10:31
        ping BGM及ping172.16.9.2
        """
        self.mix.change_ip_and_id("172.16.9.31","02:00:00:00:10:31","eth0.9")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.9.2")

    @pytest.mark.smoke
    def test_BGMSOC_VLAN5_2_caseid_111992(self):
        """
        ssh  进入到BGM ;输入ip neigh show指令
        系统返回存在以下内容：172.16.5.2 dev eth0.5 lladdr 02:00:00:00:10:02 PERMANENT
        """
        res = self.ssh.type_commands(DeviceName.BGM,"ip neigh show")
        str = "172.16.5.2 dev eth0.5 lladdr 02:00:00:00:10:02 PERMANENT"
        if str not in res:
            assert False,f"进入BGM执行 ip neigh show 指令后,未发现 {str} "

    @pytest.mark.smoke
    def test_BGMSOC_VLAN9_2_caseid_111991(self):
        """
        ssh  进入到BGM ;输入ip neigh show指令
        系统返回存在以下内容：172.16.9.2 dev eth0.9 lladdr 02:00:00:00:10:02 PERMANENT
        """
        res = self.ssh.type_commands(DeviceName.BGM,"ip neigh show")
        str = "172.16.9.2 dev eth0.9 lladdr 02:00:00:00:10:02 PERMANENT"
        if str not in res:
            assert False,f"进入BGM执行 ip neigh show 指令后,未发现 {str} "
        
        
    @pytest.mark.smoke
    def test_BGMMCU_VLAN9_1_caseid_1912715(self):
        """
        在BGM输入arping172.16.9.2
        可以ping通BGM
        """
        self.mix.ping_bgm_ip_and_vlan_ip("172.16.9.2",ping="get_arping")
 
    
    @pytest.mark.smoke
    def test_BGMMCU_VLAN5_1_caseid_109879(self):
        """
        在BGM输入arping172.16.5.2
        可以ping通BGM
        """
        self.mix.ping_bgm_ip_and_vlan_ip("172.16.5.2",ping="get_arping")

    @pytest.mark.smoke
    def test_BGMMCU_VLAN5_31_caseid_109878(self):
        """
        设置PC端VLAN5网络IP172.16.5.31,ether02:00:00:00:10:31
        在PC端执行命令ping172.16.5.2
        """
        self.mix.change_ip_and_id("172.16.5.31","02:00:00:00:10:31","eth0.5")
        self.mix.ping_bgm_ip_and_vlan_ip("169.254.19.1","172.16.5.2")
