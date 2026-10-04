"""
UDS Security Module

Migrated from uds_securitycal.py and aes_128_cbc.py.
Supports AES-128-CBC encryption for seed/key calculation.
Allows users to register custom algorithms.
"""

import struct
from typing import Callable, Dict
import logging

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    _HAS_CRYPTOGRAPHY = True
except ImportError:
    _HAS_CRYPTOGRAPHY = False

from xat_ecu.core.types import SecurityLevel

logger = logging.getLogger(__name__)


class Aes128Cbc:
    """AES-128-CBC Crypto Utility"""
    
    @staticmethod
    def encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
        """Encrypt data using AES-128-CBC."""
        if not _HAS_CRYPTOGRAPHY:
            raise ImportError("cryptography package required: pip install cryptography")
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(data) + encryptor.finalize()

    @staticmethod
    def decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
        """Decrypt data using AES-128-CBC."""
        if not _HAS_CRYPTOGRAPHY:
            raise ImportError("cryptography package required: pip install cryptography")
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(data) + decryptor.finalize()


class SecurityManager:
    """
    Security Access Manager.
    Pluggable architecture allowing users to register custom algorithms.
    """
    
    def __init__(self):
        self._algorithms: Dict[int, Callable[[bytes, bytes, bytes], bytes]] = {}
        # Register default algorithms
        self.register_algorithm(SecurityLevel.LEVEL_1, self.default_algo)
        self.register_algorithm(SecurityLevel.LEVEL_3, self.default_algo)

    def register_algorithm(self, level: int, algorithm: Callable[[bytes, bytes, bytes], bytes]):
        """
        Register a security algorithm for a specific security level.
        
        Args:
            level: The security level (1, 3, etc. or defined in SecurityLevel)
            algorithm: A callable that takes (seed, mask, constant) and returns the key.
        """
        self._algorithms[level] = algorithm

    def compute_key(self, level: int, seed: bytes, mask: bytes = b"", constant: bytes = b"") -> bytes:
        """
        Compute the key for a given seed and security level.
        """
        algo = self._algorithms.get(level)
        if not algo:
            logger.error(f"No security algorithm registered for level {level}")
            raise ValueError(f"Unsupported security level {level}")
            
        return algo(seed, mask, constant)
        
    @staticmethod
    def default_algo(seed: bytes, mask: bytes, constant: bytes) -> bytes:
        """
        Default dummy AES algorithm structure.
        Users should override this with their specific ECU logic.
        """
        # Ensure padding for 16-byte block
        padded_seed = seed.ljust(16, b'\x00')
        key = mask.ljust(16, b'\x00') if mask else (b'\x00' * 16)
        iv = constant.ljust(16, b'\x00') if constant else (b'\x00' * 16)
        
        return Aes128Cbc.encrypt(padded_seed, key, iv)
