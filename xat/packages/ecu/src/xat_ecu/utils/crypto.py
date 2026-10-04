"""
Crypto - Cryptographic utilities
"""
import hashlib
import binascii

def sha256_hash(data: bytes) -> bytes:
    """Calculate SHA256 hash of data."""
    hasher = hashlib.sha256()
    hasher.update(data)
    return hasher.digest()

def crc16_ccitt(data: bytes) -> int:
    """Calculate CRC16-CCITT."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
        crc &= 0xFFFF
    return crc

def calculate_checksum(data: bytes) -> int:
    """Simple 8-bit checksum."""
    return sum(data) & 0xFF
