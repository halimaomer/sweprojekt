"""Modul für die Geschäftslogik."""

from hotel.service.exceptions import (
    NotFoundError,
    VersionOutdatedError,
)
from hotel.service.hotel_dto import HotelDTO
from hotel.service.hotel_service import HotelService
from hotel.service.hotel_write_service import HotelWriteService
from hotel.service.mailer import send_mail
from hotel.service.standort_dto import StandortDTO

__all__ = [
    "HotelDTO",
    "HotelService",
    "HotelWriteService",
    "NotFoundError",
    "StandortDTO",
    "VersionOutdatedError",
    "send_mail",
]
