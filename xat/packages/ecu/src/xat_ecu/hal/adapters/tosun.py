import glob
import logging
import os
import socket
import subprocess
import time
from pathlib import Path
from typing import Optional

try:
    import psutil
except ImportError:
    psutil = None

from xat_ecu.core.types import BusMessage
from xat_ecu.hal.adapter import BaseHardwareAdapter
from xat_ecu.hal.registry import AdapterRegistry

logger = logging.getLogger(__name__)

@AdapterRegistry.register("tosun")
class TosunAdapter(BaseHardwareAdapter):
    """
    Tosun TSMaster硬件适配器。
    Tosun TSMaster hardware adapter using UDP IPC with IniMap executable.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if psutil is None:
            raise ImportError("psutil library is required for TosunAdapter")
            
        self.host = self.config.get("host", "127.0.0.1")
        self.port = self.config.get("port", 8001)
        self.tosun_serial = self.config.get("tosun_serial", "")
        
        # Base path for IniMap executable
        self.inimap_dir = self.config.get("inimap_dir", "./libTSCANAPI/linux")
        self.ini_path = self.config.get("ini_path", "./config1.ini")
        self.logpath = self.config.get("logpath", "./tosun.log")
        
        self.client_socket = None
        self.proc = None

    def _init_ini_config(self) -> None:
        """Generate INI configuration for IniMap"""
        is_save_log = self.config.get("is_save_log", 1)
        msg_infos_list = self.config.get("msg_infos_list", [])
        
        with open(self.ini_path, "w") as f:
            f.write("[config]\n")
            f.write("E2EConfig = 1\n")
            f.write(f"SaveLog = {is_save_log}\n")
            f.write(f"DeviceSerial = {self.tosun_serial}\n")
            f.write("E2ECRCDLL = ./E2ECRCDLL.dll\n")
            f.write("CRCFunc = crc8_calc\n")
            f.write("FlexRaySRCIP = 127.0.0.1\n")
            f.write(f"FlexRaySRCPORT = {self.port - 1}\n")
            f.write("FlexRayDSTIP = 127.0.0.1\n")
            f.write(f"FlexRayDSTPORT = {self.port}\n")
            
            if self.port == 8003:
                f.write("Chn_AIntervalCnt = 0,0,0,0,0,0,0,0,0,0,0,0\n\n")
                
            for msg_infos in msg_infos_list:
                for msg_info in msg_infos:
                    for msginfo in msg_info:
                        if isinstance(msginfo, str):
                            f.write(msginfo + "\n")
                        else:
                            if msginfo:
                                for sig_info in msginfo:
                                    f.write(sig_info + "\n")
                f.write("\n")

    def _do_start(self) -> None:
        self._init_ini_config()
        
        # Start IniMap subprocess
        inimap_path = Path(self.inimap_dir) / "IniMap"
        cmd = f"cd {self.inimap_dir}; ./IniMap {os.path.abspath(self.ini_path)} {os.path.abspath(self.logpath)}"
        
        self.proc = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
            close_fds=True, preexec_fn=os.setsid, text=True
        )
        
        # Wait for initialization
        time.sleep(1.0)
        if self.proc.poll() is not None:
            stdout = self.proc.stdout.read() if self.proc.stdout else ""
            stderr = self.proc.stderr.read() if self.proc.stderr else ""
            raise RuntimeError(f"Failed to start Tosun IniMap. stdout: {stdout}, stderr: {stderr}")
            
        # Connect UDP socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.bind((self.host, self.port))

    def _do_stop(self) -> None:
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            
        if self.proc:
            try:
                parent_proc = psutil.Process(self.proc.pid)
                for child_proc in parent_proc.children(recursive=True):
                    child_proc.kill()
                parent_proc.kill()
                
                # Cleanup INI files
                clear_ini_map = self.config.get("clear_ini_map", True)
                if clear_ini_map:
                    for file in glob.glob('config*.ini'):
                        try:
                            os.remove(file)
                        except OSError as e:
                            logger.warning(f"Failed to remove INI file {file}: {e}")
            except (OSError, psutil.NoSuchProcess) as e:
                logger.warning(f"Error stopping Tosun IniMap: {e}")
            self.proc = None

    def _do_send(self, msg: BusMessage) -> None:
        if self.client_socket is None:
            return
        # Convert BusMessage to raw bytes expected by Tosun UDP protocol
        # (Assuming custom serialization is handled externally or passing raw bytes here temporarily)
        raw_data = bytes(msg.data)
        self.client_socket.sendto(raw_data, (self.host, self.port - 1))

    def _do_recv(self, timeout: float) -> Optional[BusMessage]:
        if self.client_socket is None:
            return None
        
        self.client_socket.settimeout(timeout)
        try:
            data, _ = self.client_socket.recvfrom(1024)
            # Dummy parsing, should be aligned with Tosun protocol
            return BusMessage(
                msg_id=0,
                data=list(data),
                timestamp=time.time(),
                bus_name="tosun",
                dlc=len(data)
            )
        except socket.timeout:
            return None
