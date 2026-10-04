# -*- coding: utf-8 -*-
"""
@File        : test_update_mcu
@Author      : tanggeng.li@jiduauto.com
@Time        : 2023/10/10 20:10
@Description : 包含 mcu 升级的相关的一些操作

"""
import copy
import json
import time
import requests
import pytest
import sys, os

project_root = os.path.join(os.getcwd().split("sat")[0], 'sat')
sys.path.append(project_root)

work_path_2 = os.path.join(os.getcwd().split("sat")[0], 'sat', 'ecu_simulator', 'interface')
sys.path.append(work_path_2)
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

import base64
from xat_ecu.legacy.sdk.ecu_sim_const import ECUSimConst
from xat_ecu.legacy.interface.bgm.bgm_ssh import BGM_SSH
from xat_ecu.legacy.sdk.sdk_tools import *
from pathlib import Path
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.config.path import CONFIG_DIR_PATH
from xat_ecu.legacy.ecu_sim.parse_tb_config import ParseTBConfig

# from ecu_simulator.interface.bgm.bgm_env.change_bgm_env import *
from time import sleep

forder0 = Path(__file__).resolve().parents[1]  # mcu


class MCU_Interface(object):
    def __init__(self):
        tb_path = os.path.join(CONFIG_DIR_PATH, "willow_bgm_flash_config.yaml")
        tb_config = ParseTBConfig(tb_path)
        self.sd_tc_config = tb_config.yaml_content

        self.sd_test = None
        self.bgm_ssh = BGM_SSH()
        # 存放每个bus（can lin  fr） 上所有的数据
        self.__all_bus_data_info = {}

    def reset_bgm(self, nucapp=None, time_delay=40):
        '''
        重启bgm
        @param nucapp:
        @param time_delay: 重启后延时时间 默认40s
        @return:
        '''

        if nucapp:
            # 重启
            nucapp.bgm_power_off()
            time.sleep(10)
            nucapp.bgm_power_on()
            logger.info(f"bgm重启延时{time_delay}s")
            time.sleep(time_delay)
        else:
            try:
                sd_tester = Sd_Tester(**self.sd_tc_config)
                sd_tester.diagnostic_client_sim_start()
                sleep(0.5)
                sd_tester.update_serverdoipid(0x1002)
                sleep(0.5)
                sd_tester.send_data([0x11, 0x81])
                time.sleep(0.5)
                sd_tester.diagnostic_client_sim_close()
                logger.info(f"bgm重启延时{time_delay}s")
                time.sleep(time_delay)
            except Exception as e:
                logger.warning(f"重启失败==》》{str(e)}")
                assert 0, "修改成功bgm 配置成功，重启失败，可能无法生效"

    def prepare_mcu_update_env(self):
        '''
        准备升级环境
        @return:
        '''

        # 获取版本号
        version = self.get_bgm_version()

        # https://wiki.jiduauto.com/pages/viewpage.action?pageId=749061160
        # 在/data/目录下创建一个目录"mkdir /data/uatest"

        self.bgm_ssh.create_bgm_uatest_file()

        # 2、输入指令”cp /app/etc/runenv.sh /data/debug.sh“将/app/etc/runenv.sh文件拷贝至/data/目录下并命名为debug.sh
        self.bgm_ssh.push_debug_file_to_bgm_data()

        # ”rm /data/debug_script_executed_count“防止BGM重启满二十次删除的debug.sh脚本。
        self.bgm_ssh.delete_debug_script_executed_count()
        # 4.输入指令“cp /app/etc/bgm_app_env.sh /data/bgm_app_env.sh"将/app/etc/bgm_app_env.sh脚本拷贝至/data/目录下，
        self.bgm_ssh.push_bgm_app_env_file_to_bgm_data()

        # 5、输入指令"cp -rf /app/etc/* /data/etc/"拷贝相应文件
        cmd = "cp -rf /app/etc/* /data/etc/"
        ret = self.bgm_ssh.type_commands(cmd)
        # 6、将/data/etc/app_info.json中name为ua_XXX的path修改为/data/uatest/
        self.bgm_ssh.push_app_info_json_file_to_bgm_data()
        # 7 然后将编译的arm版本的ua相关动态库与app：libua_service.so、ua_client_app、ua_server_app拷贝到bgm中/data/uatest/目录下，修改文件权限”chmod 777 /data/uatest/*"

        self.bgm_ssh.push_ua_files_to_bgm_data(version)

        # 8、创建/data/jiarui/目录，将ua_file_info.json文件放入/data/jiarui/。
        self.bgm_ssh.push_ua_file_info_json_to_bgm_data()
        # sync落盘后修改bgm启动方式为冷启动”/app/bin/swdl -nw 10 1“。热启动指令：/app/bin/swdl -nw 10 0
        self.bgm_ssh.set_bgm_cold_start()

        self.bgm_ssh.set_bgm_sync()
        #
        self.reset_bgm(nucapp=None)

    def restore_mcu_update_env(self):
        '''
        恢复环境
        @return:
        '''
        # 删除 文件

        cmd_list = [
            "rm -rf /data/debug.sh",
            "rm -rf /data/uatest",
            "rm -rf /data/jiarui",
            "rm -rf /data/bgm_app_env.sh",
            # "rm -rf /data/etc"
        ]

        for cmd in cmd_list:
            self.bgm_ssh.type_commands(cmd)

        cmd = "ls /data/"
        ret = self.bgm_ssh.type_commands(cmd)
        name_List = ret.split()
        logger.warning(f"name_List=》》{name_List}")
        if "debug.sh" in name_List:
            assert 0, " 环境恢复失败 debug.sh 还存在"

        self.bgm_ssh.set_bgm_hot_start()

        self.bgm_ssh.set_bgm_sync()
        #
        self.reset_bgm(nucapp=None)

    def get_bgm_version(self):
        '''
        获取bgm的那个版本  130 ，140
        @return:
        '''
        ver_dic = self.bgm_ssh.get_version()
        version = ver_dic.get('build_version', None)
        if version:
            # 'build_version': '6160110140 AN'
            version = int(version[7:10])  # 140
        return version

    def get_mcu_zip_url(self,url=None):
        '''
        获取 mcu 版本的 所有链接
        @param url:  默认是 https://repo.jidudev.com/artifactory/BGM_Aptiv/DailyBuild/MCU/
        @return:
        '''
        username = base64.b64decode(ECUSimConst.SOA_PUBLIC.encode()).decode()
        password = base64.b64decode(ECUSimConst.SOA_PUBLIC_PD.encode()).decode()
        data = f"{username}:{password}"
        Authorization = base64.b64encode(data.encode()).decode()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {Authorization}'
        }
        if url is None:
            url = "https://repo.jidudev.com/artifactory/BGM_Aptiv/DailyBuild/MCU/"

        try:
            logger.info(f"请求的路径为》》》{url}")
            msg = requests.get(url, headers=headers)
            recv_msg = msg.text
            logger.info(f'对url 请求返回值》》》{recv_msg}')
            version_list = re.findall('<a href="(.*?)/">v', recv_msg)
            logger.info(f"获取到的mcu 所有大版本名称为》》》{version_list}")
            last_version = version_list[-1]
            last_url = os.path.join(url, last_version)
            logger.info(f"请求的版本路径为》》》{last_url}")
            msg = requests.get(last_url, headers=headers)
            recv_msg = msg.text
            logger.info(f'对 url 请求返回值》》》{recv_msg}')
            mcu_name_list = re.findall('zip">(.*?)</a>', recv_msg)
            logger.info(f"获取到的mcu 所有版本名称为》》》{mcu_name_list}")
            mcu_url_list = [os.path.join(last_url, item) for item in mcu_name_list]
            logger.info(f"获取到的mcu 所有版本路径为》》》{mcu_url_list}")
            return mcu_url_list
        except Exception as e:
            logger.error(f"获取mcu 版本路径失败，{str(e)}")
            return None

    def down_load_file(self, file_url):
        '''
        根据路径下载升级所需的  文件
        @param file_url: 升级的bin 文件路径 如 "https://repo.jidudev.com/artifactory/TCAMSoftware/Release_build/6110110055BD.bin"
        @return:
        '''
        username = base64.b64decode(ECUSimConst.SOA_PUBLIC.encode()).decode()
        password = base64.b64decode(ECUSimConst.SOA_PUBLIC_PD.encode()).decode()
        file_name = file_url.split("/")[-1]
        file_path0 = os.path.join(forder0, "mcu_zip" )
        if not os.path.exists(file_path0):
            os.mkdir(file_path0)
        file_path = os.path.join(file_path0,  file_name)

        logger.info(f"Path: {file_path} file_name={file_name}")
        if os.path.isfile(file_path.replace('\\', '')):
            logger.info("Path: {} is exit, need not to download".format(file_path))
        else:
            download_cmd = f"curl -o {file_path} -u {username}:{password} {file_url}"
            logger.info(f"cmd={download_cmd}")
            os.system(download_cmd)
        return file_path

    def unzip_mcu_zip(self, zip_file, **kwargs):
        '''
        解压 mcu 的zip包
        @param zip_file:
        @param kwargs:
        @return:
        '''
        file_name = os.path.basename(zip_file)[:-4]
        file_name_path = os.path.join(forder0, "mcu_zip/" + file_name).replace("&", "")
        logger.info(f"file_name={file_name},file_name_path={file_name_path}")
        # 删除 文件夹
        # file_path = file_name_path.replace('\\', '')
        cmd = f"rm -rf {file_name_path}"
        logger.info(f"执行删除指令==》{cmd}")
        os.system(cmd)
        # if not os.path.exists(file_path):
        cmd = f"unzip {zip_file} -d {file_name_path}"
        os.system(cmd)
        logger.info(f"执行解压指令==》{cmd}")
        # 解压包 路径
        if not os.path.exists(file_name_path.replace('\\', '')):
            assert 0, f"解压路径不存在"
        logger.info(f"解压包路径==》》{file_name_path}")
        return file_name_path.replace('\\', '')

    def __get_vbf_path(self, path):
        '''
        可能存在三层路径
        @param path:
        @return:
        '''
        # 判断有几层路径
        logger.info(f"path>>{path}")
        files = [f for f in os.listdir(path) if f.endswith('vbf')]
        files_list = os.listdir(path)
        logger.info(f"files_list>>{files_list}")
        if not files:
            for item in files_list:
                # item=item.replace("(", "\(").replace(")", "\)")
                _path = os.path.join(path, item)
                if os.path.isdir(_path):
                    files_list2 = os.listdir(_path)
                    files = [f for f in os.listdir(_path) if f.endswith('vbf')]
                    logger.info(f"files_list2>>{files_list2}")
                    if not files:
                        for item1 in files_list2:
                            # item1 = item1.replace("(", "\(").replace(")", "\)")
                            __path = os.path.join(_path, item1)
                            if os.path.isdir(__path):
                                files_list3 = os.listdir(__path)
                                files = [f for f in os.listdir(__path) if f.endswith('vbf')]
                                logger.info(f"files_list3>>{files_list3}")
                                if files:
                                    return __path, files
                        else:
                            assert 0, "未找到安装包"
                    else:
                        path = _path
                        break

        return path, files

    def get_vbf_file_path(self, path):
        '''
        获取 VBF 文件，
        返回值为字典
               {
               “SBL_vbf”:(名称，路径)，
               “MCU_vbf”:(名称，路径)，
               BTupdater_vbf:(名称，路径)，
               }
        @param path:
        @return:
        '''
        path, files = self.__get_vbf_path(path)
        # 找到vbf的文件
        # files = [f for f in os.listdir(path) if f.endswith('vbf')]
        logger.info(f"获取的到vbf 文件为》》》{files}")
        info_dict = {}
        path1 = path.replace("(", "\(").replace(")", "\)").replace("&", "\&")
        # 2960110110AD_Bootupdater.vbf    1160110055AA_SBL.vbf   S6160110110AM_MCU.vbf
        for name in files:
            if "SBL.vbf" in name:
                sbl_vbf_path = os.path.join(path1, name)
                sbl_vbf_name = name.split("_")[0]
                sbl_vbf_path2 = os.path.join(path1, "BGM_SBL.vbf")
                cmd = f"cp -f {sbl_vbf_path} {sbl_vbf_path2}"
                logger.info(f"重命名BGM_SBL》》》{cmd}")
                os.system(cmd)
                info_dict["SBL_vbf"] = (sbl_vbf_name, sbl_vbf_path2)
            elif "MCU.vbf" in name:
                mcu_vbf_name = name.split("_")[0]
                mcu_vbf_path = os.path.join(path1, name)
                mcu_vbf_path2 = os.path.join(path1, "BGM_MCU.vbf")
                cmd = f"cp -f {mcu_vbf_path} {mcu_vbf_path2}"
                logger.info(f"重命名 BGM_MCU 》》》{cmd}")
                os.system(cmd)
                info_dict["MCU_vbf"] = (mcu_vbf_name, mcu_vbf_path2)
            elif "Bootupdater.vbf" in name:
                bootupdater_vbf_name = name.split("_")[0]
                bootupdater_vbf_path = os.path.join(path1, name)

                bootupdater_vbf_path2 = os.path.join(path1, "BTupdater.vbf")
                cmd = f"cp -f {bootupdater_vbf_path} {bootupdater_vbf_path2}"
                logger.info(f"重命名 BGM_Bootupdater 》》》{cmd}")
                os.system(cmd)

                info_dict["BTupdater_vbf"] = (
                    bootupdater_vbf_name,
                    bootupdater_vbf_path2,
                )
            else:
                pass
        logger.info(f"获取的mcu 文件相关信息{info_dict}")
        return path, info_dict

    def create_install_json_file(self, info_dict, **kwargs):
        '''
        根据升级包 生成新的 json 文件
        :param info_dict:
                info_dict = {
                "BGM_SBL.vbf": 3844,
                "BGM_MCU.vbf": 3061886,
            }
        :param kwargs:
        :return:
        '''
        file_name_path = os.path.join(forder0, "config/install.json")
        local_path = kwargs.get("local_path", file_name_path)
        # 生成 json 文件路径
        save_path = kwargs.get("save_path", os.path.dirname(local_path))

        with open(local_path, 'r') as rf:
            data = json.load(rf)
        lis = data["mcuPackageInfo"]["files"]
        new_lis = []
        for info in lis:
            filename = info["filename"]
            info["fileSize"] = info_dict.get(filename, 0)
            new_lis.append(info)

        data["mcuPackageInfo"]["files"] = new_lis
        install_save_path = os.path.join(save_path, "install.json")
        with open(install_save_path, 'w') as wf:
            json.dump(data, wf)
        logger.info(f"生成新的json文件路径为{install_save_path}")
        return install_save_path

    def create_install_boot_json_file(self, info_dict, **kwargs):
        '''
        根据升级包 生成新的 json 文件
        :param info_dict:
                info_dict = {
                "BGM_SBL.vbf": 3844,
                "BTupdater.vbf": 3061886,
            }
        :param kwargs:
        :return:
        '''
        file_name_path = os.path.join(forder0, "config/install_boot.json")
        local_path = kwargs.get("local_path", file_name_path)
        # 生成 json 文件路径
        save_path = kwargs.get("save_path", os.path.dirname(local_path))

        with open(local_path, 'r') as rf:
            data = json.load(rf)
        lis = data["mcuBootPackageInfo"]["files"]
        new_lis = []
        for info in lis:
            filename = info["filename"]
            info["fileSize"] = info_dict.get(filename, 0)
            new_lis.append(info)

        data["mcuBootPackageInfo"]["files"] = new_lis
        install_save_path = os.path.join(save_path, "install_boot.json")
        with open(install_save_path, 'w') as wf:
            json.dump(data, wf)
        logger.info(f"生成新的install_boot json文件路径为{install_save_path}")
        return install_save_path

    def get_mcu_ver(self, sd_test=None, timeout=10):
        '''

        @param sd_test:
        @return:
        '''
        os.system("ifconfig")
        logger.info(f'************ifconfig==========')
        if sd_test is None:
            self.sd_test = Sd_Tester(**self.sd_tc_config)
            self.sd_test.diagnostic_client_sim_start()
            self.sd_test.tester_present()
        else:
            self.sd_test = sd_test
        try:
            self.sd_test.send_data([0x22, 0xF1, 0x86])
            recv_data_list = (
                self.sd_test.return_udsdata_and_check_and_print_response_result(
                    "获取 mcu 版本号"
                )
            )
            t = time.time()
            self.sd_test.update_serverdoipid(0x1002)
            while time.time() - t < timeout:
                # 0x22, 0xF1, 0xF0
                self.sd_test.information_check_f1f0()
                recv_data_list = (
                    self.sd_test.return_udsdata_and_check_and_print_response_result(
                        "获取 mcu 版本号"
                    )
                )
                if recv_data_list[:3] == [0x62, 0xF1, 0xF0]:
                    break
                time.sleep(5)

            mcu_version = self.sd_test.read_mcu_version_or_check()
            logger.info(f'获取 mcu_version 的版本{mcu_version}')
            boot_version = self.sd_test.read_boot_version_or_check()
        except Exception as e:
            logger.error(f"读取mcu 版本号失败{str(e)}")
            mcu_version = None
            boot_version = None
        finally:
            if sd_test is None:
                self.sd_test.stop_tester_present()
                self.sd_test.diagnostic_client_sim_close()
            if mcu_version is None:
                assert 0, " 读取mcu 版本失败"
        return mcu_version, boot_version

    def update_mcu(self):
        '''
        升级mcu
        @return:
        '''
        # 升级
        cmd_list = [
            "export JIDU_APP_LOG_PATH=/log/",
            "export JETCRASH_DMP_DIR=/log/jetcrash/",
            "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/data/uatest",
            "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib",
            "export ENV_APP_PATH=/app/",
            "export ENV_SOA_CONFIG_PATH=/app/etc/soaconfig/",
            "export ENV_CONFIG_PATH=/data/etc/",
            "export UDSDOIP_CONFIG_PATH=/app/bin/udsconfig/",
            "export UDSDOIP_DATA_PATH=/tmp/uds/",
            "export UDSDOIP_LOG_PATH=/tmp/uds/",
            "export BOOTES_HOME_DIR=/app/etc",
        ]
        for cmd in cmd_list:
            self.bgm_ssh.type_commands(cmd, timeout=2)
            # time.sleep(0.01)

        cdm = "rm /data/debug_script_executed_count"
        self.bgm_ssh.type_commands(cdm)

        cmd = "cd /data/uatest"
        string = self.bgm_ssh.type_commands(cmd)
        cmd = "./ua_client_app"
        string = self.bgm_ssh.type_commands(cmd, timeout=10)
        logger.info(f"string>>{string}")
        cmd = "ua 4"
        string = self.bgm_ssh.type_commands(cmd, timeout=3)
        logger.info(f"string>>{string}")
        cmd = "ua 1"
        t = time.time()
        try:
            string = self.bgm_ssh.type_commands(cmd, timeout=60)
            logger.info(f"string>>{string}")
        except Exception as e:
            logger.info(f"ua 1 >>>>{str(e)}")

        t2 = time.time()
        tmp = 400 - (t2 - t)
        logger.info(f"ua 1 >>>>安装过程中等待{tmp}秒")
        time.sleep(tmp)

    def push_bgm_mcu_app_vbf(self, local_path, bgm_path="/update/installer"):
        '''
        推送 mcu 的app vbf 文件，以及引导文件BGM_SBL 的vbf ；以及对应的 json文件
        @param local_path:
        @param bgm_path:
        @return:
        '''
        # 推送mcu vbf 文件
        mcu_local_path = os.path.join(local_path, "BGM_MCU.vbf")
        self.bgm_ssh.scp_local_file_to_bgm(mcu_local_path, bgm_path=bgm_path)
        # 推送 引导 vbf 文件
        sbl_local_path = os.path.join(local_path, "BGM_SBL.vbf")
        self.bgm_ssh.scp_local_file_to_bgm(sbl_local_path, bgm_path=bgm_path)
        # 生成新的 install.json 安装app
        info_dict = {
            "BGM_SBL.vbf": os.path.getsize(sbl_local_path),
            "BGM_MCU.vbf": os.path.getsize(mcu_local_path),
        }
        install_save_path = self.create_install_json_file(info_dict)
        self.bgm_ssh.scp_local_file_to_bgm(install_save_path, bgm_path=bgm_path)

    def push_bgm_mcu_boot_vbf(self, local_path, bgm_path="/update/installer"):
        '''
        推送 mcu 的 boot的 vbf 文件，以及引导文件BGM_SBL 的vbf ；以及对应的 json文件
        @param local_path: 本地路径
        @param bgm_path: bgm 内部路径
        @return:
        '''
        # 推送 引导 vbf 文件
        sbl_local_path = os.path.join(local_path, "BGM_SBL.vbf")
        self.bgm_ssh.scp_local_file_to_bgm(sbl_local_path, bgm_path=bgm_path)
        # 推送 boot vbf 文件
        boot_local_path = os.path.join(local_path, "BTupdater.vbf")
        self.bgm_ssh.scp_local_file_to_bgm(boot_local_path, bgm_path=bgm_path)
        # 生成新的 install.json 安装app
        info_dict = {
            "BGM_SBL.vbf": os.path.getsize(sbl_local_path),
            "BTupdater.vbf": os.path.getsize(boot_local_path),
        }
        # 推送 安装boot的 json 文件
        install_boot_save_path = self.create_install_boot_json_file(info_dict)
        self.bgm_ssh.scp_local_file_to_bgm(install_boot_save_path, bgm_path=bgm_path)

    def push_update_mcu_files(self, local_path, bgm_path="/update/installer"):
        '''
        推送升级包到 bgm
        @param local_path: 本地路径
        @return:
        '''

        flash_boot = False
        flash_app = False
        # 推送 boot vbf 文件
        boot_local_path = os.path.join(local_path, "BTupdater.vbf")
        if os.path.exists(boot_local_path):
            self.push_bgm_mcu_app_vbf(local_path, bgm_path)
            flash_boot = True

        # 推送mcu vbf 文件
        mcu_local_path = os.path.join(local_path, "BGM_MCU.vbf")
        if os.path.exists(mcu_local_path):
            self.push_bgm_mcu_boot_vbf(local_path, bgm_path)
            flash_app = True

        # 判断是升级类型
        # 可以根据需要修改文件中的数组，0表示刷写boot，1表示刷写mcu，2表示两者都刷。
        if flash_boot and flash_app:
            flash_type = """{"NeedFlashECU": 2}"""
            logger.info("刷写mcu boot 和 app")
        elif flash_boot and not flash_app:
            flash_type = """{"NeedFlashECU": 0}"""
            logger.info("只刷写mcu boot")
        elif not flash_boot and flash_app:
            flash_type = """{"NeedFlashECU": 1}"""
            logger.info("只刷写mcu app")
        else:
            logger.info("mcu 的 boot 和app 的vbf 文件都不存在！")
            assert 0, "mcu 的 boot 和app 的vbf 文件都不存在！"

        file_name_path = os.path.join(forder0, "config/mcu_flag")
        with open(file_name_path, 'w+') as rf:
            rf.write(flash_type)

        self.bgm_ssh.scp_local_file_to_bgm(file_name_path, bgm_path='/update/')

        cmd_exe = "chmod 777 /update/mcu_flag"
        self.bgm_ssh.type_commands(cmd_exe)
        cmd_exe = "ls /update/"
        string = self.bgm_ssh.type_commands(cmd_exe)
        if 'mcu_flag' not in string:
            logger.error("mcu_flag 文件推送失败！！！！")


    def update_mcu_flow(
            self, local_path='', dst_mcu_ver=None, dst_boot_ver=None, **kwargs
    ):
        '''
        mcu 升级流程
        @param local_path: 为 zip包的路径，或者是vbf 文件路径
        @return:
        '''
        time_delay = kwargs.get("time_delay", 120)
        if local_path.startswith("http"):
            mcu_zip_url = local_path.replace("(", "\(").replace(")", "\)").replace("&", "\&")
            # 根据url  下载 mcu的 zip 包
            zip_path = self.down_load_file(mcu_zip_url)
            # 解压 zip 包
            file_path = self.unzip_mcu_zip(zip_path)
            # 获取 vbf 的路径  2960110110AD_Bootupdater.vbf    1160110055AA_SBL.vbf   S6160110110AM_MCU.vbf
            local_path, info_dict = self.get_vbf_file_path(file_path)
            # #
            sbl_vbf_name = info_dict.get("SBL_vbf")[0]
            dst_mcu_ver = info_dict.get("MCU_vbf")[0]
            dst_boot_ver = info_dict.get("BTupdater_vbf")[0]
            self.push_update_mcu_files(local_path)
        elif local_path.endswith("zip"):
            local_path = local_path.replace("(", "\(").replace(")", "\)").replace("&", "\&")
            file_path = self.unzip_mcu_zip(local_path)
            # 获取 vbf 的路径  2960110110AD_Bootupdater.vbf    1160110055AA_SBL.vbf   S6160110110AM_MCU.vbf
            local_path, info_dict = self.get_vbf_file_path(file_path)
            # #
            sbl_vbf_name = info_dict.get("SBL_vbf")[0]
            dst_mcu_ver = info_dict.get("MCU_vbf")[0]
            dst_boot_ver = info_dict.get("BTupdater_vbf")[0]
            self.push_update_mcu_files(local_path)
        else:
            # 判断下 文件是否存在，判断文件是否带版本号
            mcu_local_path = os.path.join(local_path, "BGM_MCU.vbf")
            sbl_vbf_path = os.path.join(local_path, "BGM_SBL.vbf")
            bootupdater_vbf_path = os.path.join(local_path, "BTupdater.vbf")
            if (
                    not os.path.exists(mcu_local_path)
                    or not os.path.exists(sbl_vbf_path)
                    or not os.path.exists(bootupdater_vbf_path)
            ):
                #
                # 删除 文件 防止下一轮找不到版本号
                re_list = [
                    f"rm -rf {mcu_local_path}",
                    f"rm -rf {sbl_vbf_path}",
                    f"rm -rf {bootupdater_vbf_path}",
                ]
                for cmd in re_list:
                    os.system(cmd)
                # 处理带版本号的文件
                local_path, info_dict = self.get_vbf_file_path(local_path)
                # #
                dst_mcu_ver = info_dict.get("MCU_vbf")[0]
                dst_boot_ver = info_dict.get("BTupdater_vbf")[0]

                self.push_update_mcu_files(local_path)
                ##删除 文件，下一轮重新生成
                re_list = [
                    f"rm -rf {mcu_local_path}",
                    f"rm -rf {sbl_vbf_path}",
                    f"rm -rf {bootupdater_vbf_path}",
                ]
                for cmd in re_list:
                    os.system(cmd)
            else:
                self.push_update_mcu_files(local_path)

        # # todo 执行升级操作
        logger.info("升级前读取 mcu 版本号")
        update_flag = True
        mcu_version, boot_version = None, None
        self.get_mcu_ver()
        for index in range(1):
            # 执行升级
            self.update_mcu()
            # logger.info(f"》》》》》升级 mcu 后延时 {time_delay} 秒《《《《《《《《《《《《")
            # time.sleep(time_delay)
            logger.info("升级后读取 mcu 版本号")
            logger.info(f'ifconfig=============================')
            mcu_version, boot_version = self.get_mcu_ver(timeout=time_delay)
            update_flag = True
            if dst_mcu_ver and mcu_version != dst_mcu_ver.upper():
                logger.error(
                    f"升级后的版本和预期版本不一样，mcu_version 预期为{dst_mcu_ver}实际为{mcu_version}"
                )
                update_flag = False
            if dst_boot_ver and boot_version != dst_boot_ver.upper():
                logger.error(
                    f"升级后的版本和预期版本不一样，boot_version预期为{dst_boot_ver}实际为{boot_version}"
                )
                update_flag = False
            if update_flag:
                break
        # if not update_flag:
        #     self.change_bgm_env.reset_bgm()
        assert update_flag, "mcu升级失败"
        return mcu_version, boot_version

    def chmod_udp_pcap_tool(self):
        '''
        授权 文件 否咋无法使用
        @return:
        '''
        path = os.path.join(forder0, 'case_helper/tools/udp_pcap')
        cmd = f'chmod 777 {path}'
        logger.info(f"授权可执行文件=》》{cmd}")
        os.system(cmd)

    def pase_udp_pcap_to_csv(self, pcap_path, csv_name=None, csv_path=None):
        '''
        解析 pcap 包到 csv
        @param pcap_path:  r"/root/ltg/sat/xat_cases/legacy/mcu/00ltg/udp.pcap"
        @param csv_name: 要保存的csv 文件名 默认和pcap 包名称一致
        @param csv_path: 保存的csv 路径，默认会在logs 目录下
        @return:
        '''

        if csv_name is None:
            # 不传参数 默认去pcap 包的名称
            csv_name = os.path.basename(pcap_path).split('.')[0]

        if csv_path is None:
            # 不传递则存在logs 目录下
            csv_path = os.path.join(forder0, 'logs')
            if not os.path.exists(csv_path):
                os.makedirs(csv_path)
        # 保存csv 全路径
        save_csv_path = os.path.join(csv_path, csv_name + ".csv")
        # 工具路径
        udp_pcap_path = os.path.join(forder0, 'case_helper/tools/udp_pcap')
        cmd = f"{udp_pcap_path} --pcap_path {pcap_path} --csv_path {save_csv_path}"
        logger.info(f"开始转化pcap文件到csv=》》{cmd}")
        t = time.time()
        os.system(cmd)
        # 确保文件生成，否则报错提示
        if not os.path.exists(save_csv_path):
            assert 0, f"未生成 {save_csv_path} 文件 "

        logger.info(f"转化pcap文件到csv=》》结束路径为{save_csv_path}，耗时{time.time() - t}秒")
        return save_csv_path

    def parse_one_eth_packet(self, data_info_string, packet_index, time_string):
        '''
        解析 一条 eth 报文的数据
        UDP Payload格式： 总线编号+报文ID+ 毫秒时间戳 +报文长度 Data…总线编号 + 报文ID + 毫秒时间戳+ 报文长度+ Data… 结束符（0xFE）
        @param data_info_string:
        @param packet_index:
        @param time_string:
        @return:
        '''
        can_map_dic = {
            2: "Info CANFD",
            3: "AD CANFD",
            4: "Propulsion CAN",
            5: "Chassis CAN1",
            6: "Chassis CAN2",
            7: "PassiveSafety CAN",
            8: "Connectivity CANFD",
            9: "Body CAN",
            10: "BodyExposed CANFD",
            11: "BodyALM CANFD1",
            12: "BodyALM CANFD2",
        }
        lin_map_dic = {
            41: "CEM_LIN1",
            42: "CEM_LIN2",
            43: "CEM_LIN3",
            44: "CEM_LIN4",
            45: "CEM_LIN5",
            46: "CEM_LIN6",
            47: "CEM_LIN7",
        }
        one_udp_data_list = []
        while 1:
            # 通道 一个字节
            channel_index_string = data_info_string[:2]
            channel_index = int(channel_index_string, 16)
            # 报文ID：LIN报文ID占1个字节；
            # CAN/CANFD报文ID占2bytes；
            # FlexRay 报文ID（ SLOT ID（2Byte） +BASE CYCLE（1Byte）+ Repetition（1Byte）)共占4Byte；报文ID从报文接收模块获取。
            if channel_index == 1:
                # fr   FlexRay
                channel_name = "backbonefr"
                count = 8
            elif 2 <= channel_index <= 12:
                # can
                channel_name = can_map_dic.get(channel_index)
                count = 4
            elif 41 <= channel_index <= 47:
                # lin
                channel_name = lin_map_dic.get(channel_index)
                count = 2
            else:
                # 异常总线
                channel_name = None
                count = None

            # id  1  2  4 字节
            msg_id_string = data_info_string[2 : 2 + count]
            base_cycle = None
            repetition = None
            if len(msg_id_string) == 8:
                msg_id = msg_id_string[:4]
                base_cycle = int(msg_id_string[4:6], 16)
                repetition = int(msg_id_string[6:8], 16)
            else:
                msg_id = msg_id_string
            # 时间毫秒 2
            ms_time_string = data_info_string[2 + count : 6 + count]
            # 数据长度 1个字节
            msg_len = data_info_string[6 + count : 6 + count + 2]
            msg_len_int = int(msg_len, 16) * 2
            # 数据内容
            msg_content = data_info_string[6 + count + 2 : 8 + count + msg_len_int]
            # 剩余部分
            left_data = data_info_string[8 + count + msg_len_int :]
            # [所在pcap 包的行数(int),通道名字（str）,报文id（int），毫秒时间（int），报文长度（int），报文内容（str），
            # base_cycle（针对fr，can lin 为None）,repetition（针对fr，can lin 为None）]
            # print(time_string, channel_name, msg_id, ms_time_string, msg_len, msg_content, base_cycle, repetition)

            channel_name = channel_name.strip().replace(" ", "").lower()
            dic = {
                "packet_index": packet_index + 1,
                "timestamp": time_string,
                "channel_name": channel_name,
                "msg_id": int(msg_id, 16),
                "ms_timestamp": int(ms_time_string, 16),
                "msg_len": msg_len_int // 2,
                "msg": msg_content,
                "msg_base_cycle": base_cycle,
                "msg_repetition": repetition,
            }

            one_udp_data_list.append(dic)
            if not left_data:
                break
            data_info_string = copy.deepcopy(left_data)

        return one_udp_data_list

    def parse_pdu_msg(self, file_path, **kwargs):
        '''
        参考文档
        https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46

        解析pud 的报文
        :param file_path: pcap 包路径
        :return:  packet_list ,packet_list
        data_list=[{所在pcap 包的行数(int),通道名字（str）,报文id（int），毫秒时间（int），报文长度（int），报文内容（str），
                     base_cycle（针对fr，can lin 为None）,repetition（针对fr，can lin 为None）}]
        packet_list=[{所在pcap 包的行数(int)，payload的 长度(int) ，结束符号(str),时间戳 （float）}]

        '''

        src_ip = kwargs.get("src_ip", "172.16.5.2")
        des_ip = kwargs.get("des_ip", "172.16.5.1")
        # 时差 默认无
        hours_diff = kwargs.get("hours_diff", 0)
        # 走的udp  还是tcp 协议
        proto = kwargs.get("proto", None)
        # 处理下 tcp 或者udp
        if proto is None:
            proto_str = None
        elif proto.lower() == "udp":
            proto_str = "11"
        else:
            proto_str = "06"
        # 处理ip
        ip_str = (
            bytes([int(i) for i in src_ip.split('.')]).hex()
            + bytes([int(i) for i in des_ip.split('.')]).hex()
        )
        # 处理返回值
        logger.info(f"开始读取pcap文件，会耗时一段时间{file_path}。。。。。")
        t1 = time.time()
        read_data = rdpcap(file_path)
        logger.info(f"读取pcap文件，耗时 {time.time() - t1}秒")
        # 存放所有的can lin fr 数据
        data_list = []
        # 存放 udp 报文的信息
        packet_list = []
        logger.info("开始解析文件，会耗时一段时间。。。。。")
        start_time = time.time()
        for packet_index in range(len(read_data)):
            packet = read_data[packet_index]
            line = bytes(packet).hex()
            packet_time = float(packet.time)
            if ip_str in line:
                # ip 方向对，再判断那种报文
                # 需要判断 带不带vlan  0200000010010200000010028100
                vlan = int(line[24 : 24 + 4], 16)
                if vlan == 0x8100:
                    packet_proto_str = line[54:56]
                    payload_start = 92
                else:
                    payload_start = 84
                    packet_proto_str = line[46:48]
                if proto_str and packet_proto_str != proto_str:
                    continue
                # 解析 数据
                payload_string = line[payload_start:]
                # UDP Payload格式：全局时钟（年月日时分秒）+ 总线编号+报文ID+ 毫秒时间戳 +报文长度 Data…总线编号 + 报文ID + 毫秒时间戳+ 报文长度+ Data… 结束符（0xFE）
                # pload 长度
                payload_string_len = len(payload_string) // 2
                # 时间戳  全局时间戳：年（1byte，只表示年份的后两位，如2022的22；） 月（1byte) 日（1byte) 时（1byte) 分（1byte) 秒（1byte)
                time_string1 = payload_string[0:12]
                time_string_list = [
                    str(int(time_string1[i : i + 2], 16)).zfill(2)
                    for i in range(0, len(time_string1), 2)
                ]
                UTC_FORMAT = r"%Y:%m:%d:%H:%M:%S"
                current_year = str(datetime.datetime.now().year)
                string = current_year[:2] + ':'.join(time_string_list)
                utc_time = datetime.datetime.strptime(string, UTC_FORMAT)
                time_string = utc_time + datetime.timedelta(hours=hours_diff)

                # 结束符
                end_string = payload_string[-2:]
                # 数据部分
                data_info_string = payload_string[12:-2]
                # 所在pcap 包的行数(int)，payload的 长度(int) ，结束符号(str)，格式化时间，时间戳 （float）
                # udp_packet_info = (packet_index + 1, payload_string_len, end_string, packet_time)
                otherStyleTime = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(int(packet_time))
                )
                udp_packet_info = {
                    "packet_index": packet_index + 1,
                    "payload_len": payload_string_len,
                    "end_string": end_string,
                    "packet_time": otherStyleTime,
                    "packet_timestamp": packet_time,
                }
                packet_list.append(udp_packet_info)

                one_udp_data_lis = self.parse_one_eth_packet(
                    data_info_string, packet_index, time_string
                )
                data_list.extend(one_udp_data_lis)
        # packet_list=[所在pcap 包的行数(int)，payload的 长度(int) ，结束符号(str),时间戳 （float）]
        # data_list=[所在pcap 包的行数(int),通道名字（str）,报文id（int），毫秒时间（int），报文长度（int），报文内容（str），
        # base_cycle（针对fr，can lin 为None）,
        # repetition（针对fr，can lin 为None）]8100
        string = f"解析耗时》》》{time.time() - start_time}秒"
        logger.info(string)
        return data_list, packet_list

    def check_end_string(self, packet_list, end_string="fe"):
        '''
        判断 结尾字符是不是 fe 结尾
        @param self:
        @param packet_list:
        @param end_string:
        @return:
        '''
        lis = [
            item
            for item in packet_list
            if item.get("end_string").lower() != end_string.lower()
        ]
        if not len(lis):
            return True
        else:
            logger.info(f"结束符不为{end_string}的是》》{lis}")
            return False

    def get_range_scop(self, data_list, cycly):
        '''
        获取分布范围
        @param data_list:
        @param cycly: 周期
        @return:
        '''
        dic = {
            "正常": 0,
            "5%以下": 0,
            "5%-10%": 0,
            "10%-20%": 0,
            "20%-30%": 0,
            "30%-40%": 0,
            "40%-50%": 0,
            "50%-60%": 0,
            "60%-70%": 0,
            "70%-80%": 0,
            "80%-90%": 0,
            "90%-100%": 0,
            "100%以上": 0,
        }
        for i in data_list:
            tt = abs(i - cycly) / cycly * 100
            if tt <= 5:
                dic["5%以下"] += 1
            elif 5 < tt <= 10:
                dic["5%-10%"] += 1
            elif 10 < tt <= 20:
                dic["10%-20%"] += 1
            elif 20 < tt <= 30:
                dic["20%-30%"] += 1
            elif 30 < tt <= 40:
                dic["30%-40%"] += 1
            elif 40 < tt <= 50:
                dic["40%-50%"] += 1
            elif 50 < tt <= 60:
                dic["50%-60%"] += 1
            elif 60 < tt <= 70:
                dic["60%-70%"] += 1
            elif 70 < tt <= 80:
                dic["70%-80%"] += 1
            elif 80 < tt <= 90:
                dic["80%-90%"] += 1
            elif 90 < tt <= 100:
                dic["90%-100%"] += 1
            else:
                dic["100%以上"] += 1
        return dic

    def check_pud_cycle(self, packet_list, min_value=0.0000, max_value=0.01):
        '''
        判断 udp 报文周期
        @param self:
        @param packet_list:
        @param max_value: 10 ms
        @param min_value: 0.8ms
        @return:
        '''
        error_list = []
        erro_value = []
        # 正常的周期计数
        count = 0
        for i in range(1, len(packet_list)):
            # 时间戳
            t1 = packet_list[i - 1].get("packet_timestamp")
            t2 = packet_list[i].get("packet_timestamp")
            temp = t2 - t1
            if min_value <= temp <= max_value:
                count += 1
                continue
            erro_value.append(temp)

            packet_index = packet_list[i].get('packet_index')
            packet_time = packet_list[i].get('packet_time')
            string = f"在pcap 文件第{packet_index}行,时间为{packet_time}，打包报文周期为{t2 - t1}不在{min_value}秒到{max_value}秒之间"
            logger.info(string)
            error_list.append(packet_list[i])

        erro_value.sort()
        erro_value.reverse()

        new_dict = self.get_range_scop(erro_value, max_value)
        new_dict["正常"] = count
        for name, value in new_dict.items():
            new_dict[name] = str(round(value / len(packet_list), 4) * 100) + "%"

        if not len(error_list):
            return True
        else:
            logger.info(f"超出范围的周期频率{new_dict}")
            logger.info(f"超出范围的周期为{erro_value}")
            logger.info(
                f"总报文数{len(packet_list)},打包报文周期异常的》》{len(error_list)}个，{error_list}"
            )
            return False

    def check_pud_len(self, packet_list, max_value=1400):
        '''
        判断 udp 报文长度

        @param self:
        @param packet_list:
        @param max_value:
        @return:
        '''
        # (3, 1361, 'fe', 1698220277.769738)
        lis = [item for item in packet_list if item.get("payload_len") > max_value]
        if not len(lis):
            return True
        else:
            logger.info(f"长度超过{max_value}的是》》{lis}")
            return False

    def get_all_channel_datas(self, data_list):
        '''
        获取所有通道数据，对解析的数据进行分类，每个通道 对应一个字典，字典厘米包含每个id 对应的所有数据

        @param data_list:
            data_list=[{所在pcap 包的行数(int),通道名字（str）,报文id（int），毫秒时间（int），报文长度（int），报文内容（str），
                     base_cycle（针对fr，can lin 为None）,repetition（针对fr，can lin 为None）}]
        @return:
        data_info_dic = {
            "adcan": {
                10: [],
                20: []
                }
            }
        '''

        data_info_dic = {}

        for item_info in data_list:
            name = item_info.get("channel_name")
            msg_id = item_info.get("msg_id")
            if name in data_info_dic:
                if msg_id in data_info_dic[name]:
                    data_info_dic[name][msg_id].append(item_info)
                else:
                    data_info_dic[name][msg_id] = [item_info]
            else:
                data_info_dic[name] = {}
                data_info_dic[name][msg_id] = [item_info]

        return data_info_dic

    def get_bus_send_recv_info(self, ipdu, channel_name: str, **kwargs):
        '''
         根据通道获取当前通道的，发送节点和接收节点的数据
         @param ipdu:  对象 self.ipdu
         @param channel_name: 通道   bodycan 等等
         @param kwargs:
         @return: {}
        {
             "发送节点": {
                 "周期发送": {
                     "BGM": [ {"msg_name": msg_name,
                             "msg_id": msg_id,
                             "msg_type": msg_type,
                             "msg_tx_method": msg_tx_method,
                             "msg_cycle": msg_cycle,
                             "msg_length": msg_length,
                             "rx_nodes": rx_nodes,
                             "tx_node": tx_node,
                             "msg_base_cycle": msg_base_cycle,
                             "msg_repetition": msg_repetition}, {}],
                     "CCD": [{}, {}],
                 },
                 "非周期发送": {
                     "BGM": [{}, {}],
                     "CCD": [{}, {}],
                 },
             },
             "接收节点": {
                 "周期发送": {
                     "BGM": [{}, {}],
                     "CCD": [{}, {}],
                 },
                 "非周期发送": {
                     "BGM": [{}, {}],
                     "CCD": [{}, {}],
                 },
             },

         }
        '''

        channel_name = channel_name.strip().replace(" ", '').lower()
        # 先判断是不是解析过了，如果已经解析过，直接从缓存里取
        if channel_name in self.__all_bus_data_info:
            return self.__all_bus_data_info[channel_name]
        bus_obj = getattr(ipdu, channel_name)
        msg_obj_lis = [i for i in dir(bus_obj) if not i.startswith("_")]
        # 存放所有 接收节点
        rx_nodes_dict = {}
        # 存放所有发送节点
        tx_nodes_dict = {}
        mcu_version = int(re.findall("\d+",self.get_mcu_ver()[0])[0][-3:])
        for name in msg_obj_lis:
            # obj = eval(f"{ipdu}.{channel_name}.{name}")
            if name =="lin_scheduleTable":
                continue
            obj = getattr(bus_obj, name)
            msg_name = getattr(obj, "msg_name")
            msg_id = getattr(obj, "msg_id")

            msg_tx_method = getattr(obj, "msg_tx_method")
            if channel_name == "cem_lin1" and mcu_version >= 140:
                if any([msg_id==0x5,msg_id==0x15,msg_id==0x25,msg_id==0x27]):
                    msg_cycle = 0.165/2
                else:
                    msg_cycle = 0.165
            elif channel_name == "cem_lin2" and mcu_version >= 140:
                msg_cycle = 0.11
            elif channel_name == "cem_lin3" and mcu_version >= 140:
                if msg_id==0x20:
                    msg_cycle = 0.135/3
                else:
                    msg_cycle = 0.135
            elif channel_name == "cem_lin4" and mcu_version >= 140:
                msg_cycle = 0.075
            elif channel_name == "cem_lin5" and mcu_version >= 140:
                msg_cycle = 0.3
            elif channel_name == "cem_lin6" and mcu_version >= 140:
                if msg_id==0x2 and msg_id==0x6:
                    msg_cycle = 0.170/2
                else:
                    msg_cycle = 0.170
            else:
                msg_cycle = getattr(obj, "msg_cycle")
            msg_length = getattr(obj, "msg_length")
            # 接收端
            rx_nodes = getattr(obj, "rx_nodes")
            # 发送端
            tx_node = getattr(obj, "tx_node")
            # fr 报文
            try:
                msg_slotid = getattr(obj, "msg_slotid")
                msg_base_cycle = getattr(obj, "msg_base_cycle")
                msg_repetition = getattr(obj, "msg_repetition")
            except Exception as e:
                msg_slotid = None
                msg_base_cycle = None
                msg_repetition = None

            try:
                # lin fr 没有这个
                msg_type = getattr(obj, "msg_type")
            except Exception as e:
                msg_type = None

            if msg_slotid is not None:
                msg_id = msg_slotid

            dic = {
                "msg_name": msg_name,
                "msg_id": msg_id,
                "msg_type": msg_type,
                "msg_tx_method": msg_tx_method,
                "msg_cycle": msg_cycle,
                "msg_length": msg_length,
                "rx_nodes": rx_nodes,
                "tx_node": tx_node,
                "msg_base_cycle": msg_base_cycle,
                "msg_repetition": msg_repetition,
            }
            # 分类 接收节点

            if msg_tx_method in tx_nodes_dict:
                if tx_node in tx_nodes_dict[msg_tx_method]:
                    tx_nodes_dict[msg_tx_method][tx_node].append(dic)
                else:
                    tx_nodes_dict[msg_tx_method][tx_node] = [dic]
            else:
                tx_nodes_dict[msg_tx_method] = {}
                tx_nodes_dict[msg_tx_method][tx_node] = [dic]

            for item in rx_nodes:
                if msg_tx_method in rx_nodes_dict:
                    if item in rx_nodes_dict[msg_tx_method]:
                        rx_nodes_dict[msg_tx_method][item].append(dic)
                    else:
                        rx_nodes_dict[msg_tx_method][item] = [dic]
                else:
                    rx_nodes_dict[msg_tx_method] = {}
                    rx_nodes_dict[msg_tx_method][item] = [dic]

        new_dict = {"rx_nodes": rx_nodes_dict, "tx_nodes": tx_nodes_dict}
        # 添加缓存，防止每次都去解析数据库，浪费时间
        self.__all_bus_data_info[channel_name] = new_dict
        return new_dict

    def get_bus_send_msg_info(
        self,
        data_dic,
        send_nodes=None,
        send_type="cyclic",
    ):
        '''

        获取 当前bus通道， send_nodes 节点 send_type 发送数据；区分bgm 发送和 非bgm 发送

        @param data_dic: 根据bus 处理得到的数据  只是单个 bus
        @param send_nodes: 如果 send_nodes 为None 表示所有节点,除去bgm的 所有节点
        @param send_type:  cyclic  ，spontaneous
        @return: 非bgm 发送 列表，bgm发送的数据 列表
         [ {"msg_name": msg_name,
                "msg_id": msg_id,
                "msg_type": msg_type,
                "msg_tx_method": msg_tx_method,
                "msg_cycle": msg_cycle,
                "msg_length": msg_length,
                "rx_nodes": [BGM,.],
                "tx_node": tx_node,
                "msg_base_cycle": msg_base_cycle,
                "msg_repetition": msg_repetition
                    },
                    {
                    ....
                    }
                ]
            ，
         [{}，{}]
        '''

        if send_nodes is not None:
            tx_nodes_data_list = (
                data_dic["tx_nodes"].get(send_type, {}).get(send_nodes, {})
            )
            bgm_tx_nodes_data_list = (
                data_dic["tx_nodes"].get(send_type, {}).get("BGM", {})
            )
            return tx_nodes_data_list, bgm_tx_nodes_data_list
        else:
            # 获取所有 发送节点的，除去BGM 自己发送
            tx_nodes_data_dic = data_dic["tx_nodes"].get(send_type, {})
            # 非bgm 发送 信息
            lis_info = []
            # bgm 发送
            bgm_send_info = []
            for nodes_name, info in tx_nodes_data_dic.items():
                if str(nodes_name).upper() == "BGM":
                    bgm_send_info.extend(info)
                else:
                    lis_info.extend(info)
            return lis_info, bgm_send_info

    def get_point2point_info(
        self, data_dic, send_nodes, recv_nodes="BGM", send_type="cyclic", **kwargs
    ):
        '''
        获取 从 send_nodes 发送给recv_nodes 的数据

        @param data_dic: 根据bus 处理得到的数据  只是单个 bus
        @param send_nodes: 发送节点
        @param recv_nodes: 接收节点 默认是 BGM
        @param send_type: 发送方式  spontaneous  ，cyclic
        @param kwargs:
        @return:

         [ {"msg_name": msg_name,
                "msg_id": msg_id,
                "msg_type": msg_type,
                "msg_tx_method": msg_tx_method,
                "msg_cycle": msg_cycle,
                "msg_length": msg_length,
                "rx_nodes": [BGM,.],
                "tx_node": tx_node,
                "msg_base_cycle": msg_base_cycle,
                "msg_repetition": msg_repetition
                    },
                    {
                    ....
                    }
                ]
        '''
        if send_nodes is not None:
            tx_nodes_data_list = data_dic["tx_nodes"][send_type][send_nodes]
            data_list = [
                item
                for item in tx_nodes_data_list
                if recv_nodes in item.get("rx_nodes", [])
            ]
            return data_list
        else:
            rx_nodes_data_list = data_dic["rx_nodes"][send_type][recv_nodes]
            return rx_nodes_data_list

    def get_bus_msgid_info(self, ipdu, channel_name: str, **kwargs):
        '''
        根据通道获取当前通道的，发送节点和接收节点的数据
        @param ipdu:  对象 self.ipdu
        @param channel_name: 通道   bodycan 等等
        @param kwargs:
        @return: {}

        '''

        channel_name = channel_name.strip().replace(" ", '').lower()
        # 先判断是不是解析过了，如果已经解析过，直接从缓存里取
        # if channel_name in self.__all_bus_data_info:
        #     return self.__all_bus_data_info[channel_name]
        bus_obj = getattr(ipdu, channel_name)
        msg_obj_lis = [i for i in dir(bus_obj) if not i.startswith("_")]
        nodes_dict = {}
        for name in msg_obj_lis:
            # obj = eval(f"{ipdu}.{channel_name}.{name}")
            if name == "lin_scheduleTable":
                continue
            obj = getattr(bus_obj, name)
            msg_name = getattr(obj, "msg_name")
            msg_id = getattr(obj, "msg_id")

            msg_tx_method = getattr(obj, "msg_tx_method")

            msg_cycle = getattr(obj, "msg_cycle")
            msg_length = getattr(obj, "msg_length")
            # 接收端
            rx_nodes = getattr(obj, "rx_nodes")
            # 发送端
            tx_node = getattr(obj, "tx_node")
            # fr 报文
            try:
                msg_slotid = getattr(obj, "msg_slotid")
                msg_base_cycle = getattr(obj, "msg_base_cycle")
                msg_repetition = getattr(obj, "msg_repetition")
            except Exception as e:
                msg_slotid = None
                msg_base_cycle = None
                msg_repetition = None

            try:
                # lin fr 没有这个
                msg_type = getattr(obj, "msg_type")
            except Exception as e:
                msg_type = None

            if msg_slotid is not None:
                msg_id = msg_slotid

            dic = {
                "msg_name": msg_name,
                "msg_id": msg_id,
                "msg_type": msg_type,
                "msg_tx_method": msg_tx_method,
                "msg_cycle": msg_cycle,
                "msg_length": msg_length,
                "rx_nodes": rx_nodes,
                "tx_node": tx_node,
                "msg_base_cycle": msg_base_cycle,
                "msg_repetition": msg_repetition,
            }
            # 分类 接收节点
            nodes_dict[msg_id] = dic

        return nodes_dict