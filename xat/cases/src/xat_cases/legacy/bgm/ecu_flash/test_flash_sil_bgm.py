#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :test_flash_sil_bgm.py
@time         :8/27/24 14:31
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import json
import os.path

import allure

from xat_ecu.legacy.common import exception_error
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.nuc_app import exec_shell

from framework.automotive.core.common_sil_test_base import CommonSILTestBase
from framework.automotive.utils.data_type import EcuInfo
from framework.automotive.utils.conftest_helper import parent_dir
from framework.automotive.utils.artifactory_helper import ARTIFACTORY_PASSWORD, ARTIFACTORY_USERNAME


class TestFlashSILBgm(CommonSILTestBase):
    def before_class(self, ecu: EcuInfo):
        super().before_class(self, ecu)
        task_path = os.path.join(parent_dir, '../', 'task.json')
        self.img_url = ''
        if os.path.exists(task_path):
            with open(task_path, "r") as f:
                task_dict = json.load(f)
                self.img_url = task_dict.get("img_url").replace(".bin", ".zip")
                if self.img_url:
                    return
        else:
            self.sdb_version = ecu.get('sdb_version')
            if not self.sdb_version:
                raise Exception('缺少--sdb_version=版本号，无法升级')
            self.release_version = ecu.get('release_version')
            if "artifactory" in self.sdb_version:
                self.img_url = self.sdb_version
            else:
                if self.sdb_version.startswith('v'):
                    sdb_ver = self.sdb_version[1:].replace('.', '')
                    app_ver = f'6160110{sdb_ver}{self.sdb_version}'
                else:
                    sdb_ver = self.sdb_version.replace('.', '')
                    app_ver = f'6160110{sdb_ver}{self.release_version}'
                    self.sdb_version = f"v{self.sdb_version}"
                base_img_url = f'https://repo.jidudev.com/artifactory/BGMSoftware/Release/{self.sdb_version}/{app_ver}'
                self.img_url = f'{base_img_url}/{app_ver}.zip'
                logger.info(f"bgm app包的链接为:{self.img_url}")

    def before_each_func(self, ecu: EcuInfo):
        pass

    def after_each_func(self, ecu: EcuInfo):
        pass

    def after_class(self, ecu: EcuInfo):
        pass

    def test_update_sil_bgm(self):
        app_zip_name = self.img_url.split('/')[-1]  # 6160110210AA.zip
        app_name = app_zip_name.split(".zip")[0]
        local_app_path = os.path.join(parent_dir, 'update', app_zip_name)
        with allure.step(f"下载{self.img_url}到update目录下"):
            if not os.path.exists(local_app_path):
                logger.info(f'不存在{local_app_path}, 从artifactory上下载')
                res = os.system(
                    command=f'curl -o {local_app_path} -u {ARTIFACTORY_USERNAME}:{ARTIFACTORY_PASSWORD} {self.img_url}')
                if res != 0:
                    raise exception_error.CmdExecuteError(f"下载{self.img_url}失败")
                # ArtifactoryHelper.download(self.img_url, local_app_path)
            else:
                logger.info(f'本地存在{local_app_path}')
        with allure.step("解压升级包"):
            output = exec_shell(command='date -u').get('output')
            res = os.system(command=f"cd {os.path.join(parent_dir, 'update')};rm -rf image")
            if res != 0:
                raise exception_error.CmdExecuteError(
                    f"删除{os.path.join(parent_dir, 'update', 'image')}失败, 返回值{res}")
            res = os.system(command=f"cd {os.path.join(parent_dir, 'update')};unzip {app_zip_name}")
            if res != 0:
                raise exception_error.CmdExecuteError(f"解压{local_app_path}失败, 返回值{res}")
        with allure.step("上传到bgm的update目录"):
            local_path = os.path.join(os.path.join(parent_dir, 'update', 'image', 'appfs.img.bz2'))
            self.ssh.bgm_ssh.type_commands(commands=f'cd /update;rm -rf appfs.img*')
            self.ssh.bgm_ssh.scp_local_file_to_bgm(local_path=local_path, bgm_path='/update')
        with allure.step("解压升级镜像"):
            if output:
                self.ssh.bgm_ssh.type_commands(commands=f'date -s "{output}"')
            self.ssh.bgm_ssh.type_commands(commands=f'cd /update;tar -mxf appfs.img.bz2', timeout=600)
        with allure.step("升级app"):
            self.ssh.bgm_ssh.type_commands(commands="cd /update;mount -t ext4 -o loop appfs.img /app")
            with allure.step("检查版本"):
                version = self.ssh.bgm_ssh.get_version().get('build_version').replace(' ', '')
                if version != app_name:
                    raise exception_error.CmdExecuteError(f"升级后版本号不是{app_name}, 而是{version}")
