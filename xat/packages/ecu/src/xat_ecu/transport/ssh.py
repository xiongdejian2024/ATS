import logging
from typing import Optional, Callable, Any
from xat_ecu.core.interfaces import ITransport, ICredentialProvider

try:
    import paramiko
except ImportError:
    paramiko = None

logger = logging.getLogger(__name__)

class SSHTransport(ITransport):
    """
    SSH/SCP Remote Communication Transport.
    """
    def __init__(self, host: str, credential_provider: ICredentialProvider, port: int = 22, **kwargs):
        if paramiko is None:
            raise ImportError("paramiko library is required for SSHTransport")
            
        self.host = host
        self.port = port
        self.credential_provider = credential_provider
        self.config = kwargs
        
        self.client: Optional[paramiko.SSHClient] = None
        self.is_connected = False
        self._rx_callback: Optional[Callable[[Any], None]] = None

    def connect(self) -> None:
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            credentials = self.credential_provider.get_credentials(self.host)
            
            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=credentials.username,
                password=credentials.password,
                key_filename=credentials.key_filename,
                timeout=self.config.get('timeout', 10.0)
            )
            self.is_connected = True
            logger.info(f"SSHTransport connected to {self.host}:{self.port}")
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/transport/ssh.py")
            logger.error(f"Failed to connect SSHTransport: {e}")
            raise

    def disconnect(self) -> None:
        if self.client:
            self.client.close()
        self.client = None
        self.is_connected = False
        logger.info("SSHTransport disconnected.")

    def send(self, data: bytes, **kwargs) -> None:
        """
        Send data as a command to be executed, or via an opened channel.
        For simplicity, mapping `data` as a shell command string.
        """
        if not self.is_connected or not self.client:
            raise RuntimeError("SSHTransport is not connected")
            
        command = data.decode('utf-8', errors='ignore')
        stdin, stdout, stderr = self.client.exec_command(command)
        
        # We can optionally capture stdout here or rely on the caller
        result = stdout.read()
        if self._rx_callback and result:
            self._rx_callback(result)

    def receive(self, timeout: float) -> Optional[bytes]:
        """
        In a typical SSH scenario, receive might read from an active shell channel.
        For simple command execution, this can be handled asynchronously or omitted.
        """
        return None

    def set_receive_callback(self, callback: Callable[[Any], None]) -> None:
        self._rx_callback = callback
        
    def scp_put(self, local_path: str, remote_path: str) -> None:
        """Upload file via SCP/SFTP"""
        if not self.is_connected or not self.client:
            raise RuntimeError("SSHTransport is not connected")
            
        sftp = self.client.open_sftp()
        try:
            sftp.put(local_path, remote_path)
        finally:
            sftp.close()

    def scp_get(self, remote_path: str, local_path: str) -> None:
        """Download file via SCP/SFTP"""
        if not self.is_connected or not self.client:
            raise RuntimeError("SSHTransport is not connected")
            
        sftp = self.client.open_sftp()
        try:
            sftp.get(remote_path, local_path)
        finally:
            sftp.close()
