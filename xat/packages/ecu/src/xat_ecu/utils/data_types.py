"""
Data Types - Utilities for data type conversion
"""

import struct
from typing import Union, List

def hex_to_bytes(hex_str: str) -> bytes:
    """Convert hex string to bytes, ignoring spaces."""
    hex_str = hex_str.replace(" ", "")
    if len(hex_str) % 2 != 0:
        hex_str = "0" + hex_str
    return bytes.fromhex(hex_str)

def bytes_to_hex(data: bytes, separator: str = "") -> str:
    """Convert bytes to hex string."""
    return data.hex(separator).upper()

def int_to_bytes(value: int, length: int, byteorder: str = 'big') -> bytes:
    """Convert integer to bytes."""
    return value.to_bytes(length, byteorder=byteorder)

def bytes_to_int(data: bytes, byteorder: str = 'big') -> int:
    """Convert bytes to integer."""
    return int.from_bytes(data, byteorder=byteorder)

def get_bit(value: int, bit_position: int) -> int:
    """Get the value of a specific bit."""
    return (value >> bit_position) & 1

def set_bit(value: int, bit_position: int, bit_value: int) -> int:
    """Set the value of a specific bit."""
    if bit_value:
        return value | (1 << bit_position)
    else:
        return value & ~(1 << bit_position)

def get_bits(value: int, start_bit: int, length: int) -> int:
    """Get the value of a range of bits."""
    mask = (1 << length) - 1
    return (value >> start_bit) & mask

def set_bits(value: int, start_bit: int, length: int, bits_value: int) -> int:
    """Set the value of a range of bits."""
    mask = ((1 << length) - 1) << start_bit
    value = value & ~mask
    return value | ((bits_value & ((1 << length) - 1)) << start_bit)
