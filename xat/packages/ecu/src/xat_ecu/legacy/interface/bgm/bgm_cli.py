# -*- coding: utf-8 -*-
"""
@File        : bgm_cli.py
@Author      : jinhui.zhao@jiduauto.com
@Time        : 2022/03/07 3:30 PM
@Description : description about this file
@Examples    : example of how to use it
"""

import sys
import os
import base64
import time
project_root = __import__("xat_ecu.resources", fromlist=["LEGACY_ROOT"]).LEGACY_ROOT.as_posix()
from xat_ecu.legacy.driver.ssh_client import SSHClient
from xat_ecu.legacy.common.logger import logger


class Cli:
    """ command line interface API"""

    def __init__(self, hostname, port, username, password, timeout=30):
        self.hostname = hostname
        self.port = port
        self.username = base64.b64decode(username.encode()).decode()
        self.password = base64.b64decode(password.encode()).decode()
        self.sudo_password = self.password
        self.timeout = timeout

    def connect(self):
        try:
            ssh_client = SSHClient(self.hostname, port=self.port,
                                   username=self.username, password=self.password)
        except TimeoutError:
            logger.error('Timeout from "ssh {}'.format(self.hostname))
        return ssh_client

    def exec_cmd(self, cmd, timeout=60, wait_time=1.0):
        outmsg, errmsg = self.client.exec_cmd(cmd, timeout=timeout, wait_time=wait_time)
        return outmsg, errmsg

    def sudo_cmd(self, cmd, timeout=60):
        outmsg, errmsg = self.client.sudo_exec_cmd(cmd, self.sudo_password, timeout=timeout)
        return outmsg, errmsg

    def start_interactive_cmd(self, cmd, callbak, timeout=300, password=None, if_string=True):
        return self.client.start_interactive_cmd(cmd, callbak, timeout, password, if_string)

    def stop_interactive_cmd(self, interactive_t):
        self.client.stop_interactive_cmd(interactive_t)

    def close(self):
        self.client.close()

    def reboot(self):
        """
        Reboot DUT
        :return: True always
        """
        logger.info("Reboot DUT")
        self.sudo_cmd('reboot')

        # Usually CGW reboot takes 36 sec. Sleep 60 sec to wait for CGW to be ready
        # after reboot.
        logger.info("Sleep 60 sec to wait for DUT to be ready after reboot")
        time.sleep(60)

        # After CGW reboots, make sure connection is okay.
        count = 1
        while not self.client.is_connected() and count < 11:
            try:
                logger.info(
                    "Count%s: After reboot, connecting DUT is down. To reconnect..."
                    % count)
                self.client.re_connect()

                # Sleep 2 sec
                time.sleep(2)

                count += 1
            except Exception as e:
                __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/interface/bgm/bgm_cli.py")
                logger.error('Exception: %s' % str(e))
                continue
        return True
