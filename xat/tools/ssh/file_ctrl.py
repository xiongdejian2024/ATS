import sys

# from ecu_simulator.interface.cdc.cdca_adb import file_download as cdca_file_download
# from ecu_simulator.interface.cdc.cdca_adb import file_upload as cdca_file_upload

from xat_ecu.legacy.driver.ssh_interface import file_download, file_upload


if __name__ == "__main__":
    if sys.argv[1] == "pull":
        file_download(
            device_name = sys.argv[2],
            local_path = sys.argv[3],
            remote_path = sys.argv[4]
        )
    elif sys.argv[1] == "push":
        file_upload(
            device_name = sys.argv[2],
            local_path = sys.argv[3],
            remote_path = sys.argv[4]
        )
