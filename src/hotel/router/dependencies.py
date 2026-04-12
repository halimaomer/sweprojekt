"""Factory-Funktionen für Dependency Injection."""

from typing import Annotated

from fastapi import Depends

from hotel.repository.hotel_repository import HotelRepository
from hotel.service.hotel_service import HotelService
from hotel.service.hotel_write_service import HotelWriteService


def get_repository() -> HotelRepository:
    """Factory-Funktion für HotelRepository.

    :return: Das Repository
    :rtype: HotelRepository
    """
    return HotelRepository()


def get_service(
    repo: Annotated[HotelRepository, Depends(get_repository)],
) -> HotelService:
    """Factory-Funktion für HotelService."""
    return HotelService(repo=repo)


def get_write_service(
    repo: Annotated[HotelRepository, Depends(get_repository)],
) -> HotelWriteService:
    """Factory-Funktion für HotelWriteService."""
    return HotelWriteService(repo=repo)
