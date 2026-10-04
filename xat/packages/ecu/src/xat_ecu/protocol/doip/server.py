"""
DoIP Diagnostic Server (Stub)
"""

import socket
import logging

from xat_ecu.core.interfaces import ITransport

logger = logging.getLogger(__name__)


class DoipServer:
    """
    DoIP TCP Server Stub (ECU simulator side)
    """
    
    def __init__(self):
        self._socket = None
        self._running = False
        
    def start(self, host: str = "0.0.0.0", port: int = 13400):
        """Start the DoIP Server stub"""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((host, port))
        self._socket.listen(5)
        self._running = True
        logger.info(f"DoIP Server started on {host}:{port}")
        
    def stop(self):
        """Stop the server"""
        self._running = False
        if self._socket:
            self._socket.close()
            self._socket = None
