"""
UDS Data Templates and Constants
"""

class UdsDataConstants:
    """
    UDS Configuration Constants.
    """
    # Timeout configurations (ms)
    P2_CLIENT_MAX = 150
    P2_STAR_CLIENT_MAX = 5000
    
    P2_SERVER_MAX = 50
    P2_STAR_SERVER_MAX = 5000
    
    S3_CLIENT = 2000
    S3_SERVER = 5000
    
    # Block sizes for UDS Service 0x34, 0x36, 0x37
    MAX_BLOCK_LENGTH = 1024
    
    # Default response data structures
    DEFAULT_RESPONSE_DATA = {
        0x10: b"\x00\x32\x01\xF4", # Default timings
        0x27: b"\x00\x00\x00\x00", # Dummy seed
        0x22: b"",
    }
