#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename     :sil_file_ctrl.py
@time         :8/29/24 20:59
@author       :dejian.xiong@jiduauto.com
@description  :
"""
import sys

# from ecu_simulator.interface.cdc.cdca_adb import file_download as cdca_file_download
# from ecu_simulator.interface.cdc.cdca_adb import file_upload as cdca_file_upload

from xat_ecu.legacy.driver.ssh_interface import file_download, file_upload, command_send

if __name__ == "__main__":
    if sys.argv[1] == "pull":
        file_download(
            device_name=sys.argv[2],
            local_path=sys.argv[3],
            remote_path=sys.argv[4]
        )
    elif sys.argv[1] == "push":
        command_send(
            connect_type='vlan',
            device_name=sys.argv[2],
            cmd=f'mkdir -p /tmp/upload_tmp;chmod 777 * -R /tmp/upload_tmp'
        )
        file_upload(
            connect_type='vlan',
            device_name=sys.argv[2],
            local_path=sys.argv[3],
            remote_path='/tmp/upload_tmp'
        )
        status, terminal_return = command_send(
            connect_type='vlan',
            device_name=sys.argv[2],
            cmd=f'cp -rf /tmp/upload_tmp/* {sys.argv[4]};cd /usr/bin/;cat vlanset.sh;sync'
        )
        print(sys.argv, terminal_return)
