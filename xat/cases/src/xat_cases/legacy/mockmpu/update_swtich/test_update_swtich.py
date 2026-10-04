# -*- coding: utf-8 -*-
"""
@File        : updata_swtich
@Author      : tanggeng.li@jiduauto.com
@Time        : 2024/7/18 19:23
@Description : 升级swtich 版本

"""
import pytest

from xat_cases.legacy.mockmpu.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.interface.nuc_app import *
from xat_ecu.legacy.driver.ssh_interface import file_download, file_upload


@allure.story("升级swtich")
class TestUpdateSwtich(TestABCBase):
    def before_class(self, ecu):
        logger.info("before_class")
        super().before_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.obd_iface = ecu.tb_config.get("bus", {}).get('eth_obd')

    def after_each_func(self, ecu):
        super().after_each_func(ecu)
        logger.info("after_each_func")
        self.io.bgm_power_off()
        time.sleep(2)
        self.io.bgm_power_on()
        time.sleep(20)

    def after_class(self, ecu):
        logger.info("after_class")
        super().after_class(self, ecu)

    @pytest.mark.update_engine_swtich
    def test_update_swtich_engine_version_caseid_0001(self):
        '''
        升级工程版本 swtich 升级前 如果能连上BGM 则会下载BGM 内部的swtich 版本存在/root/bgm_current_swtich 下
        @return:
        '''
        path = "/root/bgm_current_swtich"
        bgm_wtich_pat = '/app/firmware/BGM_Switch_B_FW.bin'
        try:
            if not os.path.exists(path):
                os.makedirs(path)
                # 下载 bgm 内部的 swtich 版本
                file_download(device_name='BGM', local_path=path, remote_path=bgm_wtich_pat, connect_type='obd')
        except Exception as e:
            logger.error("下载bgm的wtich失败")
            os.system(f"rm -rf {path}")
        # # 先开后门升级 如果失败则 不开后门升级
        try:
            logger.info("开始升级swtich 工程版本")
            self.ssh.update_mcu_switch(obd_iface=self.obd_iface, open_obd=True)
            logger.info("工程版本swtich 升级成功")
        except Exception as e:
            logger.info("开后门升级失败")
            self.ssh.update_mcu_switch(obd_iface=self.obd_iface, open_obd=False)
            logger.info("工程版本swtich 升级成功")

    @pytest.mark.update_release_swtich
    def test_update_swtich_release_version_caseid_0001(self):
        '''
        刷写 release 版本
            默认升级 从bgm下载下来的swtich 版本  存放在 /root/bgm_current_swtich下 升级成功后则删除该版本
            如果不存在，则升级默认的swtich版本 在 ./update_swtich/swtich_version 路径下
        @return:
        '''
        path = "/root/bgm_current_swtich"
        if os.path.exists(path) and os.listdir(path):
            # 路径下有版本
            swtich_ver = os.path.join(path, os.listdir(path)[0])
        else:
            logger.info("采用默认的swtich 版本")
            p = "./update_swtich/swtich_version"
            pp = os.listdir(p)[0]
            swtich_ver = os.path.join(os.path.abspath('.'), p, pp)

        logger.info(f"swtich_ver={swtich_ver}")
        try:
            self.ssh.update_mcu_switch(obd_iface=self.obd_iface, software_path=swtich_ver, open_obd=False)
            os.system(f"rm -rf {path}")
            logger.info("relaease版本 swtich 升级成功")
        except Exception as e:
            logger.info("未开后门升级失败")
            time.sleep(10)
            self.ssh.update_mcu_switch(obd_iface=self.obd_iface, software_path=swtich_ver, open_obd=True)
            os.system(f"rm -rf {path}")
            logger.info("relaease版本 swtich 升级成功")

    @pytest.mark.update_swtich_need_auth
    def test_update_swtich_need_auth_caseid_0001(self):
        '''
        刷写 swtich 版本
            默认升级 /root/bgm_swtich 下版本
            如果不存在，则升级默认的swtich版本 在 ./update_swtich/swtich_version 路径下
        @return:
        '''
        path = "/root/bgm_swtich"
        if os.path.exists(path) and os.listdir(path):
            # 路径下有版本
            swtich_ver = os.path.join(path, os.listdir(path)[0])
        else:
            assert 0, "/root/bgm_swtich  路径下没有 swtich 版本，需要把目标版本放在当前路径下，只能有一个版本"

        logger.info("需授权进行  swtich relaease版本升级")
        self.ssh.update_mcu_switch(obd_iface=self.obd_iface, software_path=swtich_ver, open_obd=True)
        logger.info("relaease版本 swtich 升级成功")

    @pytest.mark.update_swtich_no_need_auth
    def test_update_swtich_no_need_auth_caseid_0001(self):
        '''
        刷写 swtich 版本
            默认升级 /root/bgm_swtich 下版本
            如果不存在，则升级默认的swtich版本 在 ./update_swtich/swtich_version 路径下
        @return:
        '''
        path = "/root/bgm_swtich"
        if os.path.exists(path) and os.listdir(path):
            # 路径下有版本
            swtich_ver = os.path.join(path, os.listdir(path)[0])
        else:
            assert 0, "/root/bgm_swtich  路径下没有 swtich 版本，需要把目标版本放在当前路径下，只能有一个版本"

        logger.info(f"swtich_ver={swtich_ver} 不需要授权")
        logger.info("不授权进行  swtich relaease版本升级")
        self.ssh.update_mcu_switch(obd_iface=self.obd_iface, software_path=swtich_ver, open_obd=False)
        logger.info("relaease版本 swtich 升级成功")
