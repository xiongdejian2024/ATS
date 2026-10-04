"""
DoCAN Diagnostic Server (Stub)
"""

import logging

from xat_ecu.core.interfaces import ITransport

logger = logging.getLogger(__name__)


class DocanServer:
    """
    DoCAN Server Stub (ECU simulator side)
    """
    
    def __init__(self):
        self._running = False
        
    def start(self):
        """Start the DoCAN Server stub"""
        self._running = True
        logger.info("DoCAN Server started")
        
    def stop(self):
        """Stop the server"""
        self._running = False
