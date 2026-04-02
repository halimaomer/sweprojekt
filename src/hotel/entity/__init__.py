"""Modul für persistente Hoteldaten."""

from hotel.entity.base import Base
from hotel.entity.hotel import Hotel
from hotel.entity.standort import Standort
from hotel.entity.zimmer import Zimmer

__all__ = [
    "Base",
    "Hotel",
    "Standort",
    "Zimmer",
]
