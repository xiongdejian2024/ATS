"""
Vehicle Module - Represents different vehicle types and models
"""

from .base import VehicleProfile
from .loader import VehicleDataLoader

__all__ = [
    "VehicleProfile",
    "VehicleDataLoader",
]
