"""
UDS Parser

Parse raw UDS response bytes into DiagResponse objects.
"""
from typing import Optional, List
import logging

from xat_ecu.core.types import DiagResponse, NrcCode

logger = logging.getLogger(__name__)


class UdsParser:
    """UDS Response Parser"""
    
    @staticmethod
    def parse_response(raw_data: bytes) -> Optional[DiagResponse]:
        """
        Parse raw UDS response bytes into DiagResponse.
        
        Args:
            raw_data: Raw byte array of the response
            
        Returns:
            DiagResponse object or None if invalid
        """
        if not raw_data:
            return None
            
        if raw_data[0] == 0x7F:
            # Negative response
            if len(raw_data) >= 3:
                req_sid = raw_data[1]
                nrc = raw_data[2]
                return DiagResponse(
                    service_id=req_sid,
                    is_positive=False,
                    nrc=nrc,
                    raw_data=raw_data
                )
            else:
                logger.warning("Invalid negative response length")
                return None
                
        # Positive response
        # Typically sid + 0x40
        resp_sid = raw_data[0]
        req_sid = resp_sid - 0x40 if resp_sid >= 0x40 else resp_sid
        
        return DiagResponse(
            service_id=req_sid,
            is_positive=True,
            data=raw_data[1:],
            raw_data=raw_data
        )
