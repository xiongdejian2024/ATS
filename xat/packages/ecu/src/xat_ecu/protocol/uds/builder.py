"""
UDS Builder

Build UDS request bytes from DiagRequest objects.
"""

from xat_ecu.core.types import DiagRequest

class UdsBuilder:
    """UDS Request Builder"""
    
    @staticmethod
    def build_request(request: DiagRequest) -> bytes:
        """
        Build raw UDS request bytes from DiagRequest.
        
        Args:
            request: DiagRequest object
            
        Returns:
            Raw byte array representing the request
        """
        return request.to_bytes()
